#!/usr/bin/env python3
#                  _     _
#  _ __ ___  _ __ (_) __| | ___
# | '_ ` _ \| '_ \| |/ _` |/ _ \
# | | | | | | |_) | | (_| |  __/
# |_| |_| |_| .__/|_|\__,_|\___|
#           |_|
#
# mpide - MicroPython (Integrated) Development Environment
# Copyright (C) 2024 - Frans Fürst
#
# mpide is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# mpide is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details at <http://www.gnu.org/licenses/>.
#
# Anyway this project is not free for machine learning. If you're using any content of this
# repository to train any sort of machine learned model (e.g. LLMs), you agree to make the whole
# model trained with this repository and all data needed to train (i.e. reproduce) the model
# publicly and freely available (i.e. free of charge and with no obligation to register to any
# service) and make sure to inform the author (me, frans.fuerst@protonmail.com) via email how to
# get and use that model and any sources needed to train it.

"""Magic REPL and file synchronization toolbox"""

# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=fixme

import argparse
import asyncio
import builtins
import io
import logging
import re
import sys
from collections.abc import Iterable, Iterator, MutableSequence, Sequence
from contextlib import contextmanager, suppress
from pathlib import Path

import yaml
from apparat import fs_changes
from mpremote.main import State  # type: ignore[import-untyped]
from mpremote.transport import TransportError  # type: ignore[import-untyped]
from pydantic import BaseModel
from rich.panel import Panel
from rich.syntax import Syntax
from rich.traceback import Traceback
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Header, Input, Label, RichLog, Switch
from trickkiste.base_tui_app import TuiBaseApp
from trickkiste.logging_helper import apply_common_logging_cli_args
from trickkiste.misc import async_filter

from mpide.utils import (
    async_process_output,
    awatch_duration,
    load_module,
    mpyfy,
    shorten_path,
)

__version__ = "0.2.0.dev3"  # It MUST match the version in pyproject.toml file

STARTUP_HELPTEXT = f"""{'<br>' * 100}
Quick reference
:cat <file>                # plot @file to REPL
:tree                      # dump file system tree to REPL
:cp <src> <dst>            # copy file from host to target
:rm <file, ...>            # remove file(s) on target
:persist                   # persist stuff in /ramdisk to /
:ramdisk                   # set up a RAM-disk at /ramdisk
:bootstrap                 # make all project files available on device
:snippet <name> [<extra>]  # run snippet @name and verbatim @extra if provided
CTRL-A                     # enter raw REPL mode
CTRL-B                     # enter normal REPL mode
CTRL-D                     # soft-reboot
CTRL-E                     # enter paste mode
CTRL-C                     # send keyboard interrupt
CTRL-X                     # quit application
""".replace(
    "<br>", "\n"
)


def log() -> logging.Logger:
    """Returns the logger instance to use here"""
    return logging.getLogger("trickkiste.mpide")


class MpideConfig(BaseModel):
    """Model for shared device/mpide configuration"""

    mpy_cross_path: Path = Path("mpy-cross")
    static_files: Sequence[Path] = []
    dynamic_files: Sequence[Path] = []


class MpIDE(TuiBaseApp):
    """mpide Textual app tailoring all features"""

    MPIDE_DIR = Path(__file__).parent
    CSS_PATH = MPIDE_DIR / "mpide.css"
    PROJECT_CONFIG_FILENAME = "mpide_project.py"

    BINDINGS = [
        Binding("ctrl+x", "app.quit", "Quit", show=True),
        Binding("ctrl+b", "ctrlb"),
        Binding("ctrl+c", "ctrlc"),
        Binding("up", "arrow_up"),
        Binding("down", "arrow_down"),
        Binding("tab", "arrow_up"),
    ]

    class Prompt(Input):
        """Specialization for Input just in order to re-direct ctrl+d"""

        BINDINGS = [
            # overrides pre-defined Binding
            Binding("ctrl+a", "app.ctrla"),
            Binding("ctrl+d", "app.ctrld"),
            Binding("ctrl+e", "app.ctrle"),
            Binding("tab", "app.arrow_down"),
        ]

    class PrintWrapper(io.StringIO):
        """Acts like print() and redirects to log"""

        def __init__(self) -> None:
            self.builtins_print = builtins.print
            super().__init__()

        def __call__(self, *args: object, **kwargs: object) -> None:
            if args == ("no device found",):
                return

            self.builtins_print(  # type: ignore [call-overload]
                *args, **{**kwargs, **{"file": (sio := io.StringIO())}}
            )
            for line in map(str.rstrip, sio.getvalue().split("\n")):
                log().warning("%s", line)

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(
            logger_show_name=12,
            logger_show_funcname=20,
            logger_show_tid=5,
        )
        self.set_log_levels(
            (log(), args.log_level)
        )  # , ("trickkiste", "INFO"), others_level="WARNING")
        self.code_log = RichLog(id="code-log")
        self.code_log.can_focus = False
        self.repl_input = self.Prompt(id="repl-input")
        self.prefix_label = Label("", id="prefix-label")
        self._mqueue: asyncio.Queue[str] = asyncio.Queue()
        self.history: MutableSequence[str] = []
        self.state = State()
        self.history_cursor = 0
        self.project_dir = Path(args.project_dir)
        self.mpide_local_dir = self.project_dir / ".mpide"
        self.mpy_cache_dir = self.mpide_local_dir / "mpy_cache"
        self.title = f"MPIDE - {self.project_dir.name}"
        self.project_config = MpideConfig()
        self.mpy_cross_version = ""

    def compose(self) -> ComposeResult:
        """Set up the UI"""
        yield Header(show_clock=True, id="header")
        with Vertical(id="left-pane"):
            yield self.code_log
            with Horizontal(id="input-pane"):
                yield self.prefix_label
                yield self.repl_input
        with Horizontal(classes="container"):
            yield Label("auto-sync", classes="label")
            yield (
                switch_auto_sync := Switch(
                    id="auto-sync",
                    value=True,
                    tooltip=(
                        "Automatically synchronize files tracked"
                        f" in {self.PROJECT_CONFIG_FILENAME} with device."
                    ),
                )
            )
            switch_auto_sync.can_focus = False
            yield (
                btn_ramdisk := Button(
                    "ramdisk",
                    id="ramdisk",
                    tooltip="Creates and mounts a RAM disk\nsame as :ramdisk",
                )
            )
            btn_ramdisk.can_focus = False
            yield (
                btn_persist := Button(
                    "persist",
                    id="persist",
                    tooltip="Writes volatile stuff to flash\nsame as :persist",
                )
            )
            btn_persist.can_focus = False
            yield (
                btn_bootstrap := Button(
                    "bootstrap",
                    id="bootstrap",
                    tooltip="Flash project files to device\nsame as :bootstrap",
                )
            )
            btn_bootstrap.can_focus = False
        yield from super().compose()

    @awatch_duration()
    async def initialize(self) -> None:
        """UI entry point"""
        # fixme: FileNotFoundError possible when project dir does not exist
        self.mpide_local_dir.mkdir(exist_ok=True)
        self.set_log_levels((log(), "DEBUG"), ("trickkiste", "INFO"), others_level="WARNING")
        self.add_serial_output(STARTUP_HELPTEXT)
        await asyncio.sleep(0.1)  # wait for window resize updates, to avoid ugly logs
        self.add_serial_output("---")
        # redirect `print` messages from mpremote
        builtins.print = self.PrintWrapper()  # type: ignore [assignment]
        self.ensure_connection()
        self.handle_messages()
        with suppress(FileNotFoundError):
            with (self.mpide_local_dir / "command_history.yaml").open(encoding="utf-8") as in_file:
                self.history = yaml.load(in_file, Loader=yaml.Loader)
        await self.load_project_config()
        self.set_status_info()
        if (self.project_dir / self.PROJECT_CONFIG_FILENAME).exists():
            self.watch_fs_changes()
        else:
            self.repl_msg(
                f"[red][bold]Config file {self.PROJECT_CONFIG_FILENAME} not found"
                f" in {self.project_dir}.[/]"
                "\nREPL will still work but auto-syncing and other stuff won't"
            )

    def cleanup(self) -> None:
        """UI shutdown"""
        with (self.mpide_local_dir / "command_history.yaml").open(
            "wt", encoding="utf-8"
        ) as out_file:
            yaml.dump(self.history, out_file)

    @on(Input.Submitted, "#repl-input")
    async def send_repl_cmd(self) -> None:
        """Invoke functionality after pressing Return in input field"""
        await self._mqueue.put(command := self.repl_input.value.rstrip())
        if command:
            if not self.history or self.history[-1] != command:
                self.history.append(command)
        self.repl_input.value = ""
        self.history_cursor = 0

    @on(Button.Pressed, "#ramdisk")
    async def send_cmd_ramdisk(self) -> None:
        """Convenience button for typing :ramdisk"""
        await self._mqueue.put(":ramdisk")

    @on(Button.Pressed, "#persist")
    async def send_cmd_persist(self) -> None:
        """Convenience button for typing :persist"""
        await self._mqueue.put(":persist")

    @on(Button.Pressed, "#bootstrap")
    async def send_cmd_bootstrap(self) -> None:
        """Convenience button for typing :bootstrap"""
        await self._mqueue.put(":bootstrap")

    async def action_ctrla(self) -> None:
        """React on CTRL-A"""
        await self._mqueue.put(":ctrl-a")

    async def action_ctrlb(self) -> None:
        """React on CTRL-B"""
        await self._mqueue.put(":ctrl-b")

    async def action_ctrlc(self) -> None:
        """React on CTRL-C"""
        await self._mqueue.put(":ctrl-c")

    async def action_ctrld(self) -> None:
        """React on CTRL-D"""
        await self._mqueue.put(":ctrl-d")

    async def action_ctrle(self) -> None:
        """React on CTRL-E"""
        await self._mqueue.put(":ctrl-e")

    async def action_arrow_up(self) -> None:
        """React on UP"""
        self.history_cursor = max(self.history_cursor - 1, -len(self.history))
        with suppress(IndexError):
            self.repl_input.value = self.history[self.history_cursor]

    async def action_arrow_down(self) -> None:
        """React on DOWN"""
        self.history_cursor = min(self.history_cursor + 1, 0)
        with suppress(IndexError):
            self.repl_input.value = self.history[self.history_cursor] if self.history_cursor else ""

    @work(exit_on_error=True)
    async def ensure_connection(self) -> None:
        """Continuously tries to connect"""
        show_message = True
        while True:
            if self.state.transport:
                await asyncio.sleep(1)
                continue
            try:
                if show_message:
                    log().info("connect..")
                self.state.ensure_friendly_repl()
                self.state.did_action()
                self.state.transport.serial.write(b"\r\n")
                self.print_serial()
                self.set_status_info()
            except SystemExit:
                if show_message:
                    log().error("mpremote could not connect to any device")
                self.abort_connection()
            except Exception as exc:  # pylint: disable=broad-except
                log().error("%s", exc)
                self.repl_exc()
            await asyncio.sleep(2)
            show_message = False

    @contextmanager
    def raw_repl(self) -> Iterator[None]:
        """Convenience decorator for entering raw repl"""
        state_before = self.state.transport.in_raw_repl
        assert not state_before
        try:
            if not state_before:
                log().debug("enter raw REPL")
                self.state.transport.enter_raw_repl(soft_reset=False)
                assert self.state.transport.in_raw_repl
            yield
        finally:
            assert self.state.transport.in_raw_repl
            if not state_before:
                log().debug("leave raw REPL")
                self.state.transport.exit_raw_repl()
                assert not self.state.transport.in_raw_repl

    @work(exit_on_error=True)
    async def repl_msg(self, msg: str) -> None:
        """Write a flashy message supporting markups to the REPL"""
        self.code_log.write(Panel(msg))
        await asyncio.sleep(1)

    def repl_exc(self) -> None:
        """Write a flashy message supporting markups to the REPL"""
        self.code_log.write(Panel(Traceback()))

    @work(exit_on_error=True)
    async def handle_messages(self) -> None:
        """Reads messages from a queue and operates on serial. This is the only function
        allowed to write to serial to avoid conflicts (thus the queue)"""
        while True:
            element = await self._mqueue.get()
            log().debug("got element %s", element)
            try:
                if not self.state or not self.state.transport:
                    self.repl_msg("[yellow bold]no device connected")
                elif self.state.transport.in_raw_repl:
                    assert False, "should not happen"
                elif element == ":ctrl-a":
                    self.repl_msg("send CTRL-A (enter raw REPL) to device..")
                    self.state.transport.serial.write(b"\r\x01")
                elif element == ":ctrl-b":
                    self.repl_msg("send CTRL-B (leave raw REPL) to device..")
                    self.state.transport.serial.write(b"\r\x02")
                elif element == ":ctrl-d":
                    self.repl_msg("send CTRL-D (soft-reboot) to device..")
                    self.state.transport.write_ctrl_d(self.add_serial_output)
                elif element == ":ctrl-c":
                    self.state.transport.serial.write(b"\x03")
                elif element == ":ctrl-e":
                    self.repl_msg("send CTRL-E (paste mode) to device..")
                    self.state.transport.serial.write(b"\r\x05")
                elif element == ":ramdisk":
                    self.run_snippet("setup_ramdisk")
                elif element == ":bootstrap":
                    await self.bootstrap_device()
                elif element == ":persist":
                    self.run_snippet("persist")
                elif element == ":tree":
                    self.run_snippet("fs_ops", "print(tree)")
                elif element.startswith(":snippet "):
                    _, name, *rest = element.split(maxsplit=2)
                    self.run_snippet(name, rest[0] if rest else "")
                elif element.startswith(":cp "):
                    _, source_raw, target_raw = element.split()
                    await self.copy_files(Path(source_raw), Path(target_raw))
                elif element.startswith(":cat "):
                    _, *paths = element.split()
                    log().debug("cat %s", paths)
                    self.run_snippet("fs_ops", f"target_cat({paths})")
                elif element.startswith(":rm "):
                    _, *paths = element.split()
                    self.run_snippet("fs_ops", f"target_rm_files({paths})")
                else:
                    self.state.transport.serial.write(f"{element}\r\n".encode())
            except TransportError:
                self.repl_msg("[red bold]caught TransportError[/]")
                self.repl_exc()
            except OSError as exc:
                log().error("could not write to serial: %s", exc)
                self.abort_connection()
                # self.repl_msg("[red bold]serial communication failed - reset connection")
                self.repl_exc()
            except Exception as exc:  # pylint: disable=broad-except
                log().error("could not write: %r", exc)
                self.repl_exc()

    def run_snippet(self, name: str, extra: str = "") -> None:
        """Run snippet contained in file located at @path"""
        log().debug("try to execute snippet %s", name)

        if not (path := self.local_path(f"{name}.py")):
            self.repl_msg(f"[red bold] no file {name}.py found")
            return

        with path.open() as file:
            snippet = "\n".join(filter(lambda line: line.rstrip(), file.readlines() + [extra]))

        with self.raw_repl():
            try:
                # fixme - syntax error keeps us in raw repl
                # - fix error handling
                # - don't allow faulty snippets in the first place
                self.state.transport.exec_raw_no_follow(snippet.encode())
                log().debug("executed %d lines", len(snippet.split("\n")))
            except TransportError as exc:
                self.add_serial_output(f"Error: {exc}")

    async def copy_files(self, *sources_destination: Path) -> None:
        """Copy files or directories from host to target (for now)"""

        async def copy_file(source_raw: Path, target_raw: Path) -> None:
            log().debug("copy_file(%s, %s)", shorten_path(source_raw), target_raw)
            if source_raw.suffix == ".py" and target_raw.suffix == ".mpy":
                source_path = await self.precompiled_from(Path(source_raw))
            else:
                source_path = Path(source_raw)

            # fixme: skip identical files - keep a dict
            # (source, target) -> hash
            # and check if copy_cache.get((source, target)==hash

            # self.state.transport.fs_cp(source, target)
            log().debug("cp %s %s", shorten_path(source_path), target_raw)

            with open(source_path, "rb") as in_file:
                source_file_content = in_file.read()

            # create parent directories if needed but
            # don't create '/ramdisk' automatically
            if target_raw.is_relative_to("/ramdisk") or target_raw.is_relative_to("ramdisk"):
                # fixme: make independent from mpide_project (might not be available)
                self.run_snippet("setup_ramdisk")
                await asyncio.sleep(1)

            try:
                with self.raw_repl():
                    self.state.transport.exec(f"import os\nos.mkdir('{target_raw.parent}')")
            except TransportError as exc:
                if "EEXIST" in str(exc):
                    pass
                else:
                    raise

            with self.raw_repl():
                self.state.transport.fs_writefile(target_raw, source_file_content)
                await asyncio.sleep(.2)

            self.repl_msg(
                "[blue]copied"
                f" <project>/[bold]{shorten_path(source_path)}[/]"
                f" to <device>/[bold]{target_raw}[/]"
            )

        *raw_srcs, raw_dst = sources_destination
        for raw_src in raw_srcs:
            src_path = raw_src if raw_src.is_absolute() else self.project_dir / raw_src
            if src_path.is_dir():
                # if not dst.is_dir():
                #    raise RuntimeError("Destination target for {src} has to be a directory")
                for file_path in src_path.rglob("*"):
                    dst_path = raw_dst / file_path.relative_to(src_path.parent)
                    if dst_path.suffix == ".py":
                        dst_path = dst_path.parent / f"{dst_path.stem}.mpy"

                    await copy_file(file_path, dst_path)
            elif src_path.is_file():
                await copy_file(src_path, raw_dst)
            else:
                raise RuntimeError(
                    f"Source {raw_src} is neither a file nor a directory in {Path.cwd()}"
                )

    async def bootstrap_device(self) -> None:
        """Make sure all tracked project files are present and up to date on the target device"""

        def local_path_from(path: Path) -> Path | None:
            if not (target_path := self.local_path(path)):
                log().warning("There is no local source file for %s", path)
                return None
            return target_path

        log().debug("bootstap device by copying all of")
        log().debug("static:  %s", list(map(str, self.project_config.static_files)))
        log().debug("dynamic: %s", list(map(str, self.project_config.dynamic_files)))
        paths = list(
            (src_path, target_path.relative_to("mpide") if target_path.is_relative_to("mpide") else target_path)
            for path_list in (self.project_config.static_files, self.project_config.dynamic_files)
            for target_path in path_list
            if (src_path := local_path_from(target_path))
        )
        await self.update_target_files(paths)

    @work(exit_on_error=True)
    async def print_serial(self) -> None:
        """Reads data from serial and adds it to the output"""
        buffer = b""
        while True:
            try:
                # busy wait for data - we have to go away from mpremote to make this async..
                await asyncio.sleep(0.1)
                if not (num_bytes := self.state.transport.serial.inWaiting()):
                    if buffer:
                        self.add_serial_output(buffer.decode(errors="replace"))
                        buffer = b""
                    continue
                if (dev_data_in := self.state.transport.serial.read(num_bytes)) is not None:
                    buffer += dev_data_in
                    # todo: yield completed lines
            except AttributeError:
                # self.state.transport has already been removed
                return
            except OSError as exc:
                log().error("could not read: %s", exc)
                self.abort_connection()
                return

    def abort_connection(self) -> None:
        """Reset connection and show flashy connection state"""
        self.state = State()
        self.set_status_info()

    def set_status_info(self) -> None:
        """Sets text and color of status bar"""
        connected_device = (
            f"connected to {self.state.transport.device_name}" if self.state.transport else ""
        )
        self.update_status_bar(
            # PID / process.cpu_percent() / tasks / System CPU
            # idf version
            f" Status: {connected_device or 'not connected'}"
            f" │ mpide v{__version__}"
            f" │ mpy-cross: {self.mpy_cross_version}"
        )
        self._footer_label.styles.background = "#224422" if connected_device else "#442222"
        self.query_one(Header).styles.background = "#224422" if connected_device else "#442222"

    def add_serial_output(self, data: str) -> None:
        """Append stuff to the REPL log"""
        if data == "---":
            self.code_log.write("─" * (self.code_log.size.width - 3))
            return
        *head, tail = data.rsplit("\n", maxsplit=1)
        self.prefix_label.update(tail)
        if head:
            self.code_log.write(
                Syntax(
                    head[0],
                    "python",
                    indent_guides=True,
                    background_color="#222222",
                    word_wrap=True,
                )
            )

    async def load_project_config(self) -> None:
        """Returns held up to date instance of project configuration"""
        with suppress(FileNotFoundError):
            if self.project_dir.as_posix() not in sys.path:
                sys.path.append(
                    self.project_dir.as_posix()
                )  # needed for loading relative stuff inside mpide_project.py
            try:
                if (
                    new_config := MpideConfig.model_validate(
                        load_module(self.project_dir / self.PROJECT_CONFIG_FILENAME).config
                    )
                ) == self.project_config:
                    return
                self.project_config = new_config
                self.mpy_cross_version = "invalid"
                try:
                    stdout, _stderr, _result = await async_process_output(
                        f"{new_config.mpy_cross_path.expanduser()} --version"
                    )
                    if match := re.match(
                        r"^MicroPython ([a-z0-9\-\.]*) on (.*);"
                        r" mpy-cross emitting mpy v([a-z0-9\-\.]*)$",
                        stdout[0],
                    ):

                        self.mpy_cross_version = " ".join(match.groups())
                    else:
                        self.mpy_cross_version = stdout[0]
                except FileNotFoundError:
                    log().warning(
                        "mpy-cross compiler (`%s`) could not be executed",
                        new_config.mpy_cross_path,
                    )
                    self.mpy_cross_version = "not-found"
                self.set_status_info()
                self.repl_msg("[blue](Re)loaded project configuration[/]")
                return
            except Exception as exc:  # pylint: disable=broad-except
                log().error("could not load %s: %s", self.PROJECT_CONFIG_FILENAME, exc)
                self.repl_msg(
                    f"[red bold]{self.PROJECT_CONFIG_FILENAME} cannot be loaded[/]"
                    "\nconsider all other issues a result and fix your config first."
                )
        self.project_config = MpideConfig()

    def target_path(self, source_path: Path) -> Path | None:
        """Returns the device counterpart of given @source_path as defined in project config,
        None if there is no mapping."""
        rel_source_path = source_path.relative_to(self.project_dir)
        for target_base, file_list in (
            ("/", self.project_config.static_files),
            ("/ramdisk", self.project_config.dynamic_files),
        ):
            for path in file_list:
                if (
                    path.parent == rel_source_path.parent
                    and path.stem == rel_source_path.stem
                    and (
                        path.suffix == rel_source_path.suffix
                        or (path.suffix == ".mpy" and rel_source_path.suffix == ".py")
                    )
                ):
                    return Path(target_base) / path
        # todo: add builtins
        log().debug("%s not tracked", rel_source_path)
        return None

    def local_path(self, target_path: Path | str) -> Path | None:
        """Returns the local counterpart for a target path if it exists, otherwise None"""
        _raw = raw.parent / f"{raw.stem}.py" if (raw := Path(target_path)).suffix == ".mpy" else raw
        if (path := self.project_dir / _raw).exists():
            return path
        if (path := self.MPIDE_DIR / "target" / _raw).exists():
            return path
        if (path := self.MPIDE_DIR / "target" / "mpide" / _raw).exists():
            return path
        return None

    async def precompiled_from(self, path: Path) -> Path:
        """Returns path to precompiled result from @path"""
        mpy_cross = self.project_config.mpy_cross_path
        log().debug("mpy-cross: '%s'", mpy_cross)
        result = await mpyfy(path, mpy_cross.expanduser(), self.mpy_cache_dir)
        self.repl_msg(
            f"[blue]precompiled [bold]{result.relative_to(self.mpy_cache_dir)}[/]"
            f" from [bold]{shorten_path(path)}[/]"
        )
        return result

    async def update_target_files(self, paths: Iterable[tuple[Path, Path]]) -> None:
        """Copy a bunch of local files to the target, eventually precompiling them first"""

        try:
            paths = list(paths)  # fixme

            self.repl_msg("\n".join(str(local_path) for local_path, _ in paths))
            copy_instructions = [
                (
                    (await self.precompiled_from(local_path))
                    if local_path.suffix == ".py" and target_path.suffix == ".mpy"
                    else local_path,
                    target_path,
                )
                for local_path, target_path in paths
            ]
            if modules := [repr(target_path.as_posix()) for _, target_path in copy_instructions]:
                await self._mqueue.put(
                    f":snippet unload_module unload_module({', '.join(modules)})"
                )

            # fixme: no clue why this is needed - without it, the snippet won't be
            # executed..
            await asyncio.sleep(0.5)

            for local_path, target_path in copy_instructions:
                await self._mqueue.put(f":cp {local_path} {target_path}")

        except FileNotFoundError as exc:
            log().error("%s", exc)
        except Exception as exc:  # pylint: disable=broad-except
            log().error("%s", exc)
            self.repl_exc()

    @work(exit_on_error=True)
    async def watch_fs_changes(self) -> None:
        """Watch out for changes on filesystem and automatically update device"""
        def ignore_pattern(path: Path) -> bool:
            if re.match(r"^(~.*|.*~|.*\.swp)$", path.name):
                log().debug("prune %s", path.name)
                return False
            return True

        async for src_paths in async_filter(
            ignore_pattern,
            fs_changes(
                self.project_dir,
                min_interval=1,
                additional_ignore_pattern=(
                    "/.mpide", "/dev", "/micropython",
                    "/.cache",
                    "/.espressif",
                    "/esp-idf",
                    "/st7789_mpy",
                ),
                bucket_size=100,
            ),
        ):
            # todo: remove duplicates
            # todo: sort config_local > mpide_project to top

            # since there's no trivial way to know if `mpide_project.py` is affected by any
            # change we (re)load it unconditionally. Also changes to `mpide_project.py` or any
            # of its dependencies might affect the following filtering, so we shouldn't do it
            # before having reloaded the project config
            await self.load_project_config()

            if not self.query_one("#auto-sync", Switch).value:
                log().debug("auto-synchronization with device deactivated")
                continue

            await self.update_target_files(
                (path, target_path) for path in src_paths if (target_path := self.target_path(path))
            )


def main() -> None:
    """Entry point for mpide application"""
    parser = apply_common_logging_cli_args(argparse.ArgumentParser())
    parser.add_argument("--build-micropython", action="store_true")
    parser.add_argument("--serial-port")
    parser.add_argument("--baudrate", "-b", type=int)
    # parser.add_argument("--mpy-cross", type=Path)
    # parser.add_argument("--cache-dir", type=Path)
    # parser.add_argument("--dest-dir", type=Path, default=Path("/"))

    # todo: check for existence
    parser.add_argument(
        "project_dir", type=lambda p: Path(p).resolve().absolute(), nargs="?", default="."
    )
    if (args := parser.parse_args()).build_micropython:
        build_micropython_path = (Path(__file__).parent / "build_micropython").resolve()
        print(f"Run {build_micropython_path / 'run-containerized'} /opt/build-micropython.sh")
        return
    MpIDE(args).execute()



if __name__ == "__main__":
    main()

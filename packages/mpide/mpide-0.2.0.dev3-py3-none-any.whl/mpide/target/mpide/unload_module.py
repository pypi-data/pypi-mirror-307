#!/usr/bin/env python3

"""Provides functionality to unload modules"""

import sys


def unload_module(path_or_name: str, prefix: str = "/ramdisk") -> None:
    """Searches and unloads module with provided name or file path.
    Not exactly sophisticated, but works for now..
    Implementation found here:
        https://forum.micropython.org/viewtopic.php?t=413&start=20
    """

    def without_prefix(string: str, prefix: str) -> str:
        return string[len(prefix) :] if string.startswith(prefix) else string

    # hacky: also unload project config when config_local.py gets changed
    # better approach would track dependencies instead and unload 'parent' modules
    # when a dependency changed
    print(f"ul {path_or_name}..")

    if "config_local." in path_or_name:
        unload_module("mpide_project")

    for name, mod in sys.modules.items():
        if not (
            name == path_or_name
            or without_prefix(mod.__file__ or "", prefix).lstrip("/").replace(".mpy", ".py")
            == without_prefix(path_or_name, prefix).lstrip("/").replace(".mpy", ".py")
        ):
            continue
        print(f"ul {path_or_name} found")
        try:
            loaded_module = __import__(name)
            del loaded_module
        except ImportError:
            pass
        try:
            del sys.modules[name]
        except KeyError:
            pass
        return
    print(f"ul {path_or_name} done")

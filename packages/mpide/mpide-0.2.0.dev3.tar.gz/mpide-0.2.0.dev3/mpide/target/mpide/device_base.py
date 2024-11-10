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

"""Base class for common device interaction"""

# pylint: disable=import-outside-toplevel
# pylint: disable=import-error
# pylint: disable=fixme

#from abc import ABC, abstractmethod
ABC = object

class DisplayBase(ABC):
    """Basic interaction with built in displays"""

    #@abstractmethod
    def __init__(self) -> None:
        ...

    #@abstractmethod
    def println(self, line: int, text: str, color: int | str | None) -> None:
        """Print @text on given @line in given @color"""

    #@abstractmethod
    def fill(self, color: int | str | None = None) -> None:
        """Fill the screen in given @color"""

    #@abstractmethod
    def set_bg(self, color: int | str | None) -> None:
        """Sets background color to @color"""

    #@abstractmethod
    def rotation(self, rotation: int) -> None:
        """Sets rotation to @rotation"""


class DeviceBase(ABC):
    """Base class for common device interaction"""

    _instance = None
    _context = 0
    _fully_initialized = False

    def __new__(cls, full_init: bool = False) -> "DeviceBase":
        if cls._instance is None:
            cls._instance = super(DeviceBase, cls).__new__(cls)
            cls._instance.partial_init()
        if full_init and not cls._fully_initialized:
            cls._instance.full_init()

        return cls._instance

    #@abstractmethod
    def partial_init(self) -> None:
        """Only initialize the most basic parts"""
        print("DeviceBase.partial_init()")

    #@abstractmethod
    def full_init(self) -> None:
        """Initialize the more risky components"""
        print("DeviceBase.full_init()")
        self._fully_initialized = True

    def _deinit(self) -> None:
        print("DeviceBase._deinit()")
        self._fully_initialized = False

    def __enter__(self) -> "DeviceBase":
        self._context += 1
        return self

    def __exit__(self, *_: object) -> None:
        self._context -= 1
        if not self._context:
            assert self._instance
            self._deinit()
            self.__class__._instance = None

    #@abstractmethod
    def acc(self) -> tuple[float, float, float] | None:
        """Returns the acc sensor values"""
        return None

    #@abstractmethod
    def println(self, line: int, text: str, color: int | str | None = None) -> None:
        """Print @text on given @line in given @color on self.device"""
        print(line, text)

    #@abstractmethod
    def print(self, *args: object) -> None:
        """Print @text on self.device"""
        print(*args)

    def usb_connected(self) -> bool:
        """Returns whether or not an USB cable is connected (if possible)"""
        return True

    def connect_wifi(self, credentials: list[dict[str, str]]) -> str | None:
        """Connects to provided WiFi hotspot"""
        # todo: set hostname
        import time

        import network  # type: ignore[import-not-found]

        status_names = {
            network.STAT_IDLE: "idle",
            network.STAT_CONNECTING: "connecting",
            network.STAT_WRONG_PASSWORD: "wrong password",
            network.STAT_NO_AP_FOUND: "no AP found",
            network.STAT_GOT_IP: "got IP",
            network.STAT_BEACON_TIMEOUT: "beacon timeout",
            network.STAT_ASSOC_FAIL: "assoc fail",
            network.STAT_HANDSHAKE_TIMEOUT: "handshake timeout",
        }

        wlan = network.WLAN(network.WLAN.IF_STA)

        def _connect() -> None:
            if wlan.isconnected():
                print(f"WiFi already connected: {wlan.ifconfig()}")
                return

            wlan.active(False)
            wlan.active(True)
            print("MAC:", ":".join((map(lambda i: f"{i:.2X}", wlan.config("mac")))))
            print(f"Configured SSIDs: {', '.join(e['ssid'] for e in credentials)}")
            for _i1 in range(3):
                print("Scanned SSIDs:")
                scanned = {e[0].decode(): (e[2], e[3], e[4]) for e in wlan.scan()}
                for ssid, (channel, rssi, security) in sorted(
                    scanned.items(), key=lambda x: x[1][1], reverse=True
                ):
                    print(f"   '{ssid}' (ch={channel}) strength={rssi} {security=}")
                if not (
                    matching_ssids := [
                        (cred["ssid"], cred["pw"])
                        for cred in credentials
                        if cred["ssid"] in scanned
                    ]
                ):
                    print("No matching SSIDs found!")

                for ssid, passphrase in matching_ssids:
                    print(f"Try to connect to '{ssid}'...")
                    last_status = wlan.status()
                    wlan.connect(ssid, passphrase)
                    for _i2 in range(10):
                        status = wlan.status()
                        if status != last_status:
                            print(
                                f"status changed: {status_names.get(last_status)} ({last_status})"
                                + f" -> {status_names.get(status)} ({status})"
                            )
                        if status in {network.STAT_IDLE, network.STAT_CONNECTING}:
                            time.sleep(0.3)
                            continue
                        return

        _connect()
        return str(wlan.ifconfig()[0]) if wlan.isconnected() else None

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

"""Stuff needed on both target and development host"""

# pylint: disable=import-outside-toplevel


def sha1_sum(data: bytes | str) -> str:
    """Returns the sha1 hex representation of @data"""
    import binascii
    import hashlib

    return binascii.hexlify(
        hashlib.sha1(
            data if isinstance(data, bytes) else data.encode(),
        ).digest()
    ).decode()


def file_checksum(path: str) -> str:
    """Returns the sha1 hex representation file content referenced by @path"""
    try:
        with open(path, "rb") as in_file:
            return sha1_sum(in_file.read())
    except OSError:
        return ""

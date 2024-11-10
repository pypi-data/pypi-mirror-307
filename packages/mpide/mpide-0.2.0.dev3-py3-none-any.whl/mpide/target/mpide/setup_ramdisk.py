#!/usr/bin/env python3

"""Sets up a RAM-disk"""
# pylint: disable=import-error
# pylint: disable=fixme

import os
import sys

from mpide_project import config  # type: ignore[import-not-found]


class RAMBlockDev:
    """
    Taken from https://docs.micropython.org/en/latest/reference/filesystem.html
    """

    def __init__(self, block_size: int, num_blocks: int) -> None:
        self.block_size = block_size
        self.data = bytearray(block_size * num_blocks)

    def readblocks(self, block_num: int, buf: bytearray, offset: int = 0) -> None:
        """Read @block_num blocks into @buf"""
        addr = block_num * self.block_size + offset
        # todo: there is probably a more efficient way to copy bytes with offset..
        for i in range(len(buf)):  # pylint: disable=consider-using-enumerate
            buf[i] = self.data[addr + i]

    def writeblocks(self, block_num: int, buf: bytearray, offset: int | None = None) -> None:
        """Write @block_num blocks into @buf"""
        if offset is None:
            # do erase, then write
            for i in range(len(buf) // self.block_size):
                self.ioctl(6, block_num + i)
            offset = 0
        addr = block_num * self.block_size + offset
        for i, value in enumerate(buf):
            self.data[addr + i] = value

    def ioctl(self, opcode: int, _arg: object) -> int | None:
        """ioctl"""
        if opcode == 4:  # block count
            return len(self.data) // self.block_size
        if opcode == 5:  # block size
            return self.block_size
        if opcode == 6:  # block erase
            return 0
        # print(f"WARNING: RAMBlockDev.ioctl: unknown opcode {opcode} requested", file=sys.stderr)
        return None


def setup_ramfs(mountpoint: str, block_size: int, num_blocks: int) -> None:
    """Setup a RAM-FS we can use for storing files without wearing off the
    flash memory
    """
    if mountpoint.split("/")[-1] in os.listdir():
        print(f"{mountpoint} already exists")
    elif sys.platform == "linux":
        os.mkdir(os.path.join(os.getcwd(), mountpoint.split("/")[-1]))
    else:
        print(f"create RAM disk i{block_size=}*{num_blocks=} = {block_size * num_blocks / 1024}kib")
        bdev = RAMBlockDev(block_size, num_blocks)
        os.VfsLfs2.mkfs(bdev)  # pylint: disable=no-member
        os.mount(bdev, mountpoint)  # pylint: disable=no-member

    if mountpoint not in sys.path:
        print(f"insert {mountpoint}")
        sys.path.insert(0, mountpoint)
    else:
        print(f"{mountpoint} already in sys.path")


if __name__ == "__main__":
    rd_config = config["ramdisk"]
    setup_ramfs(rd_config["mountpoint"], rd_config["block_size"], rd_config["num_blocks"])

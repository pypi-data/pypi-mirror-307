#!/usr/bin/env python3

"""provides a couple of FS operations"""
# pylint: disable=import-error
# pylint: disable=fixme

import os

def target_cat(paths: list[str]) -> None:
    """Print out contents of files specified by @paths"""
    for path in os.listdir() if paths == ["*"] else paths:
        print(path)
        with open(path, encoding="utf-8") as text_file:
            print(text_file.read())


def target_rm_files(paths: list[str]) -> None:
    """Remove files specified by @paths"""
    for path in os.listdir() if paths == ["*"] else paths:
        print(f"remove {path}")
        os.remove(path)


class FsTreeLister:
    """Makes instances print out a file system tree on target when __repr__ is called"""

    def __repr__(self) -> str:
        # pylint: disable=no-member

        print("files on /:")
        for name, entry_type, inode, *date in os.ilistdir():  # type: ignore[attr-defined]
            print(name, entry_type, inode, date)
            if entry_type == 0x4000:
                print(os.statvfs(name))
        return "\n".join(map(str, os.ilistdir()))  # type: ignore[attr-defined]

    def __call__(self, *args: object, **kwargs: object) -> None:
        print("called")


tree = FsTreeLister()

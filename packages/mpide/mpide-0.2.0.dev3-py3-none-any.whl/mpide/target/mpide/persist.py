"""Write volatile stuff from RAM disk to flash FS"""
import os

for path in os.listdir("/ramdisk"):
    print(path)
    # we can't just os.rename here because we're on different
    # filesystems
    with open(f"/ramdisk/{path}", "rb") as in_file:
        with open(f"/{path}", "wb") as out_file:
            out_file.write(in_file.read())
    os.remove(f"/ramdisk/{path}")
# os.sync()

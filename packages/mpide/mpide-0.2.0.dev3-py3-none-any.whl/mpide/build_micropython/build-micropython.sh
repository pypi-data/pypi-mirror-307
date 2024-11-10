#!/usr/bin/bash
# see https://github.com/russhughes/st7789_mpy/

# - l libusb-1.0-0-dev
# - 4.4.7
# - ../../../st7789_mpy

set -e

if [ ! -d esp-idf ]; then
    git clone -b v5.0.4 --recursive https://github.com/espressif/esp-idf.git
fi

cd esp-idf
git checkout v5.0.4
git submodule update --init --recursive

./install.sh

# shellcheck disable=SC1091
source export.sh

cd -

if [ ! -d micropython ]; then
    git clone https://github.com/micropython/micropython.git
fi

if [ ! -d st7789_mpy ]; then
    git clone https://github.com/russhughes/st7789_mpy.git
fi

(cd micropython/
    #git checkout v1.22
    git submodule update --init
    (cd mpy-cross/
        make -j8
    )
    (cd ports/esp32

        cp ../../../st7789_mpy/fonts/bitmap/vga1_8x8.py modules
        #cp ../../../st7789_mpy/fonts/bitmap/vga1_16x16.py modules
        #cp ../../../st7789_mpy/fonts/truetype/NotoSans_32.py modules
        #cp ../../../st7789_mpy/fonts/vector/scripts.py modules

        make -j8 \
            USER_C_MODULES=../../../../st7789_mpy/st7789/micropython.cmake \
            FROZEN_MANIFEST="" \
            FROZEN_MPY_DIR="$(pwd)/modules" \
            BOARD=ESP32_GENERIC
        make -j8 \
            USER_C_MODULES=../../../../st7789_mpy/st7789/micropython.cmake \
            FROZEN_MANIFEST="" \
            FROZEN_MPY_DIR="$(pwd)/modules" \
            BOARD=ESP32_GENERIC_S3 \
            BOARD_VARIANT=FLASH_4M
    )
    (cd ports/unix
        make -j8
    )
)
echo "$(realpath micropython/mpy-cross/build/mpy-cross)"
micropython/ports/unix/build-standard/micropython -c "import sys; print(sys.version)"
micropython/mpy-cross/build/mpy-cross --version
find micropython/ -name firmware.bin

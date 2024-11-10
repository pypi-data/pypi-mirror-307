FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update \
    && apt-get -y install \
    build-essential \
    libusb-1.0-0-dev \
    libffi-dev \
    git pkg-config \
    cmake \
    virtualenv \
    python3-pip \
    python3-virtualenv \
    python3-venv \
    tig \
    vim
COPY build-micropython.sh /opt/


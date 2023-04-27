FROM ubuntu:16.04
ENV DEBIAN_FRONTEND=noninteractive
RUN dpkg --add-architecture i686
RUN apt update
RUN apt-get install -y pkg-config scons gcc-mingw-w64
ENV MINGW64_PREFIX=i686-w64-mingw32-
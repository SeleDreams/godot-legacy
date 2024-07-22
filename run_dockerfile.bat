docker build ./docker/windows-build --tag godot:windows
docker run -it --rm -v .:/src:rw -w /src godot:windows scons platform=windows mingw64_for_32=yes -j7 tools=yes target=release_debug
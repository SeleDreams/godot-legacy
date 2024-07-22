![GODOT](/logo.png)

# Godot Legacy

This is the repository of the Godot legacy project.
This project aims to maintain the 1.0 version of godot in order to ensure it stays easy to build.

The goal is to be able to port it to various retro consoles such as the Nintendo 3DS, the Dreamcast etc thanks to its fixed pipeline.

## How to build

### Building for Windows

You will need to have Scons installed and in your path as well as either Visual Studio, either MinGW.

For Visual Studio, open the visual studio command prompt and go to the project's repository. then type `scons platform=windows bits=64 -j7 tools=yes target=release_debug` in order to build the editor for Windows 64-bit (adjust the -j depending on the number of cores on your CPU).

For MinGW, just type the same command from any command line with mingw in your PATH.

## Original readme

### The Engine

Godot is a fully featured, open source, MIT licensed, game engine. It focuses on having great tools, and a visual oriented workflow that can export to PC, Mobile and Web platforms with no hassle.
The editor, language and APIs are feature rich, yet simple to learn, allowing you to become productive in a matter of hours.

### About

Godot has been developed by Juan Linietsky and Ariel Manzur for several years, and was born as an in-house engine, used to publish several work-for-hire titles.
Development is sponsored by OKAM Studio (http://www.okamstudio.com).

### Documentation

Documentation has been moved to the [GitHub Wiki](https://github.com/SeleDreams/godot-legacy/wiki).

### Binary Downloads, Community, etc.

Binary downloads, community, etc. can be found in Godot homepage:

http://www.godotengine.org

### Compiling from Source

Compilation instructions for every platform can be found in the Wiki:
https://github.com/SeleDreams/godot-legacy/wiki/advanced

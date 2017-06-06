# EyeTracker

An application for selecting  images from a grid using [pupil labs](https://pupil-labs.com/) eyetracking hardware.
The application is 100% working on Ubuntu 16.04. Windows and MacOS are theoretically also supported with additional steps.

## Dependencies

Eyetracker requires the same dependencies as described in https://docs.pupil-labs.com/#developer-setup. Follow the dependency setup for OS of your choosing. You also need to install [PyQt](5https://sourceforge.net/projects/pyqt/) for our GUI. Easiest way to do so is using pip:
```pip3 install pyqt5```.

## Launching the application

### From source

The application can be launched directly from source code (provided all dependencies are installed) by launching [/src/capture/main.py](../src/capture/main.py) as administrator. (using command ```python main.py``` from elevated command prompt on Windows or ```sudo python3 main.py``` on Ubuntu).

### From the build

On Ubuntu you can also launch from the prebuilt [/build/exe.linux-x86_64-3.5/main](./build/exe.linux-x86_64-3.5/main). The application still needs to be launched with administrator privileges.

## Building the application

The application can be built from the root ofthe repository using ```python setup.py build```.

## Source structure

Eyetracker source code is structured into multiple source subfolders:
* [src/capture](./src/capture) for the pupil capture app running in background,
* [src/eyetracker](./src/exetracker) for the main eyetracker algorithm and GUI,
* [src/shared_cpp](./src/shared_cpp) for C++ background modules,
* [src/shared_modules](./src/shared_modules) for shared modules used by pupil.

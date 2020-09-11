# Setup Guide

## Installation

### python

First you must have python 3.6 installed on your system. I recommend doing this with some virtual environment, I like using `pyenv`. Next, install these dependencies:

* `python -m pip install future`
* `python -m pip install pillow`

### java

You will need `OpenJDK 8` as well. Install this based on your operating system. 

### malmo

Now go to [this page](https://github.com/microsoft/malmo/releases/tag/0.37.0) and download the `Python 3.6` version for your operating system. If you are on linux and your distro isn't listed, the Ubuntu version might work for you. I tested this on Manjaro, and the Ubuntu verson works fine. After downloading and extracting the folder, rename it to `malmo`. This is so the `.gitignore` file will set that folder to be ignored, as we do not want it in our version control. Now go to `malmo/Python_Examples/` and copy `MalmoPython.so` and `malmoutils.py` to the root directory of the repository, these files are also going to be ignored in version control.

## Running test.py

### Starting Minecraft

To start the client, go to `malmo/Minecraft` and run `launchClient.sh` (`launchClient.bat` on Windows). This will open a Minecraft client. Now in this client click `Mods`, `Microsoft Malmo Mod`, and set `debugDisplayLevel` to `Show all diagnostics` so that you can see any error popping up.

### test.py

Open another terminal, and run `python test.py`, this should cause the Minecraft client to begin the test. In the Minecraft window, press `Enter` to take control of the agent. If you look around at different blocks, the data for the block in your sight will be printed to the terminal where `test.py` is running. If you step on the diamond block in the middle of the structure, or if the time runs out, the test will end.

### Other Example

The `Python_Examples` folder has many more examples in it that you can run. There is also a Tutorial PDF in that folder that explains the examples.

# Things to work on

* Extend the observer to see all the blocks in the agent's view.

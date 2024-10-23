# FL Studio Migration Helper

## What it does:
- This program searches for installed FL Studio plugins and lists their directories.
- I created this tool to assist in installing all of my plugins from an old PC and making sure my song files work.

## How to use it:
Run `main.py` in your plugin database directory, typically located at `C:/Users/<you>/Documents/Image-Line/FL Studio/Presets/Plugin database`

### Optional Arguments
#### -i --input:
- Choose the root directory
- Without this, it will run in the folder `main.py` is in

#### -o --output:
- Choose the output filepath
- Without this, it will write to `fl_plugins.json` in the folder `main.py` is run from

#### -v --verbose:
- Prints more stuff to the commandline

#### -s --slashes:
- Modifies output file URLs to forward, backward, or double backward slashes

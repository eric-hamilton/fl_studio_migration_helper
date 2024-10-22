# FL Studio Migration Helper

## What it does:
- This program searches for installed FL Studio plugins and lists their directories.
- I created this tool to assist in installing all of my plugins from an old PC and making sure my files work.

## How to use it:
Run `main.py` in your plugin database directory, typically located at `C:/Users/<you>/Documents/Image-Line/FL Studio/Presets/Plugin database`

### Optional Arguments
#### -i --input:
- Choose the root directory
- Without this, it will run in the folder `main.py` is in

#### -o --output:
- Choose the output filepath
- Without this, it will write to `fl_plugin_paths.txt` in the folder `main.py` is run from

#### -v --verbose:
- Prints more stuff to the commandline

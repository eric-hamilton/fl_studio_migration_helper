import os
import re
import argparse
import json


# Find .vst .vst3 .dll .aax and .component
PATH_PATTERN = re.compile(rb'([a-zA-Z]:[\\/][^:\n\r\x00]+(?:\.dll|\.vst3?|\.aax|\.component))|([\\/][^:\n\r\x00]+(?:\.dll|\.vst3?|\.aax|\.component))', re.IGNORECASE)

default_plugin_data = {"directories":[], "plugins":{}}


def extract_plugin_data_from_fst(fst_file_path, verbose=False):

    try:
        with open(fst_file_path, 'rb') as file:
            data = file.read()
        # Find paths in the binary data
        matches = re.findall(PATH_PATTERN, data)
        plugin_name = os.path.splitext(os.path.basename(fst_file_path))[0]
        if matches:
            plugin_url = [match.decode('utf-8') for match in matches[0] if match][0]
        else:
            plugin_url = ""
        plugin_url.replace("", "/")
        plugin_dirs = {os.path.dirname(plugin_url)}
        if verbose:
            print(f"Extracted paths from {fst_file_path}: {plugin_dirs}, {plugin_name}")
        
        return plugin_name, plugin_url, plugin_dirs

    except Exception as e:
        print(f"Error reading {fst_file_path}: {e}")
        return "", [], set()


def find_plugin_directories_from_fst(plugin_data, root_dir, verbose=False):
    all_plugin_dirs = set()
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            
            if filename.lower().endswith('.fst'): # FL Studio plugin state file
                fst_file_path = os.path.join(dirpath, filename)
                if verbose:
                    print(f"Processing .fst file: {fst_file_path}")
                
                plugin_name, plugin_url, plugin_dirs = extract_plugin_data_from_fst(fst_file_path, verbose)
                all_plugin_dirs.update(plugin_dirs)
                if plugin_name:
                    plugin_data["plugins"][plugin_name] = plugin_url
    
    plugin_data["directories"] = [x for x in sorted(all_plugin_dirs)]
    return plugin_data


def modify_slashes(data, format):
    if format == "db":
        return data 
    elif format == "b":
        format_string = "\\"
    elif format == "f":
        format_string = "/"

    def replace_in_string(value):
        if isinstance(value, str):
            return value.replace("\\", format_string)
        return value

    def modify_recursive(data):
        if isinstance(data, dict):
            return {k: modify_recursive(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [modify_recursive(item) for item in data]
        else:
            return replace_in_string(data)

    return modify_recursive(data)


def main():
    parser = argparse.ArgumentParser(description="Find plugin directories from .fst files.")
    parser.add_argument("-i", "--input", help="The root directory to search for .fst files.", default=".")
    parser.add_argument("-o", "--output", help="Output file to save the plugin data.", default="fl_plugins.json")
    parser.add_argument("-v", "--verbose", help="Print verbose output to terminal.", action="store_true")
    parser.add_argument("-s", "--slashes", help="Url slash format.", default="f", choices=["f","db","b"])
    
    args = parser.parse_args()
    print("Running...")
    
    plugin_data = find_plugin_directories_from_fst(default_plugin_data, args.input, args.verbose)
    plugin_data = modify_slashes(plugin_data, args.slashes)

    if args.verbose:
        print(f"Found {len(plugin_data['plugins'].keys())} plugins...")
    
    with open(args.output, "w") as file:
        json.dump(plugin_data, file, indent=4)

    if args.verbose:
        print(f"\nData saved to '{args.output}'.")
    print("Finished!")


if __name__ == "__main__":
    main()

import os
import re
import argparse

# Find .vst .vst3 .dll .aax and .component
PATH_PATTERN = re.compile(rb'([a-zA-Z]:[\\/][^:\n\r\x00]+(?:\.dll|\.vst3?|\.aax|\.component))|([\\/][^:\n\r\x00]+(?:\.dll|\.vst3?|\.aax|\.component))', re.IGNORECASE)

def extract_plugin_paths_from_fst(fst_file_path, verbose=False):
    try:
        with open(fst_file_path, 'rb') as file:
            data = file.read()
        # Find paths in the binary data
        matches = re.findall(PATH_PATTERN, data)

        # Only get the folder path
        plugin_dirs = {os.path.dirname(match.decode('utf-8')) for match in matches if match}
        if verbose:
            print(f"Extracted paths from {fst_file_path}: {plugin_dirs}")
        
        return plugin_dirs

    except Exception as e:
        if verbose:
            print(f"Error reading {fst_file_path}: {e}")
        return set()


def find_plugin_directories_from_fst(root_dir, verbose=False):
    all_plugin_dirs = set()

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            
            if filename.lower().endswith('.fst'): # FL Studio plugin state file
                fst_file_path = os.path.join(dirpath, filename)
                if verbose:
                    print(f"Processing .fst file: {fst_file_path}")
                
                plugin_dirs = extract_plugin_paths_from_fst(fst_file_path, verbose)
                all_plugin_dirs.update(plugin_dirs)
    return all_plugin_dirs


def main():
    parser = argparse.ArgumentParser(description="Find plugin directories from .fst files.")
    parser.add_argument("-i", "--input", help="The root directory to search for .fst files.", default=".")
    parser.add_argument("-o", "--output", help="Output file to save the list of plugin directories.", default="fl_plugin_paths.txt")
    parser.add_argument("-v", "--verbose", help="Print output to terminal.", action="store_true")
    
    args = parser.parse_args()
    print("Searching for .fst files")
    
    plugin_directories = find_plugin_directories_from_fst(args.input, args.verbose)
    
    if args.verbose:
        print("\nPlugin directories:")

    with open(args.output, "w") as file:
        for plugin_dir in sorted(plugin_directories):
            file.write(plugin_dir + "\n")
            if args.verbose:
                print(plugin_dir)

    if args.verbose:
        print(f"\nList saved to '{args.output}'.")
    print("Finished")


if __name__ == "__main__":
    main()

import os
import importlib
import re
import inspect  # Import the inspect module to get caller information
import argparse

# Function to find all versioned files (except main.py and versioning.py)
def get_versioned_files(directory):
    # Find all Python files in the directory except for main.py and versioning.py
    files = [f for f in os.listdir(directory) if f.endswith('.py') and f not in ['main.py', 'versioning.py']]
    
    versioned_files = {}
    
    for file in files:
        # Try to match the versioned pattern (e.g., 'server_management_v1.py', 'utility_v2.py')
        match = re.match(r"(.+)_v(\d+)\.py", file)
        if match:
            base_name = match.group(1)
            version = int(match.group(2))
            if base_name not in versioned_files or version > versioned_files[base_name][1]:
                versioned_files[base_name] = (file, version)
    
    return versioned_files

# Function to import the latest version of a module (whether versioned or non-versioned)
def import_module(directory, base_name, version_file=None):
    # Get versioned files
    versioned_files = get_versioned_files(directory)

    # Get the caller information (the file that called import_module)
    caller = inspect.stack()[1]  # Inspect the previous stack frame (caller)
    caller_file = caller.filename  # The file that called import_module
    caller_line = caller.lineno  # The line number of the call
    print(f"Module {base_name} is being imported by {caller_file} at line {caller_line}")
    
    # If a version argument is passed, use that version if it exists
    if version_file:
        if version_file in versioned_files:
            latest_file, version = versioned_files[version_file]
            module_name = latest_file[:-3]  # Remove the .py extension
            print(f"Importing specified version of {base_name}: {latest_file}")
            return importlib.import_module(module_name)
        else:
            print(f"Specified version {version_file} not found, importing latest version.")
    
    # If versioned file exists, import the latest version
    if base_name in versioned_files:
        latest_file, version = versioned_files[base_name]
        module_name = latest_file[:-3]  # Remove the .py extension
        print(f"Importing latest version of {base_name}: {latest_file}")
        return importlib.import_module(module_name)
    else:
        # If no versioned file found, try to import the non-versioned file directly
        try:
            print(f"Importing latest version of {base_name}: {base_name}.py")
            return importlib.import_module(base_name)
        except ModuleNotFoundError:
            raise FileNotFoundError(f"No valid {base_name} file found")


# Argument parsing to pass versions to main.py
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose specific versions for modules.")
    parser.add_argument('--versions', nargs='*', help="Specify module versions in the format module_vX.py")
    args = parser.parse_args()
    
    # Get current directory to pass to import_module
    current_directory = os.getcwd()  # Get the current working directory
    
    # Dynamically import the latest version or specified versions of modules
    server_management = import_module(current_directory, 'server_management', args.versions[0] if args.versions else None)
    file_management = import_module(current_directory, 'file_management', args.versions[1] if len(args.versions) > 1 else None)
    utility = import_module(current_directory, 'utility', args.versions[2] if len(args.versions) > 2 else None)
    
    # Check if the modules were imported successfully
    if server_management is None or file_management is None or utility is None:
        print(f"Failed to import necessary modules.")
        if server_management is None:
            print("server_management module not found.")
        if file_management is None:
            print("file_management module not found.")
        if utility is None:
            print("utility module not found.")
        raise Exception("Failed to import necessary modules.")
    
    # Your existing code for handling .txt files and running speed tests would go here...
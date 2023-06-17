"""
A function to parse the config file and return the values as a dictionary.
"""
import sys
import tomllib

def parse_config(config_file: str) -> dict:
    """Parse the config file and return the values as a dictionary"""
    try:
        with open(config_file, "r") as file:
            file_contents = file.read()
            config = tomllib.loads(file_contents)['config']
    except FileNotFoundError as file_error:
        print(f"Fatal error: Unable to find file '{config_file}'.")
        print(f"{file_error.strerror}")
        sys.exit()
    return config
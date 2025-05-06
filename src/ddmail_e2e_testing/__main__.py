import sys
import os
import argparse
import toml
from ddmail_e2e_testing.test_auth import test_register

def main():
    # Get arguments from args.
    parser = argparse.ArgumentParser(description="End-to-end testing for the DDMail project.")
    parser.add_argument('--config-file', type=str, help='Full path to toml config file.', required=True)
    args = parser.parse_args()

    # Check that config file exists and is a file.
    if not os.path.isfile(args.config_file):
        print("Error: config file does not exist or is not a file.")
        sys.exit(1)

    # Parse toml config file.
    with open(args.config_file, 'r') as f:
        toml_config = toml.load(f)

    # Testing register, login and logout
    test_register(toml_config)

if __name__ == "__main__":
    main()

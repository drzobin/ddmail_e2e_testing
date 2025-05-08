import sys
import os
import argparse
import logging
import toml
from ddmail_e2e_testing.test_auth import test_register, test_login_logout
from ddmail_e2e_testing.test_email import test_add_email

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

    # Setup logging.
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    formatter = logging.Formatter(
        "{asctime} {levelname} in {module} {funcName} {lineno}: {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    # Testing register.
    logger.info("Running test_register")
    test_register(toml_config,logger)

    # Test login and logout.
    logger.info("Running test_login_logout")
    test_login_logout(toml_config,logger)

    # Test to add an email account
    logger.info("Running test_add_email")
    test_add_email(toml_config,logger)

if __name__ == "__main__":
    main()

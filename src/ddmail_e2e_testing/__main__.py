import sys
import os
import argparse
import logging
import logging.handlers
import secrets
import string
import time
import toml
from ddmail_e2e_testing.test_auth import test_register, test_login_logout
from ddmail_e2e_testing.test_email import test_add_email, test_change_password_on_email, test_remove_email
from ddmail_e2e_testing.test_openpgp import test_upload_openpgp_public_key, test_remove_openpgp_public_key

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

    formatter = logging.Formatter(
        "{asctime} {levelname} in {module} {funcName} {lineno}: {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        )

    if toml_config["LOGGING"]["LOG_TO_CONSOLE"] == True:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    if toml_config["LOGGING"]["LOG_TO_FILE"] == True:
        file_handler = logging.FileHandler(toml_config["LOGGING"]["LOGFILE"], mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    if toml_config["LOGGING"]["LOG_TO_SYSLOG"] == True:
        syslog_handler = logging.handlers.SysLogHandler(address = toml_config["LOGGING"]["SYSLOG_SERVER"])
        syslog_handler.setFormatter(formatter)
        logger.addHandler(syslog_handler)

    # Set loglevel.
    if toml_config["LOGGING"]["LOGLEVEL"] == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif toml_config["LOGGING"]["LOGLEVEL"] == "INFO":
        logger.setLevel(logging.INFO)
    elif toml_config["LOGGING"]["LOGLEVEL"] == "WARNING":
        logger.setLevel(logging.WARNING)
    elif toml_config["LOGGING"]["LOGLEVEL"] == "ERROR":
        logger.setLevel(logging.ERROR)

    # Slepp time between tests, this is to prevent dos protection to block us.
    sleep_time = toml_config["SLEEP_TIME"]


    #
    #
    # Testing register.
    logger.info("Running test_register")
    data = test_register(toml_config,logger)
    if data["is_working"] == True:
        logger.info(data["msg"])
    else:
        logger.error(data["msg"])
    

    #
    #
    # Test login and logout.
    time.sleep(sleep_time)
    logger.info("Running test_login_logout")
    data = test_login_logout(toml_config,logger)
    if data["is_working"] == True:
        logger.info(data["msg"])
    else:
        logger.error(data["msg"])

    #
    #
    # Test to add an email account.
    time.sleep(sleep_time)
    logger.info("Running test_add_email")

    # Create email and set domain
    email = ''.join(secrets.choice(string.ascii_lowercase ) for _ in range(8))
    domain = "ddmail.se"
    password = None

    data = test_add_email(toml_config,logger,email,domain)
    if data["is_working"] == True:
        logger.info(data["msg"])
        password = data["data"]["password"]
    else:
        logger.error(data["msg"])

    #
    #
    # Test to change password on email account.
    time.sleep(sleep_time)
    logger.info("Running test_change_password_on_email")

    data = test_change_password_on_email(toml_config,logger,email,domain,password)
    if data["is_working"] == True:
        logger.info(data["msg"])
    else:
        logger.error(data["msg"])

    #
    #
    # Test to remove email account.
    time.sleep(sleep_time)
    logger.info("Running test_remove_email")

    data = test_remove_email(toml_config,logger,email,domain)
    if data["is_working"] == True:
        logger.info(data["msg"])
    else:
        logger.error(data["msg"])

    #
    #
    # Test to upload openpgp public key.
    time.sleep(sleep_time)
    logger.info("Running test_upload_openpgp_public_key")

    data = test_upload_openpgp_public_key(toml_config,logger)
    if data["is_working"] == True:
        logger.info(data["msg"])
    else:
        logger.error(data["msg"])

    #
    #
    # Test to remove openpgp public key.
    time.sleep(sleep_time)
    if data["is_working"] == True:
        logger.info("Running test_remove_openpgp_public_key")
        key_fingerprint = data["data"]["key_fingerprint"]

        data = test_remove_openpgp_public_key(toml_config,logger,key_fingerprint)
        if data["is_working"] == True:
            logger.info(data["msg"])
        else:
            logger.error(data["msg"])

if __name__ == "__main__":
    main()

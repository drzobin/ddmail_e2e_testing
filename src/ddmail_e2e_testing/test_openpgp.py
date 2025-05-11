import toml
import requests
import gnupg
import ddmail_e2e_testing.helpers as helpers

def test_upload_openpgp_public_key(toml_config,logger):
    upload_url = toml_config["URL"] + "/settings/upload_openpgp_public_key"

    # Login.
    login_data = helpers.login(toml_config)
    
    # Check that login worked.
    if login_data["is_working"] == False:
        return_data = {"is_working": False, "msg": login_data["msg"], "data": None}
        logger.error(login_data["msg"])

        return return_data
    
    # Set requests session from login_data
    s = login_data["data"]["requests_session"]

    response = s.get(upload_url, timeout=2)

    # Check if get add_email worked and returned status code 200.
    if response.status_code != 200:
        msg = "GET " + upload_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data
    
    # check that login worked.
    if "Logged in as user: " + toml_config["TEST_ACCOUNT"]["USERNAME"] not in str(response.content):
        msg = "GET " + upload_url + " login failed"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that content is correct.
    if "<h3>Upload OpenPGP public key</h3>" not in str(response.content):
        msg = "GET " + upload_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Get csrf token.
    csrf_token = helpers.get_csrf_token(response.content)

    # Create openpgp private and public key.
    gpg = gnupg.GPG(gpgbinary="/usr/bin/gpg")
    gpg.encoding = 'utf-8'
    input_data = gpg.gen_key_input(key_type="RSA", key_length=4096,no_protection=True)
    key = gpg.gen_key(input_data)
    ascii_key = gpg.export_keys(key.fingerprint)

    # Upload openpgp public key.
    data={'csrf_token': csrf_token}
    file_content = ascii_key.encode('utf-8')
    files = {"openpgp_public_key": ("openpgp_public_key", file_content)}

    response = s.post(upload_url, data=data, files=files, timeout=2)


    # Check if post upload worked and returned status code 200.
    if response.status_code != 200:
        msg = "POST " + upload_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that upload worked.
    if "Succesfully upload openpgp public key." not in str(response.content):
        msg = "POST " + upload_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)
        print(response.content)

        return return_data

    msg = "working"
    return_data = {"is_working": True, "msg": msg, "data": {"key_fingerprint":key.fingerprint}}

    return return_data

def test_remove_openpgp_public_key(toml_config,logger,key_fingerprint):
    remove_url = toml_config["URL"] + "/settings/remove_openpgp_public_key"

    # Login.
    login_data = helpers.login(toml_config)
    
    # Check that login worked.
    if login_data["is_working"] == False:
        return_data = {"is_working": False, "msg": login_data["msg"], "data": None}
        logger.error(login_data["msg"])

        return return_data
    
    # Set requests session from login_data
    s = login_data["data"]["requests_session"]

    response = s.get(remove_url, timeout=2)

    # Check if get remove_url worked and returned status code 200.
    if response.status_code != 200:
        msg = "GET " + remove_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data
    
    # check that login worked.
    if "Logged in as user: " + toml_config["TEST_ACCOUNT"]["USERNAME"] not in str(response.content):
        msg = "GET " + remove_url + " login failed"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that content is correct.
    if "<h3>Remove Openpgp public key</h3>" not in str(response.content):
        msg = "GET " + remove_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)
        print(str(response.content))

        return return_data

    # Get csrf token.
    csrf_token = helpers.get_csrf_token(response.content)

    # Remove openpgp public key.
    data={'csrf_token': csrf_token, 'fingerprint': key_fingerprint}
    response = s.post(remove_url, data=data, timeout=2)


    # Check if post remove_url worked and returned status code 200.
    if response.status_code != 200:
        msg = "POST " + remove_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that remove_url return correct content.
    if "Succesfully removed OpenPGP public key." not in str(response.content):
        msg = "POST " + remove_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)
        print(response.content)

        return return_data

    msg = "working"
    return_data = {"is_working": True, "msg": msg, "data": None}

    return return_data
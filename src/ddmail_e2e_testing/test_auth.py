import time
import toml
import requests
import ddmail_e2e_testing.helpers as helpers

def test_register(toml_config, logger):
    # Use requests session to easy get out auth cookie to follow along our requests.
    s = requests.Session()

    # Get /register csrf token.
    register_url = toml_config["URL"] + "/register"
    response = s.get(register_url, timeout=2)

    # Check that we get status code 200.
    if response.status_code != 200:
        msg = "GET " + register_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Parse the csrf token from html content.
    csrf_token = helpers.get_csrf_token(response.content)

    # Register new account and user.
    response = s.post(register_url, data={'csrf_token': csrf_token},timeout=2)

    # Get authentication data for the newly registers account and user.
    auth_data = helpers.get_register_data(response.content)
    
    # Get /login csrf token.
    login_url = toml_config["URL"] + "/login"
    response = s.get(login_url, timeout=2)
    csrf_token = helpers.get_csrf_token(response.content)

    # Login with new account.
    data={'csrf_token': csrf_token, 'user': auth_data["username"], 'password': auth_data["password"]}
    file_content = auth_data["key"].encode('utf-8')
    files = {"key": ("key.txt", file_content)}

    response = s.post(login_url, data=data, files=files, timeout=2)

    # Check if POST /login returns status code 200.
    if response.status_code != 200:
        msg = "POST " + login_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that POST /login
    if "Logged in as user: " + auth_data["username"] not in str(response.content):
        msg = "POST " + login_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # All is working.
    msg = "working"
    return_data = {"is_working": True, "msg": msg, "data": None}

    return return_data


def test_login_logout(toml_config, logger):
    main_url = toml_config["URL"] 
    logout_url = toml_config["URL"] + "/logout"

    login_data = helpers.login(toml_config)
    
    # Check that login worked.
    if login_data["is_working"] == False:
        return_data = {"is_working": False, "msg": login_data["msg"], "data": None}
        logger.error(login_data["msg"])

        return return_data
    
    # Set requests session from login_data
    s = login_data["data"]["requests_session"]
    response = s.get(main_url, timeout=2)

    # Check if login worked and returned status code 200.
    if response.status_code != 200:
        msg = "GET " + main_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data
    
    # Check if login worked.
    if "Logged in as user: " + toml_config["TEST_ACCOUNT"]["USERNAME"] not in str(response.content):
        msg = "GET " + main_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Logout.
    response = s.get(logout_url, timeout=2)
    
    # Check if logout worked and returned status code 200.
    if response.status_code != 200:
        msg = "GET " + logout_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data
    
    # Check if logout worked.
    if "Logged in as user: Not logged in" not in str(response.content):
        msg = "fail: GET " + logout_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # All is working.
    msg = "working"
    return_data = {"is_working": True, "msg": msg, "data": None}

    return return_data


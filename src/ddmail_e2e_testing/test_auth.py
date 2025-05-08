import time
import toml
import requests
import ddmail_e2e_testing.helpers as helpers

def test_register(toml_config, logger):
    # Use requests session to easy get out auth cookie to follow along our requests.
    s = requests.Session()

    # Get /register csrf token.
    register_url = toml_config["URL"] + "/register"
    response = s.get(register_url, timeout=1)

    # Check that we get status code 200.
    if response.status_code != 200:
        msg = "GET " + register_url + " did not returned status code 200"
        logger.error(msg)

        return msg

    # Parse the csrf token from html content.
    csrf_token = helpers.get_csrf_token(response.content)

    # Register new account and user.
    response = s.post(register_url, data={'csrf_token': csrf_token},timeout=1)

    # Get authentication data for the newly registers account and user.
    auth_data = helpers.get_register_data(response.content)
    
    # Get /login csrf token.
    login_url = toml_config["URL"] + "/login"
    response = s.get(login_url, timeout=1)
    csrf_token = helpers.get_csrf_token(response.content)

    # Login with new account.
    data={'csrf_token': csrf_token, 'user': auth_data["username"], 'password': auth_data["password"]}
    file_content = auth_data["key"].encode('utf-8')
    files = {"key": ("key.txt", file_content)}

    response = s.post(login_url, data=data, files=files, timeout=2)

    # Check if POST /login returns status code 200.
    if response.status_code != 200:
        msg = "POST " + login_url + " did not returned status code 200"
        logger.error(msg)

        return msg

    # Check that POST /login
    if "Logged in as user: " + auth_data["username"] not in str(response.content):
        msg = "POST " + login_url + " did not returned correct content"
        logger.error(msg)

        return msg

    # All is working.
    logger.info("working")
    return "working"


def test_login_logout(toml_config, logger):
    print("Testing /login and /logout")
    main_url = toml_config["URL"] 
    logout_url = toml_config["URL"] + "/logout"

    s = helpers.login(toml_config)
    
    # Check that login worked.
    if s == None:
        msg = "login failed"
        logger.error(msg)

        return msg

    response = s.get(main_url, timeout=1)

    # Check if login worked and returned status code 200.
    if response.status_code != 200:
        msg = "GET " + main_url + " did not returned status code 200"
        logger.error(msg)

        return msg
    
    # Check if login worked.
    if "Logged in as user: " + toml_config["TEST_ACCOUNT"]["USERNAME"] not in str(response.content):
        msg = "GET " + main_url + " did not returned correct content"
        logger.error(msg)

        return msg

    # Logout.
    response = s.get(logout_url, timeout=1)
    
    # Check if logout worked and returned status code 200.
    if response.status_code != 200:
        msg = "GET " + logout_url + " did not returned status code 200"
        logger.error(msg)

        return msg
    
    # Check if logout worked.
    if "Logged in as user: Not logged in" not in str(response.content):
        msg = "fail: GET " + logout_url + " did not returned correct content"
        logger.error(msg)

        return msg

    logger.info("working")
    return "working"


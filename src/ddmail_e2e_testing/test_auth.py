import time
import toml
import pytest
import requests
import ddmail_e2e_testing.helpers as helpers

def test_register(toml_config):
    print("Testing /register")
    # Use requests session to easy get out auth cookie to follow along our requests.
    s = requests.Session()

    # Get /register csrf token.
    register_url = toml_config["URL"] + "/register"
    response = s.get(register_url, timeout=1)
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

    # Check if login workes with the newly registered/created account/user/password and key.
    if response.status_code == 200 and "Logged in as user: " + auth_data["username"] in str(response.content):
        print("working")
        return "working"
    else:
        print("fail")
        return "fail"

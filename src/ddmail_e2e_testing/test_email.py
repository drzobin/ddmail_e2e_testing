import toml
import requests
import ddmail_e2e_testing.helpers as helpers

def test_add_email(toml_config,logger,email,domain):
    main_url = toml_config["URL"] 
    add_email_url = toml_config["URL"] + "/settings/add_email"

    # Login.
    login_data = helpers.login(toml_config)
    
    # Check that login worked.
    if login_data["is_working"] == False:
        return_data = {"is_working": False, "msg": login_data["msg"], "data": None}
        logger.error(login_data["msg"])

        return return_data
    
    # Set requests session from login_data
    s = login_data["data"]["requests_session"]

    response = s.get(add_email_url, timeout=2)

    # Check if get add_email worked and returned status code 200.
    if response.status_code != 200:
        msg = "GET " + add_email_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data
    
    # check that login worked.
    if "Logged in as user: " + toml_config["TEST_ACCOUNT"]["USERNAME"] not in str(response.content):
        msg = "GET " + add_email_url + " login failed"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that content is correct.
    if "<h3>Add Email Account</h3>" not in str(response.content):
        msg = "GET " + add_email_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Get csrf token.
    csrf_token = helpers.get_csrf_token(response.content)

    # Add email.
    data={'csrf_token': csrf_token, 'email': email, 'domain': domain}
    response = s.post(add_email_url, data=data, timeout=2)

    # Check if post add_email worked and returned status code 200.
    if response.status_code != 200:
        msg = "POST " + add_email_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that email was added.
    if "Successfully added email: " + email + "@" + domain + " with password:" not in str(response.content):
        msg = "POST " + add_email_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Get email password.
    password = helpers.get_email_password(response.content)

    msg = "working"
    return_data = {"is_working": True, "msg": msg, "data": {"email":email,"domain":domain,"password":password}}

    return return_data

def test_change_password_on_email(toml_config,logger,email,domain,password):
    main_url = toml_config["URL"] 
    change_password_on_email_url = toml_config["URL"] + "/settings/change_password_on_email"

    # Login.
    login_data = helpers.login(toml_config)
    
    # Check that login worked.
    if login_data["is_working"] == False:
        return_data = {"is_working": False, "msg": login_data["msg"], "data": None}
        logger.error(login_data["msg"])

        return return_data
    
    # Set requests session from login_data
    s = login_data["data"]["requests_session"]

    response = s.get(change_password_on_email_url, timeout=2)

    # Check if get change_password_on_email_url worked and returned status code 200.
    if response.status_code != 200:
        msg = "GET " + change_password_on_email_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data
    
    # check that login worked.
    if "Logged in as user: " + toml_config["TEST_ACCOUNT"]["USERNAME"] not in str(response.content):
        msg = "GET " + change_password_on_email_url + " login failed"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that content is correct.
    if "<h3>Change password on Email Account</h3>" not in str(response.content):
        msg = "GET " + change_password_on_email_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Get csrf token.
    csrf_token = helpers.get_csrf_token(response.content)

    # Change password on email.
    data={'csrf_token': csrf_token, 'change_password_on_email': email + "@" + domain, 'email_password': password}
    response = s.post(change_password_on_email_url, data=data, timeout=2)

    # Check if post change_password_on_email_url worked and returned status code 200.
    if response.status_code != 200:
        msg = "POST " + change_password_on_email_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that content is correct.
    if "Successfully changed password on email account: " + email + "@" + domain + " to new password:" not in str(response.content):
        msg = "POST " + change_password_on_email_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data


    msg = "working"
    return_data = {"is_working": True, "msg": msg, "data": None}

    return return_data

def test_remove_email(toml_config,logger,email,domain):
    remove_email_url = toml_config["URL"] + "/settings/remove_email"

    # Login.
    login_data = helpers.login(toml_config)
    
    # Check that login worked.
    if login_data["is_working"] == False:
        return_data = {"is_working": False, "msg": login_data["msg"], "data": None}
        logger.error(login_data["msg"])

        return return_data
    
    # Set requests session from login_data
    s = login_data["data"]["requests_session"]

    response = s.get(remove_email_url, timeout=2)

    # Check if get remove_email_url worked and returned status code 200.
    if response.status_code != 200:
        msg = "GET " + remove_email_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data
    
    # check that login worked.
    if "Logged in as user: " + toml_config["TEST_ACCOUNT"]["USERNAME"] not in str(response.content):
        msg = "GET " + remove_email_url + " login failed"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that content is correct.
    if "<h3>Remove Email Account</h3>" not in str(response.content):
        msg = "GET " + remove_email_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Get csrf token.
    csrf_token = helpers.get_csrf_token(response.content)

    # Remove email.
    data={'csrf_token': csrf_token, 'remove_email': email + "@" + domain}
    response = s.post(remove_email_url, data=data, timeout=2)

    # Check if post remove_email_url worked and returned status code 200.
    if response.status_code != 200:
        msg = "POST " + remove_email_url + " did not returned status code 200"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data

    # Check that content is correct.
    if "Successfully removed email." not in str(response.content):
        msg = "POST " + remove_email_url + " did not returned correct content"
        return_data = {"is_working": False, "msg": msg, "data": None}
        logger.error(msg)

        return return_data


    msg = "working"
    return_data = {"is_working": True, "msg": msg, "data": None}

    return return_data


    

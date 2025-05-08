import toml
import requests
import ddmail_e2e_testing.helpers as helpers

def test_add_email(toml_config,logger):
    print("Testing /settings/add_email")

    main_url = toml_config["URL"] 
    add_email_url = toml_config["URL"] + "/settings/add_email"

    # Email to add.
    email = "test4321"

    # Email domain part
    domain = "ddmail.se"

    # Login.
    s = helpers.login(toml_config)

    if s == None:
        msg = "fail: login failed"
        print(msg)

        return msg

    response = s.get(add_email_url, timeout=1)

    # Check if get add_email worked and returned status code 200.
    if response.status_code != 200:
        msg = "fail: GET " + add_email_url + " did not returned status code 200"
        print(msg)

        return msg
    
    # check that login worked.
    if "Logged in as user: " + toml_config["TEST_ACCOUNT"]["USERNAME"] not in str(response.content):
        msg = "fail: GET " + add_email_url + " login failed"
        print(msg)

        return msg

    # Check that content is correct.
    if "<h3>Add Email Account</h3>" not in str(response.content):
        msg = "fail: GET " + add_email_url + " did not returned correct content"
        print(msg)

        return msg

    # Get csrf token.
    csrf_token = helpers.get_csrf_token(response.content)

    # Add email.
    data={'csrf_token': csrf_token, 'email': email, 'domain': domain}
    response = s.post(add_email_url, data=data, timeout=2)

    # Check if post add_email worked and returned status code 200.
    if response.status_code != 200:
        msg = "fail: POST " + add_email_url + " did not returned status code 200"
        print(msg)

        return msg

    # Check that email was added.
    if "Successfully added email: " + email + "@" + domain + "with password" in str(response.content):
        print("working")
        return "working"
    else:
        msg = "fail: POST " + add_email_url + " did not work"
        print(msg)

        return msg
    
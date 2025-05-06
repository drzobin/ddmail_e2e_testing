import re
import requests

def get_csrf_token(data):
    m = re.search(b'<input type="hidden" name="csrf_token" value="(.*)"/>', data)
    csrf_token = m.group(1).decode("utf-8")

    return csrf_token

def get_register_data(data):
    register_data = {}

    # Get account
    m = re.search(b'<p>Account: (.*)</p>', data)
    register_data["account"] = m.group(1).decode("utf-8")
    
    # Get username
    m = re.search(b'<p>Username: (.*)</p>', data)
    register_data["username"] = m.group(1).decode("utf-8")
   
   #Get password
    m = re.search(b'<p>Password: (.*)</p>', data)
    register_data["password"] = m.group(1).decode("utf-8")
    
    #Get key
    m = re.search(b'<p>Key file content: (.*)</p>', data)
    register_data["key"] = m.group(1).decode("utf-8")

    return register_data

def login(toml_config):
    # Use requests session to get auth cookie to follow along our requests.
    s = requests.Session()

    # Set login url..
    login_url = toml_config["URL"] + "/login"

    # Set username and password used for login..
    user = toml_config["TEST_ACCOUNT"]["USERNAME"]
    password = toml_config["TEST_ACCOUNT"]["PASSWORD"]

    # Set key file data used for login.
    file = open('toml_config["TEST_ACCOUNT"]["KEY_FILE_PATH"]', "r")
    key = file.read()
    file.close()
    
    # Get /login csrf token.
    response = s.get(login_url, timeout=1)
    csrf_token = helpers.get_csrf_token(response.content)

    # Create post request for login.
    data={'csrf_token': csrf_token, 'user': user, 'password': password}
    file_content = auth_data["key"].encode('utf-8')
    files = {"key": ("key.txt", file_content)}

    # Login with account from config file.
    response = s.post(login_url, data=data, files=files, timeout=2)

    # Return session with auth cookie set..
    return s

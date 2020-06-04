import requests
import re

import DataManager

un = 'admin'
pw = 'admin'
session = None
headers = {
    'Host': '192.168.1.1',
    'Connection': 'keep-alive',
    'Content-Length': '39',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://192.168.1.1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://192.168.1.1/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'he,en-US;q=0.9,en;q=0.8',
    'Cookie': 'login='
}


def init(username, password):
    global un, pw
    un = username
    pw = password


def start():
    global session
    session = requests.session()
    print("start1")


def login():
    global session
    session.get("http://192.168.1.1", headers=headers)
    url = "http://192.168.1.1/goform/login"
    data = "loginUsername=" + un + "&loginPassword=" + pw + "&rememberMe=rememberMe"
    s_data = session.post(url, data, headers=headers)
    print(s_data.text)
    print("login")


def noInternet(mac):
    print("block : " + mac)
    start()
    data = DataManager.get_user_name_and_password()
    init(data['username'], data['password'])
    login()
    return _noInternet(mac)


def _noInternet(mac):
    global session
    page = session.get("http://192.168.1.1/RgMacFiltering.asp", headers=headers)
    token = re.search(r"<input type=\"hidden\" name=\"MacFilteringCsrfToken\" value=(.*) >", page.text, re.MULTILINE)[1]
    session.post("http://192.168.1.1/goform/RgMacFiltering",
                 {'NewMacFilter': mac, 'MacFilterAction': '1', 'MacFilteringCsrfToken': token}, headers=headers)


def yesInternet(mac):
    print("unblock : " + mac)
    start()
    data = DataManager.get_user_name_and_password()
    init(data['username'], data['password'])
    login()
    return _yesInternet(mac)


def _yesInternet(mac):
    global session
    page = session.get("http://192.168.1.1/RgMacFiltering.asp", headers=headers)
    token = re.search(r"<input type=\"hidden\" name=\"MacFilteringCsrfToken\" value=(.*?) >", page.text, re.MULTILINE)[
        1]
    try:
        option = re.search(r"<option value=\"((?:(?!<).)*?)\">" + mac + "<", page.text, re.MULTILINE)[1]
        post_data = {'NewMacFilter': "", 'MacFilterAction': '2', 'MacFilteringCsrfToken': token,
                     "MacFilterList": option}
        session.post("http://192.168.1.1/goform/RgMacFiltering", post_data, headers=headers)
    except:
        pass


def __has_internet(mac):
    try:
        page = session.get("http://192.168.1.1/RgMacFiltering.asp")
        re.search(r"<option value=\"((?:(?!<).)*?)\">" + mac + "<", page.text, re.MULTILINE)[1]
        return False
    except:
        return True


def has_internet(mac):
    start()
    data = DataManager.get_user_name_and_password()
    init(data['username'], data['password'])
    login()
    return __has_internet(mac)

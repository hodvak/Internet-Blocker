import eel

NAME = 0
MAC = 1
BLOCK_START = 2
BLOCK_END = 3


def get_all_devices():
    try:
        data = []
        file = open("devices.txt", "r+", encoding="utf-8")
    except:
        open("devices.txt", "w", encoding="utf-8")
        return []
    for line in file:
        if line.endswith("\n"):
            line = line[:-1]
        if line is not "":
            data.append({"name": line.split('=')[NAME], "mac": line.split('=')[MAC],
                         "block start": line.split('=')[BLOCK_START], "block end": line.split('=')[BLOCK_END]})
    return data


def get_user_name_and_password():
    try:
        file = open("up.txt", "r+", encoding="utf-8")
    except:
        file = open("up.txt", "w", encoding="utf-8")
        file.write("admin\nadmin")
        return {"username": "admin", "password": "admin"}
    data = {'username': file.readline()[:-1], 'password': file.readline()}
    return data


def update_user_and_pass(username, password):
    file = open("up.txt", "w", encoding="utf-8")
    file.write(username + "\n" + password)


def add_device(name, mac):
    file = open("devices.txt", "a", encoding="utf-8")
    mac = mac.lower()
    if "=" not in mac:
        file.write("\n" + name + "=" + mac + "=-1=-1")


def get_name_by_mac(mac):
    try:
        devices = get_all_devices()
    except:
        print("error")
        return "-1"
    for device in devices:
        if device['mac'] == mac:
            return device['name']
    return "-1"


def delete_device(mac):
    try:
        data = ""
        file = open("devices.txt", "r+", encoding="utf-8")
    except:
        open("devices.txt", "w", encoding="utf-8")
        return
    for line in file:
        if line.replace("\n", "") is not "":
            if not line.replace("\n", "").split("=")[MAC] == mac:
                print(line)
                data += line
    open("devices.txt", "w", encoding="utf-8").write(data)


@eel.expose
def change_device_times(mac, block_start, block_end):
    try:
        data = ""
        file = open("devices.txt", "r+", encoding="utf-8")
    except:
        open("devices.txt", "w", encoding="utf-8")
        return
    for line in file:
        if line.replace("\n", "") is not "":
            if line.replace("\n", "").split("=")[MAC] == mac:
                print(line)
                line = line.replace("\n", "")
                line = line.split("=")
                newline = line[NAME] + "=" + line[MAC] + "=" + str(block_start) + "=" + str(block_end) + "\n"
                data += newline
            else:
                data += line
    open("devices.txt", "w", encoding="utf-8").write(data)


def get_device_by_mac(mac):
    try:
        devices = get_all_devices()
    except:
        print("error")
        return "-1"
    for device in devices:
        if device['mac'] == mac:
            return device
    return "-1"

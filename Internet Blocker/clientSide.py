import datetime

import eel

import DataManager
import routerConnecting


def start():
    eel.init('web')
    eel.start("index.html", port=0, block=False)


@eel.expose
def get_all_devices():
    devices = DataManager.get_all_devices()
    htmlcode = '<a class="list-group-item list-group-item-action bg-light" onclick="settings()"><b>Settings</b></a>'
    for device in devices:
        htmlcode += "<a class=\"list-group-item list-group-item-action bg-light\" onclick=\"eel.update_device('" + \
                    device[
                        'mac'] + "')\">" + device['name'] + "</a>"
    htmlcode += '<a class="list-group-item list-group-item-action bg-light" ' \
                'style="color:#007bff;" onclick="addDeviceWindow()">Add Device</a>'
    eel.setAllDevices(htmlcode)


@eel.expose
def update_settings(username, password):
    DataManager.update_user_and_pass(username, password)


@eel.expose
def add_device(name, mac):
    DataManager.add_device(name, mac)
    get_all_devices()


@eel.expose
def update_device(mac):
    device = DataManager.get_device_by_mac(mac)
    if device == "-1":
        print("error with this device)")
        return
    try:
        if device['block start']!="-1":
            if len(device['block start']) > 2:
                block_start = device['block start'][:-2] + ":" + device['block start'][-2:]
            else:
                block_start = "0:" + device['block start']
        else:
            block_start=""

        if device['block end'] != "-1":
            if len(device['block end']) > 2:
                block_end = device['block end'][:-2] + ":" + device['block end'][-2:]
            else:
                block_end = "0:" + device['block end']
        else:
            block_end = ""

        eel.setDevice(device["name"], device["mac"], routerConnecting.has_internet(mac), block_start, block_end)
    except Exception as e:
        print(e)
        print("an error with connection to router...maybe the username or password to the router are incorrect")


@eel.expose
def open_internet(mac):
    try:
        routerConnecting.yesInternet(mac)
    except:
        print("an error with connection to router...maybe the username or password to the router are incorrect")
    update_device(mac)


@eel.expose
def close_internet(mac):
    # try:
    routerConnecting.noInternet(mac)
    # except Exception as e:
    #     print(e)
    #     print("an error with connection to router...maybe the username or password are incorrect")
    update_device(mac)


@eel.expose
def delete_device(mac):
    DataManager.delete_device(mac)
    get_all_devices()


@eel.expose
def change_block_time(mac, block_start, block_end):
    block_start = block_start.replace(":", "")
    if block_start.isnumeric():
        if len(block_start) <= 2:
            block_start += '00'
    else:
        block_start = "-1"

    block_end = block_end.replace(":", "")
    if block_end.isnumeric():
        if len(block_end) <= 2:
            block_end += '00'
    else:
        block_end = "-1"

    DataManager.change_device_times(mac, block_start, block_end)


if __name__ == '__main__':
    start()
    eel.sleep(1)
    get_all_devices()
    currentDT = datetime.datetime.now()
    last_did_something = currentDT.hour * 100 + currentDT.minute
    # do some stuff
    while True:
        eel.sleep(2)
        currentDT = datetime.datetime.now()
        nowtime = currentDT.hour * 100 + currentDT.minute
        for device in DataManager.get_all_devices():
            block_start = int(device['block start'])
            block_end = int(device['block end'])
            if last_did_something < block_start <= nowtime:
                close_internet(device['mac'])

            if last_did_something < block_end <= nowtime:
                open_internet(device['mac'])
        last_did_something = nowtime

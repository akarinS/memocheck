#!/usr/bin/env python3

# Copyright (C) 2018 akarinS <akaringithub0655@gmail.com>
# Released under the WTFPL.
# https://github.com/akarinS/memocheck/blob/master/LICENSE

import requests
import os
import json
import sys
import codecs
import datetime

# ここを自動で設定するようにする！
rpcuser = "rpcuser"
rpcpassword = "rpcpassword"
rpcport = "8432"

def use_koto_cli(command, *params):
    auth = (rpcuser, rpcpassword)
    url = "http://127.0.0.1:" + port
    headers = {"content-type": "text/plain;"}
    data = json.dumps({"jsonrpc": "1.0", "id": "memocheck", "method": command, "params": params})
    try:
        response = requests.post(url, auth = auth, headers = headers, data = data)
    except:
        print("Error!")
        sys.exit()
    if response.json()["error"] != None:
        print("Error!!")
        sys.exit()
    result = response.json()["result"]
    return result

def input_index():
    while True:
        try:
            index_string = input("Select number of address : ")
        except (EOFError, KeyboardInterrupt):
            print("")
            sys.exit()
        if index_string.isdigit():
            index = int(index_string)
            break
    return index

def select_z_address():
    version = get_version()
    if 1001450 <= version:
        z_address_list = use_koto_cli("z_listaddresses", True)
    else:
        z_address_list = use_koto_cli("z_listaddresses")
    index = 0
    for z_address in z_address_list:
        print("[" + str(index) + "] " + z_address)
        index += 1
    print("")
    while True:
        index = input_index()
        if 0 <= index and index < len(z_address_list):
            selected_z_address = z_address_list[index]
            print("\n" + selected_z_address, end="\n\n")
            break
    return selected_z_address

def get_data(z_address):
    data = []
    received_data = use_koto_cli("z_listreceivedbyaddress", z_address)
    for a_data in received_data:
        transaction_data = use_koto_cli("gettransaction", a_data["txid"])
        if a_data["memo"].startswith("f60000"):
            memo = "---Empty---"
        else:
            try:
                memo = codecs.decode(a_data["memo"], "hex_codec").decode("utf-8")
            except UnicodeDecodeError:
                memo = "---DecodeError---"
        data.append({"time": transaction_data["time"], "amount": a_data["amount"], "txid": a_data["txid"], "memo": memo})
    data.sort(key = lambda a_data: a_data["time"])
    return data

def print_each_data(data):
    for a_data in data:
        if a_data["memo"] != "---Empty---" and a_data["memo"] != "---DecodeError---":    # if you delete this line, you can see all memo.
            timestamp = datetime.datetime.fromtimestamp(a_data["time"])
            print(str(timestamp) + "  " + "{0:0.8f}".format(a_data["amount"]) + "KOTO  "+ a_data["txid"])
            print(a_data["memo"], end="\n\n")

def get_version():
    info_data = use_koto_cli("getinfo")
    return info_data["version"]

if __name__ == '__main__':
    z_address = select_z_address()
    data = get_data(z_address)
    print_each_data(data)


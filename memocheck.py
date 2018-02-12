#!/usr/bin/env python3

"""
Copyright (C) 2018 akarinS <akaringithub0655@gmail.com>
Released under the WTFPL.
https://github.com/akarinS/memocheck/blob/master/LICENSE
"""

import os
import requests
import json
import sys
import codecs
import datetime
from time import sleep


class Rpc(object):
    
    def __init__(self):
        self.rpcport = "8432"   # Default port
        self.headers = {"content-type": "text/plain;"}
        self.set_conf_path()
        self.set_rpc_conf()

    def set_conf_path(self):
        os_name = sys.platform
        if os_name == "linux":
            self.path = os.path.expanduser("~/.koto/koto.conf")
        elif os_name == "darwin":
            self.path = os.path.expanduser("~/Library/Application Support/Koto/koto.conf")
        else:
            self.path = os.path.expanduser("~/.koto/koto.conf")
    
    def set_rpc_conf(self):
        try:
            with open(self.path, "r") as f:
                lines = f.readlines()
        except:
            print("koto.conf can not be found.")
            sys.exit()
        for line in lines:
            data = line.strip().split("=")
            if data[0] == "rpcuser":
                self.rpcuser = data[1]
            elif data[0] == "rpcpassword":
                self.rpcpassword = data[1]
            elif data[0] == "rpcport":
                self.rpcport = data[1]

    def koto_cli(self, command, *params):
        auth = (self.rpcuser, self.rpcpassword)
        url = "http://127.0.0.1:" + self.rpcport
        headers = self.headers
        data = json.dumps({"jsonrpc": "1.0", "id": "memocheck", "method": command, "params": params})
        timeout = 3
        while True:
            try:
                response = requests.post(url, auth = auth, headers = headers, data = data)
            except:
                print("Error : kotod may not be running.")
                sys.exit()
            if response.json()["error"] == None:
                break
            elif timeout == 0:
                print("Error : timeout. kotod may be in start-up.")
                sys.exit()
            else:
                timeout -= 1
                try:
                    sleep(10)
                except:
                    sys.exit()
        result = response.json()["result"]
        return result


class Memocheck(object):

    def __init__(self):
        self.rpc = Rpc()

    def check(self):
        self.select_address()
        self.get_data()
        self.show_data()

    def select_address(self):
        version = self.rpc.koto_cli("getinfo")["version"]
        if 1001450 <= version:
            addresses = self.rpc.koto_cli("z_listaddresses", True)
        else:
            addresses = self.rpc.koto_cli("z_listaddresses")
        index = 0
        for address in addresses:
            print("[" + str(index) + "] " + address)
            index += 1
        print("")
        while True:
            index = self.input_index()
            if 0 <= index and index < len(addresses):
                selected_address = addresses[index]
                print("\n[" + str(index) + "] " + selected_address, end="\n\n")
                break
        self.address = selected_address

    def input_index(self):
        while True:
            try:
                index_string = input("Select index of address : ")
            except (EOFError, KeyboardInterrupt):
                print("")
                sys.exit()
            except:
                print("Error")
                sys.exit()
            if index_string.isdigit():
                index = int(index_string)
                break
        return index

    def get_data(self):
        data = []
        received_data = self.rpc.koto_cli("z_listreceivedbyaddress", self.address)
        for a_data in received_data:
            transaction_data = self.rpc.koto_cli("gettransaction", a_data["txid"])
            if a_data["memo"].startswith("f60000"):
                memo = "---Empty---"
            else:
                try:
                    memo = codecs.decode(a_data["memo"], "hex_codec").decode("utf-8")
                except UnicodeDecodeError:
                    memo = "---DecodeError---"
            data.append({"time": transaction_data["time"], "amount": a_data["amount"], "txid": a_data["txid"], "memo": memo})
        data.sort(key = lambda a_data: a_data["time"])
        self.data = data

    def show_data(self):
        for a_data in self.data:
            if a_data["memo"] != "---Empty---" and a_data["memo"] != "---DecodeError---":    # if you delete this line, you can see all memo.
                timestamp = datetime.datetime.fromtimestamp(a_data["time"])
                print(str(timestamp) + "  " + "{0:0.8f}".format(a_data["amount"]) + "KOTO  "+ a_data["txid"])
                print(a_data["memo"], end="\n\n")


if __name__ == '__main__':
    memocheck = Memocheck()
    memocheck.check()


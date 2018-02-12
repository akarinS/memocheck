#!/usr/bin/env python3

"""
Copyright (C) 2018 akarinS <akaringithub0655@gmail.com>
Released under the WTFPL.
https://github.com/akarinS/memocheck/blob/master/LICENSE
"""

import os
import subprocess
import json
import sys
import codecs
import datetime
from time import sleep


class Rpc(object):
    
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "koto-cli")

    def koto_cli(self, command, *params):
        command_string_list = [self.path, command]
        command_string_list.extend(params)
        result = json.loads(subprocess.getoutput(" ".join(command_string_list)))
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
            addresses = self.rpc.koto_cli("z_listaddresses", "true")
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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import datetime
import sys
import os
import codecs

ARGS = sys.argv
ZADDRESS = ARGS[1]
KOTOCLI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "koto-cli ")
DEFAULTMEMO = "f600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

def get_received_data(z_address):
  json_data = subprocess.getoutput(KOTOCLI + "z_listreceivedbyaddress " + z_address)
  raw_data = json.loads(json_data)

  return raw_data


def get_transaction_data(raw_data):
  unsorted_data = []

  for a_data in raw_data:
    transaction_json_data = subprocess.getoutput(KOTOCLI + "gettransaction " + a_data["txid"])
    transaction_data = json.loads(transaction_json_data)
    
    if a_data["memo"] != DEFAULTMEMO:
      try:
        memo = codecs.decode(a_data["memo"], "hex_codec").decode("utf-8")
      except UnicodeDecodeError:
        memo = "---DecodeError---"
    else:
      memo = "---Empty---"
      

    txid_time_memo_amount = {"txid": transaction_data["txid"], "time": transaction_data["time"], "memo": memo, "amount": a_data["amount"]}
    unsorted_data.append(txid_time_memo_amount)

  return unsorted_data


def get_sorted_data(unsorted_data):
  sorted_data = []

  for a_data in unsorted_data:
    index = 0
    
    if len(sorted_data) == 0:
      sorted_data.append(a_data)
    else:
      while index < len(sorted_data):
        if a_data["time"] < sorted_data[index]["time"]:
          sorted_data.insert(index, a_data)
          break
        elif index == len(sorted_data) - 1:
          sorted_data.append(a_data)
          break

        index = index + 1

  return sorted_data


def print_each_data(sorted_data):
  print("\n\n", end="")

  for a_data in sorted_data:
#    if a_data["memo"] != "---Empty---":
      timestamp = datetime.datetime.fromtimestamp(a_data["time"])
      
      print(str(timestamp) + "  " + "{0:0.8f}".format(a_data["amount"]) + "KOTO  "+ a_data["txid"])
      print(a_data["memo"], end="\n\n")

def get_final_data(z_address):
  return get_sorted_data(get_transaction_data(get_received_data(ZADDRESS)))


if __name__ == '__main__':
  print_each_data(get_final_data(ZADDRESS))


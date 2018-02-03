#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import json
import datetime
import sys

ARGS = sys.argv
ZADDRESS = ARGS[1]
KOTOCLI = "~/koto/src/koto-cli "
DEFAULTMEMO = "f600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

def get_received_data(ZADDRESS):
  json_data = commands.getoutput(KOTOCLI + "z_listreceivedbyaddress " + ZADDRESS)
  raw_data = json.loads(json_data)

  return raw_data


def get_transaction_data(raw_data):
  unsorted_data = []

  for a_data in raw_data:
    transaction_json_data = commands.getoutput(KOTOCLI + "gettransaction " + a_data["txid"])
    transaction_data = json.loads(transaction_json_data)
    
    if a_data["memo"] != DEFAULTMEMO:
      try:
        memo = unicode(a_data["memo"].decode("hex_codec"), "UTF-8")
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
  print("\n\n")

  for a_data in sorted_data:
    if a_data["memo"] != "---Empty---":
      timestamp = datetime.datetime.fromtimestamp(a_data["time"])
      
      print(str(timestamp) + "  " + "{0:0.8f}".format(a_data["amount"]) + "KOTO  "+ a_data["txid"])
      print(a_data["memo"])
      print("\n")

print_each_data(get_sorted_data(get_transaction_data(get_received_data(ZADDRESS))))


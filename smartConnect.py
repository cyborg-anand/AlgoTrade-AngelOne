# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 14:22:30 2024

@author: METAZAPP
"""

from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp
import os
import urllib.request
import json
# =============================================================================
# import pandas as pd
# import datetime as dt
# import time
# =============================================================================

key_path="/media/anand/New Volume1/Anand/Stock market/AlgoTrading"
os.chdir(key_path)
key_secret=open("key.txt","r").read().split()

api_key = key_secret[0]
username = key_secret[1]
pwd = key_secret[2]
smartApi = SmartConnect(api_key)
feed_token = smartApi.getfeedToken()
token = key_secret[3]
totp = pyotp.TOTP(token).now()
data = smartApi.generateSession(username, pwd, totp)
feed_token = smartApi.getfeedToken()

instrument_url="https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response= urllib.request.urlopen(instrument_url)
instrument_list = json.loads(response.read())


def token_lookup(ticker, instrument_list, exchange="NSE"):
    for instrument in instrument_list:
        if instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[-1] == "EQ":
            return instrument["token"]
        
def place_limit_order(instrument_list, ticker, buy_sell, price, quantity, exchange="NSE"):
    params = {
                "variety":"NORMAL",
                "tradingsymbol":"{}-EQ".format(ticker),
                "symboltoken":token_lookup(ticker, instrument_list),
                "transactiontype":buy_sell,
                "exchange":"NSE",
                "ordertype":"LIMIT",
                "producttype":"INTRADAY",
                "duration":"DAY",
                "price":price,
                "quantity":quantity
                }
    limit_order = smartApi.placeOrder(params)
    return limit_order

def place_market_order(instrument_list,ticker,buy_sell,quantity,sl=0,sqof=0,exchange="NSE"):
    params = {
                "variety":"NORMAL",
                "tradingsymbol":"{}-EQ".format(ticker),
                "symboltoken":token_lookup(ticker, instrument_list),
                "transactiontype":buy_sell,
                "exchange":exchange,
                "ordertype":"MARKET",
                "producttype":"INTRADAY",
                "duration":"DAY",
                "quantity":quantity
                }
    market_order = smartApi.placeOrder(params)
    return market_order

place_limit_order(instrument_list, "IOB", "BUY", 55, 1)
place_market_order(instrument_list, "IOB", "BUY", 1)
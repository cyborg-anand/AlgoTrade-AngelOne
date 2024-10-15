# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 23:25:15 2024

@author: METAZAPP
"""
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import pyotp
import os
import urllib.request
import json
# =============================================================================
# import pandas as pd
# import datetime as dt
# import time
# =============================================================================

key_path=r"D:\Anand\Stock market\AlgoTrading"
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

# =============================================================================
# Get Historical Data
# =============================================================================
# tickers =["HDFCBANK","HCLTECH"]

# =============================================================================
# def token_lookup(ticker,instrument_list,exchange="NSE"):
#     for instrument in instrument_list:
#         if instrument["name"]== ticker and instrument["exch_seg"]==exchange and instrument["symbol"].split('-')[1]=="EQ":
#             return instrument["token"]
# =============================================================================

sws = SmartWebSocketV2(data["data"]["jwtToken"], key_secret[0], key_secret[2], feed_token)


correlation_id = "stream_1" #any string value which will help identify the specific streaming in case of concurrent streaming
action = 1 #1 subscribe, 0 unsubscribe
mode = 3 #1 for LTP, 2 for Quote and 2 for SnapQuote

token_list = [{"exchangeType": 1, "tokens": ["26009"]}]


def on_data(wsapp, message):
    print("Ticks: {}".format(message))


def on_open(wsapp):
    print("on open")
    sws.subscribe(correlation_id, mode, token_list)


def on_error(wsapp, error):
    print(error)



# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error

sws.connect()
# =============================================================================
# def symbol_lookup(token,instrument_list,exchange="NSE"):
#     for instrument in instrument_list:
#         if instrument["token"]== token and instrument["exch_seg"]==exchange and instrument["symbol"].split('-')[1]=="EQ":
#             return instrument["name"]                 
# =============================================================================
# =============================================================================
# def hist_data(ticker,duration,interval,instrument_list,exchange="NSE"):
#     params = {
#              "exchange": exchange,
#              "symboltoken": token_lookup(ticker,instrument_list),
#              "interval": interval,
#              "fromdate":(dt.date.today() - dt.timedelta(duration)).strftime("%Y-%m-%d %H:%M"),
#              "todate": dt.date.today().strftime("%Y-%m-%d %H:%M")
#              }
#     hist_data = smartApi.getCandleData(params)
#     df_data = pd.DataFrame(hist_data["data"],
#                            columns=["Date","Open","High","Low","Close","Volume"])
#     df_data.set_index("Date",inplace=True)
#     df_data.index = pd.to_datetime(df_data.index)
#     df_data.index = df_data.index.tz_localize(None)
#     return df_data
# 
# hdfc_data = hist_data("HDFCBANK",1000,"ONE_HOUR", instrument_list)
# =============================================================================
# Function to determine max days per request based on interval
# =============================================================================
# def get_max_days_per_request(interval):
#     interval_limits = {
#         "ONE_MINUTE": 30,
#         "THREE_MINUTE": 60,
#         "FIVE_MINUTE": 100,
#         "TEN_MINUTE": 100,
#         "FIFTEEN_MINUTE": 200,
#         "THIRTY_MINUTE": 200,
#         "ONE_HOUR": 400,
#         "ONE_DAY": 2000
#     }
#     return interval_limits.get(interval, 30)  # Default to 30 if interval is not found
# 
# # Function to fetch historical data in chunks if necessary
# def hist_data(ticker, total_days, interval, instrument_list, exchange="NSE"):
#     all_tickers_data = {}
#     for ticker in tickers:
#         all_data = []
#         token = token_lookup(ticker, instrument_list)
#         max_days_per_request = get_max_days_per_request(interval)
# 
#         # Loop through the data in chunks, if necessary
#         for i in range(0, total_days, max_days_per_request):
#             end_days = min(max_days_per_request, total_days - i)
#             start_date = (dt.date.today() - dt.timedelta(days=(total_days - i))).strftime("%Y-%m-%d %H:%M")
#             end_date = (dt.date.today() - dt.timedelta(days=(total_days - i - end_days))).strftime("%Y-%m-%d %H:%M")
# 
#             params = {
#                 "exchange": exchange,
#                 "symboltoken": token,
#                 "interval": interval,
#                 "fromdate": start_date,
#                 "todate": end_date
#             }
# 
#             hist_data = smartApi.getCandleData(params)
#             df_data = pd.DataFrame(hist_data["data"],
#                                    columns=["Date", "Open", "High", "Low", "Close", "Volume"])
#             df_data.set_index("Date", inplace=True)
#             df_data.index = pd.to_datetime(df_data.index)
#             df_data.index = df_data.index.tz_localize(None)
#             all_data.append(df_data)
#             # Introduce a light delay to prevent overwhelming the API
#             time.sleep(0.4)  # Adjust the sleep time as needed
# 
#         all_tickers_data[ticker] = pd.concat(all_data)
# 
#     return all_tickers_data
# 
# # Fetch historical data for multiple tickers for 1000 days
# tickers_data = hist_data(tickers, 3, "FIVE_MINUTE", instrument_list)
# =============================================================================
# =============================================================================
# Technical Analysis
# =============================================================================
# import numpy as np
# =============================================================================
# def EMA(ser, n=9):
#     multiplier = 2 / (n + 1)
#     sma = ser.rolling(n).mean()  # Calculate the initial Simple Moving Average
#     ema = np.full(len(ser), np.nan)  # Create an array of NaNs
#     start_index = len(sma) - len(sma.dropna())  # Find the start of non-NaN values
#     ema[start_index] = sma.dropna().iloc[0]  # Use iloc for positional indexing
#     
#     for i in range(start_index + 1, len(ser)):
#         if not np.isnan(ema[i - 1]):  # Only proceed if the previous value of EMA is not NaN
#             ema[i] = ((ser.iloc[i] - ema[i - 1]) * multiplier) + ema[i - 1]
#     
#     ema[start_index] = np.nan  # Set the first EMA value to NaN for alignment purposes
#     return pd.Series(ema, index=ser.index)
# =============================================================================
# RMA 
# =============================================================================
# def RMA(ser, n=9):
#     multiplier = 1/n
#     sma = ser.rolling(n).mean()  # Calculate the initial Simple Moving Average
#     rma = np.full(len(ser), np.nan)  # Create an array of NaNs
#     start_index = len(sma) - len(sma.dropna())  # Find the start of non-NaN values
#     rma[start_index] = sma.dropna().iloc[0]  # Use iloc for positional indexing
#     
#     for i in range(start_index + 1, len(ser)):
#         if not np.isnan(rma[i - 1]):  # Only proceed if the previous value of EMA is not NaN
#             rma[i] = ((ser.iloc[i] - rma[i - 1]) * multiplier) + rma[i - 1]
#     
#     rma[start_index] = np.nan  # Set the first EMA value to NaN for alignment purposes
#     return pd.Series(rma, index=ser.index)
# =============================================================================
# =============================================================================
# RSI indicator
# =============================================================================
# =============================================================================
# def RSI(df_dict, n=14):
#     "function to calculate RSI"
#     for df in df_dict:
#         df_dict[df]["change"] = df_dict[df]["Close"] - df_dict[df]["Close"].shift(1)
#         df_dict[df]["gain"] = np.where(df_dict[df]["change"]>=0, df_dict[df]["change"], 0)
#         df_dict[df]["loss"] = np.where(df_dict[df]["change"]<0, -1*df_dict[df]["change"], 0)
#         df_dict[df]["avgGain"] = RMA(df_dict[df]["gain"],n)
#         df_dict[df]["avgLoss"] = RMA(df_dict[df]["loss"],n)
#         df_dict[df]["rs"] = df_dict[df]["avgGain"]/df_dict[df]["avgLoss"]
#         df_dict[df]["rsi"] = 100 - (100/ (1 + df_dict[df]["rs"]))
#         df_dict[df].drop(["change","gain","loss","avgGain","avgLoss","rs"], axis=1, inplace=True)
#         
# RSI(tickers_data)
# =============================================================================
    
# =============================================================================
# MACD indicator
# =============================================================================

# manual calculation of EMA
# =============================================================================
# def MACD(df_dict, a=12,b=26,c=9):
#     for df in df_dict:
#         df_dict[df]["ma_fast"]=EMA(df_dict[df]["Close"],a)
#         df_dict[df]["ma_slow"]=EMA(df_dict[df]["Close"],b)
#         df_dict[df]["macd"]=df_dict[df]["ma_fast"] -  df_dict[df]["ma_slow"]
#         df_dict[df]["signal"] = EMA(df_dict[df]["macd"],c)
#         df_dict[df]["histogram"]=df_dict[df]["macd"] - df_dict[df]["signal"]
#         df_dict[df].drop(["ma_fast","ma_slow"],axis=1, inplace=True)
#         
# MACD(tickers_data)
# =============================================================================

# python calculation of EMA (ewm) 
# =============================================================================
# def MACD(df_dict, a=12,b=26,c=9):
#     for df in df_dict:
#         df_dict[df]["ma_fast"]=df_dict[df]["Close"].ewm(span=a, min_periods=a).mean()
#         df_dict[df]["ma_slow"]=df_dict[df]["Close"].ewm(span=b, min_periods=b).mean()
#         df_dict[df]["macd"]=df_dict[df]["ma_fast"] -  df_dict[df]["ma_slow"]
#         df_dict[df]["signal"] = df_dict[df]["macd"].ewm(span=c, min_periods=c).mean()
#         df_dict[df]["histogram"]=df_dict[df]["macd"] - df_dict[df]["signal"]
#         df_dict[df].drop(["ma_fast","ma_slow"],axis=1, inplace=True)
# MACD(tickers_data)
# =============================================================================

# =============================================================================
# Bollinger Band
# =============================================================================
# =============================================================================
# def bollinger_band(df_dict,n=20):
#     for df in df_dict:
#         df_dict[df]["MB"]=df_dict[df]["Close"].rolling(n).mean()
#         df_dict[df]["UB"]=df_dict[df]["MB"] + 2*df_dict[df]["Close"].rolling(n).std(ddof=0)
#         df_dict[df]["LB"]=df_dict[df]["MB"] - 2*df_dict[df]["Close"].rolling(n).std(ddof=0)
#         df_dict[df]["BB_Width"] = df_dict[df]["UB"] - df_dict[df]["LB"]
# bollinger_band(tickers_data)
# =============================================================================
# =============================================================================
# ATR Indicator
# =============================================================================
# =============================================================================
# def ATR(df_dict, n=14):
#     "function to calculate True Range and Average True Range"
#     for df in df_dict:
#         df_dict[df]["H-L"] = df_dict[df]["High"] - df_dict[df]["Low"]
#         df_dict[df]["H-PC"] = abs(df_dict[df]["High"] - df_dict[df]["Close"].shift(1))
#         df_dict[df]["L-PC"] = abs(df_dict[df]["Low"] - df_dict[df]["Close"].shift(1))
#         df_dict[df]["TR"] = df_dict[df][["H-L","H-PC","L-PC"]].max(axis=1, skipna=False)
#         df_dict[df]["ATR"] = EMA(df_dict[df]["TR"], n)  # df_dict[df]["TR"].ewm(span=n, min_periods=n).mean()  
#         df_dict[df].drop(["H-L","H-PC","L-PC","TR"], axis=1, inplace=True)
# 
# ATR(tickers_data)
# =============================================================================
# =============================================================================
# stochastic Oscillator
# =============================================================================
# =============================================================================
# def stochastic(df_dict, lookback=14, k=1, d=3):
#     """function to calculate Stochastic Oscillator
#        lookback = lookback period
#        k and d = moving average window for %K and %D"""
#     for df in df_dict:
#         df_dict[df]["HH"] = df_dict[df]["High"].rolling(lookback).max()
#         df_dict[df]["LL"] = df_dict[df]["Low"].rolling(lookback).min()
#         df_dict[df]["%K"] = (100 * (df_dict[df]["Close"] - df_dict[df]["LL"])/(df_dict[df]["HH"]-df_dict[df]["LL"])).rolling(k).mean()
#         df_dict[df]["%D"] = df_dict[df]["%K"].rolling(d).mean()
#         df_dict[df].drop(["HH","LL"], axis=1, inplace=True)
#         
# stochastic(tickers_data)
# =============================================================================









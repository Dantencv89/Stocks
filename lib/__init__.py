import os
import io
import requests
import pandas as  pd
import yfinance as  yf
from datetime import  datetime
import matplotlib.pyplot as  plt
hostPROD = os.environ.get('IEX_HOST_PROD')
access_key_prd = os.environ.get('IEX_PUBLIC_KEY_PROD')
secret_key_prd = os.environ.get('IEX_SECRET_KEY_PROD')

# ##### Host & Keys IEX SAND

hostSAND = os.environ.get('IEX_HOST_SAND')
access_key_snd = os.environ.get('IEX_PUBLIC_KEY_SAND')
secret_key_snd = os.environ.get('IEX_SECRET_KEY_SAND')

 ##### Custom Libraries
from lib.lib_database.database_functions import connect, get_connector, get_cursor, create_companies, create_dailystocks 
from lib.get_symbols.master_symbols import request_symbols,get_symbols_master, getSymbolsArrays, get_symbols_master_database
from lib.get_stock_data.get_stock_data import get_all_stock_prices, get_company_stock_prices

connect(True)




import os
import io
import requests
import pandas as  pd
import yfinance as  yf
from datetime import datetime, timedelta

g_date_format='%Y-%m-%d'

def companies_file_path(_exchange,_symbol):
    return os.path.join(os.getcwd(),'stocks_data','stock_daily_price',str.lower(_exchange), str.upper(_symbol) + '.csv')


def get_company_stock_prices(_symbol,_exchange, _initial_start, _interval='1d',_actions= True):
    ## period --> “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
    ## interval --> “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
    ## start: If not using period – in the format (yyyy-mm-dd) or datetime.
    ## end: If not using period – in the format (yyyy-mm-dd) or datetime.
    ## actions : Download stock dividends and stock splits events? (Default is True)
    ### header=0 ,names =['Date','Open','High','Low Close','Volume','Dividends','Stock Splits','symbol'] 
    _start = _initial_start;
    _exist_symbol_csv_file = os.path.exists(companies_file_path(_exchange,_symbol));
    _exist_old_data = False
    _columns = ['Date','Open','High','Low','Close','Volume','Dividends','Stock Splits','symbol'];
    if (_exist_symbol_csv_file):
        try:
            _ticket_old_data = pd.read_csv(companies_file_path(_exchange,_symbol))
            if (_ticket_old_data.shape[0]>0):
                _start = str((datetime.strptime(max(_ticket_old_data.Date),g_date_format) + timedelta(days=1)).strftime(g_date_format))
                _exist_old_data = True
        except:
            print("An exception occurred trying to read to csv this file --> ",companies_file_path(_exchange,_symbol))

    if ((datetime.strptime(_start,g_date_format)).timestamp()<(datetime.now()).timestamp()):
        _ticket=yf.Ticker(_symbol)
        _ticket_data= _ticket.history(start=_start, interval=_interval, actions=_actions)
        if (_ticket_data.shape[0]>0):
            _ticket_data['symbol']= _symbol
            _ticket_data.reset_index(inplace=True)
            _ticket_data['Date'] = _ticket_data['Date'].dt.strftime(g_date_format)
            if(_exist_old_data):
                if (_ticket_old_data.shape[0]>0):
                    _ticket_data= pd.concat([_ticket_old_data, _ticket_data], verify_integrity=False, sort=False, ignore_index=True) 
            return _ticket_data[_columns];
    elif(_exist_old_data):
        return _ticket_old_data[_columns];
    
    return pd.DataFrame(columns= _columns, data= None)
    
def get_all_stock_prices(_symbols,_exchange ,_start):
    _starttime = datetime.now(); 
    print('Start --- Get All symbols master from: ', _start, ' - Time: ', _starttime)
    ##_iter=0
    for _indx, _symbol in _symbols.items():
        _df= get_company_stock_prices(_symbol,_exchange, _start)
        if(_df.shape[0]>0):
            _df.to_csv(path_or_buf=companies_file_path(_exchange,_symbol),index=False, date_format=g_date_format)
        # if (_iter==0):
        #     _mdf = _df.copy()
        # else:
        #     _mdf= _mdf.append(_df.copy(), ignore_index=True) 
        # _iter += 1;
    _endtime = datetime.now(); 
    print('Total time all NASDAQ from - ', _start , ' - : ', (_starttime - _endtime).total_seconds())
    print('End --- Get All symbols master from: ', _start, ' - Time:  ', _endtime)
    
    
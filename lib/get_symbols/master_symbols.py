import os
import io
import requests
import pandas as pd
import yfinance as  yf
from datetime import datetime, timedelta

def companies_file_path(name):
        return os.path.join(os.getcwd(),'stocks_data','companies','companies_' + str.lower(name) + '_.csv')


def getSymbolsArrays(_symbols,_len=200):
    _symbols_str='';
    _symbols_arr=[];
    pos = 0
    for indx, symbol in _symbols.iterrows(): 
        _symbols_str += symbol.symbol + ','
        if len(_symbols_str)>_len:
            _symbols_arr.append(_symbols_str[0:len(_symbols_str)-1])
            _symbols_str=''
    return _symbols_arr

def get_symbols_master(_symbols,_host, _access_key,filename='master',_len=200):
    _symbols_arr = getSymbolsArrays(_symbols,_len)
    _indx=0;
    for _symbols in _symbols_arr:
        _companies = requests.get('https://' + _host + '/stable/stock/market/company',params={'symbols':_symbols,'format':'csv','token': _access_key})
        _companiesDF = pd.read_csv(io.StringIO(_companies.content.decode('utf-8')))
        if (_indx==0):
            _MasterCompaniesDF = _companiesDF.copy()
        else:
            _MasterCompaniesDF= _MasterCompaniesDF.append(_companiesDF, ignore_index=True)
        _indx+=1;
    ##################### out of for -- save Master Companies:
    _MasterCompaniesDF.to_csv(path_or_buf=companies_file_path(filename))
    print('Get All symbols master from ', filename, ' - ', datetime.now())
    return _MasterCompaniesDF



def request_symbols(_host, _access_key, _exchange, _type=''):
    ##GET /ref-data/symbols
    response = requests.get('https://' + _host + '/stable/ref-data/symbols',
                        params={
                                'format':'csv',
                                'token': _access_key})

    symbols= pd.read_csv(io.StringIO(response.content.decode('utf-8')));
    symbols = symbols[(symbols['exchange']==_exchange)];
    if(_type!=''):
        symbols = symbols[(symbols['type']==_type)];
    _save_file= os.path.join(os.getcwd(),'stocks_data','symbols_' + str.lower(_exchange)+'.csv')
    symbols.to_csv(path_or_buf=_save_file)
    print('Exchange', _exchange ,' - Symbols size - Type:', _type)
    return symbols;


def get_symbols_master_database(_symbols,_exchange):
    print('Start -- Save All symbols master to DB ' ,' - ', datetime.now())
    _MasterCompaniesDF = pd.DataFrame(columns=['symbol','name','exchange','sector','trailing_pe','forward_pe','marketcap','summary'])
    for index, row  in _symbols.iterrows():
        _ticketinfo = yf.Ticker(row['symbol']).info
        _MasterCompaniesDF= _MasterCompaniesDF.append({'symbol': row['symbol'],
                                                        'name':_ticketinfo['shortName'],
                                                        'exchange':_exchange,
                                                        'sector':_ticketinfo['sector'],
                                                        'trailing_pe':_ticketinfo['trailingPE'],
                                                        'forward_pe':_ticketinfo['forwardPE'],
                                                        'marketcap':_ticketinfo['marketCap'],
                                                        'summary':_ticketinfo['longBusinessSummary']}, 
                                                    ignore_index=True)
    ##################### out of for -- save Master Companies:
    print('End -- Save All symbols master to DB ' ,' - ', datetime.now())
    return _MasterCompaniesDF



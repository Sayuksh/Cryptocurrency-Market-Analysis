from coinmetrics.api_client import CoinMetricsClient
import pandas as pd
import requests
import time
from datetime import datetime,timedelta,date
apiUrl="https://api.pro.coinbase.com"
client=CoinMetricsClient()


def format_Date(str_date):
    date_obj = datetime.strptime(str_date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%Y-%m-%d')

    # Convert datetime object to ISO format
    iso_string = date_obj.isoformat()
    return iso_string


def get_data_from_coinmetrics(coin,start_date,end_date):
    metrics=client.get_asset_metrics(
    assets=coin,
    metrics=["TxTfrValMedUSD",
             "TxCnt",
            "FeeTotUSD",
            "FeeMedUSD",
            "AdrActCnt",
            "DiffMean",
            "BlkCnt",
            "BlkSizeMeanByte",
            "SplyCur",
            "TxTfrCnt",
            "TxTfrValAdjUSD",
            ],
    start_time=start_date,
    end_time=end_date,
    frequency="1d"
    )
    coin_metric_data=pd.DataFrame(metrics)
    coin_metric_data['Date'] = pd.to_datetime(coin_metric_data['time'].str.replace('Z', ''), format='%Y-%m-%dT%H:%M:%S.%f')
    coin_metric_data['Date'] = pd.to_datetime(coin_metric_data['Date'], unit='s')
    coin_metric_data['BTC / Transactions, transfers, value, median, USD']=coin_metric_data["TxTfrValMedUSD"]
    coin_metric_data['BTC / Transactions, count']=coin_metric_data["TxTfrValMedUSD"]
    coin_metric_data['BTC / Fees, total, USD']=coin_metric_data["FeeTotUSD"]
    coin_metric_data['BTC / Fees, transaction, median, USD']=coin_metric_data["FeeMedUSD"]
    coin_metric_data['BTC / Addresses, active, count']=coin_metric_data['AdrActCnt']
    coin_metric_data['BTC / Difficulty, mean']=coin_metric_data['DiffMean']
    coin_metric_data['BTC / Block, count']=coin_metric_data['BlkCnt']
    coin_metric_data['BTC / Block, size, mean, bytes']=coin_metric_data['BlkSizeMeanByte']
    coin_metric_data['BTC / Supply, current']=coin_metric_data["SplyCur"]
    coin_metric_data["BTC / Transactions, transfers, count"]=coin_metric_data["TxTfrCnt"]
    coin_metric_data['BTC / Transactions, transfers, value, adjusted, USD']=coin_metric_data["TxTfrValAdjUSD"]
    coin_metric_data=coin_metric_data[["Date",
                                       'BTC / Transactions, transfers, value, median, USD',
                                       'BTC / Transactions, count', 
                                       'BTC / Fees, total, USD',
                                       'BTC / Fees, transaction, median, USD',
                                       'BTC / Addresses, active, count', 
                                       'BTC / Difficulty, mean',
                                       'BTC / Block, count', 
                                       'BTC / Block, size, mean, bytes',
                                       'BTC / Supply, current', 
                                       'BTC / Transactions, transfers, count',
                                       'BTC / Transactions, transfers, value, adjusted, USD']]
    return coin_metric_data
    
def get_data_from_coinbase(coin,start_date,end_date):
    
    start_date=format_Date(start_date)
    end_date=format_Date(end_date)
    
    sym=f"{coin}-USD"
    barSize="86400"
    timestart=start_date
    delta=timedelta(days=1)
    timeEnd=end_date
    

    parameters={
        'start':timestart,
        'end':timeEnd,
        "granularity":barSize, 
    }
    data=requests.get(f"{apiUrl}/products/{sym}/candles",
                      params=parameters,
                      headers={
                          "content-type":"application/json"
                      })
    df=pd.DataFrame(data.json(),
                    columns=["time","low","high","open","close","volume"])
    df['Date']= pd.to_datetime(df['time'],unit='s')
    df =df[["Date","low","high","open","close","volume"]]
    return df
    

def get_api_data(coin,start_date,end_date):
    coin_metric_data=get_data_from_coinmetrics(coin=coin,start_date=start_date,end_date=end_date)
    coinbase_data= get_data_from_coinbase(coin=coin,start_date=start_date,end_date=end_date)
    coin_metric_data['Open']=coinbase_data['open']
    coin_metric_data['High']=coinbase_data['high']
    coin_metric_data['Low']=coinbase_data['low']
    coin_metric_data['Close']=coinbase_data['close']
    coin_metric_data['Volume']=coinbase_data["volume"]
    
    data=coin_metric_data
    return data
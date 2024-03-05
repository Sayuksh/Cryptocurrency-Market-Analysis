import talib
import pandas as pd
import numpy as np
#Relative Strength Index (RSI):
def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

#Exponential Moving Avgerage
def calculate_ema(data, column_name, window):
    alpha = 2 / (window + 1)
    data['EMA_' + str(window)] = data[column_name].ewm(span=window, adjust=False).mean()

#Moving Average Convergence Divergence (MACD)
def calculate_macd(data):
    # Calculate MACD using the closing prices
    macd, signal, _ = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return  macd, signal


#Bollinger Bands
def calculate_bollinger_bands(data):
    # Calculate Bollinger Bands using the closing prices
    upper_band, _, lower_band = talib.BBANDS(data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2)
    return upper_band,lower_band


#Stochastic Oscillator
def calculate_stochastic_oscillator(data, period_k, period_d):
    # Calculate %K
    Lowest_Low= data['Low'].rolling(window=period_k).min()
    Highest_High = data['High'].rolling(window=period_k).max()
    K = ((data['Close'] - Lowest_Low) / (Highest_High - Lowest_Low)) * 100

    # Calculate %D (3-period simple moving average of %K)
    D = K.rolling(window=period_d).mean()
    return K,D

#Williams %R
def calculate_williams_percent_r(data, period):
    # Calculate Highest High and Lowest Low over the specified period
    Highest_High = data['High'].rolling(window=period).max()
    Lowest_Low = data['Low'].rolling(window=period).min()

    # Calculate Williams %R
    R = -100 * (Highest_High - data['Close']) / (Highest_High-Lowest_Low)
    return R


#Aroon Oscillator
def calculate_Aroon_Oscillator(data,period):
    Aroon_Up = data['High'].rolling(window=period).apply(lambda x: x.argmax() / float(period) * 100, raw=True)
    Aroon_Down= data['Low'].rolling(window=period).apply(lambda x: x.argmin() / float(period) * 100, raw=True)

    # Calculate Aroon Oscillator
    Aroon_Oscillator = Aroon_Up - Aroon_Down
    return  Aroon_Oscillator

def feature_engieering(data):
    data['RSI']=calculate_rsi(data)
    calculate_ema(data, 'Close', window=20)
    data['MACD'],_=calculate_macd(data)
    data["upper_bond"],_=calculate_bollinger_bands(data)
    data['%K'],_=calculate_stochastic_oscillator(data,period_k=14, period_d=3)
    data['%R']=calculate_williams_percent_r(data,period=14)
    data[' Aroon_Oscillator']=calculate_Aroon_Oscillator(data,period=14)
    data['Date'] = pd.to_datetime(data['Date'])
    data['day'] = data['Date'].dt.day_name()
    day_mapping = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    data['day']=data['day'].replace(day_mapping)
    data['Parkinson Volatility']=np.sqrt(((np.log((data['High']/data['Low']))**2)/(4*np.log(2))))
    data=data.drop(columns=['Date'])
    
    return data
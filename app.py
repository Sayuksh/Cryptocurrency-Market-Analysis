from flask import Flask,jsonify,render_template
from datetime import datetime
import requests

app=Flask(__name__)
COINGECKO_API_URL = 'https://api.coingecko.com/api/v3/coins'

@app.route('/')

def welcome():
    return render_template("head.html")

@app.route('/bitcoin')
def bitcoin_data():
    now = datetime.now()
    print('Date and Time is:', now)

    timestamp = datetime.timestamp(now)
    print("timestamp =", timestamp)
    response = requests.get(f"{COINGECKO_API_URL}/bitcoin")
    bitcoin_data = response.json()

    # Extract relevant information
    name = bitcoin_data['name']
    symbol = bitcoin_data['symbol']
    current_price = bitcoin_data['market_data']['current_price']['usd']
    market_cap = bitcoin_data['market_data']['market_cap']['usd']
    high_24h = bitcoin_data['market_data']['high_24h']['usd']
    low_24h = bitcoin_data['market_data']['low_24h']['usd']
    return render_template('index.html', name=name, symbol=symbol,date_and_time=str(now) ,current_price=current_price,
                           market_cap=market_cap, high_24h=high_24h, low_24h=low_24h)

@app.route('/ethereum')
def ethereum_data():
    now = datetime.now()
    print('Date and Time is:', now)

    timestamp = datetime.timestamp(now)
    print("timestamp =", timestamp)
    response = requests.get(f"{COINGECKO_API_URL}/ethereum")
    ethereum_data = response.json()

    # Extract relevant information
    name = ethereum_data['name']
    symbol = ethereum_data['symbol']
    current_price = ethereum_data['market_data']['current_price']['usd']
    market_cap = ethereum_data['market_data']['market_cap']['usd']
    high_24h = ethereum_data['market_data']['high_24h']['usd']
    low_24h = ethereum_data['market_data']['low_24h']['usd']
    return render_template('index.html', name=name, symbol=symbol,date_and_time=str(now) ,current_price=current_price,
                           market_cap=market_cap, high_24h=high_24h, low_24h=low_24h)

if __name__=='__main__':
    app.run(debug=True)
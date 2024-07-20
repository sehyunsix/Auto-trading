import requests
from datetime import datetime, timedelta
import time
import pandas as pd

def get_data(start_date, end_date):

    result = requests.get('https://api.binance.com/api/v3/ticker/price')
    js = result.json()
    symbols = [x['symbol'] for x in js]
    symbols_usdt = [x for x in symbols if 'BTCUSDC' in x]
    symbol = symbols_usdt[0]

    COLUMNS = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'quote_av', 'trades', 
                    'tb_base_av', 'tb_quote_av', 'ignore']
    URL = 'https://api.binance.com/api/v3/klines'

    data = []
    
    start = int(time.mktime(datetime.strptime(start_date + ' 00:00', '%Y-%m-%d %H:%M').timetuple())) * 1000
    end = int(time.mktime(datetime.strptime(end_date +' 23:59', '%Y-%m-%d %H:%M').timetuple())) * 1000
    params = {
        'symbol': symbol,
        'interval': '1m',
        'limit': 1000,
        'startTime': start,
        'endTime': end
    }
    
    while start < end:
        params['startTime'] = start
        result = requests.get(URL, params=params)
        if result.status_code != 200:
            raise ValueError(f"Error fetching data from API: {result.status_code} - {result.text}")
        js = result.json()
        if not js:
            break
        data.extend(js)
        start = js[-1][0] + 60000
    if not data:
        raise ValueError("No data available for the given date range.")
    
    df = pd.DataFrame(data)
    df.columns = COLUMNS
    df['Open_time'] = df.apply(lambda x: datetime.fromtimestamp(x['Open_time'] // 1000), axis=1)
    df = df.drop(columns=['Close_time', 'ignore'])
    df['Symbol'] = symbol
    df.loc[:, 'Open':'tb_quote_av'] = df.loc[:, 'Open':'tb_quote_av'].astype(float)
    df['trades'] = df['trades'].astype(int)
    return df

# end_date = datetime.now().strftime('%Y-%m-%d')
# start_date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

# symbol = symbols_usdt[0]
# print(get_data(start_date, end_date, symbol))
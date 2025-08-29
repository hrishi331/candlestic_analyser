import pandas as pd
import yfinance as yf 
import nsepython as nse
import numpy as np
import datetime
import requests

# For telegram bot messages
BOT_TOKEN_15m = "<your access token by BOTFATHER>" # 15_m telegram bot
CHAT_ID = "<your chatID>"  # Replace with your chat ID
url_15m = f"https://api.telegram.org/bot{BOT_TOKEN_15m}/sendMessage"



end_row = datetime.date.today()+datetime.timedelta(days=1)
start_row = end_row-datetime.timedelta(days=180)

formatted_end = end_row.strftime(format="%Y-%m-%d")
formatted_start = start_row.strftime(format="%Y-%m-%d")

df = yf.download(tickers='^NSEI',
                 start=formatted_start,
                 end=formatted_end,
                 ignore_tz=True,
                 multi_level_index=False)
df.drop("Volume",axis=1,inplace=True)

# For hourly check need hourly latest reading and candles

end_row1 = datetime.date.today()+datetime.timedelta(days=1)
start_row1 = end_row1-datetime.timedelta(days=5)

formatted_end1 = end_row1.strftime(format="%Y-%m-%d")
formatted_start1 = start_row1.strftime(format="%Y-%m-%d")

df_15m = yf.download(tickers='^NSEI',
                 start=formatted_start1,
                 end=formatted_end1,
                 ignore_tz=True,
                 multi_level_index=False,interval="15m")

m15_prev_close = df_15m['Close'].iloc[-2]
m15_prev_low = df_15m['Low'].iloc[-2] 
m15_prev_high = df_15m['High'].iloc[-2] 




support_range = (m15_prev_low-500,m15_prev_low)
resistance_range = (m15_prev_high+500,m15_prev_high)

# Support calculations
support_data = df[(df['Low']>=support_range[0]) & (df['Low']<support_range[1])]


low_data = support_data[['Low']]
low_data.loc[:,'Low'] = round(support_data['Low']/25)*25

low_count = low_data['Low'].value_counts().reset_index()

for n in range(2,10):
    lcounts = low_count['count'].nlargest(n)
    if len(lcounts)>1:
        break


support_levels = low_count[low_count['count'].isin(lcounts)]['Low']
print("Support levels",support_levels.values)

# Resistance calculations
resistance_data = df[(df['High']<=resistance_range[0]) & (df['High']>resistance_range[1])]


high_data = resistance_data[['High']]
high_data.loc[:,'High'] = round(resistance_data['High']/25)*25
high_count = high_data['High'].value_counts().reset_index()

for n1 in range(2,10):
    hcounts = low_count['count'].nlargest(n1)
    if len(hcounts)>1:
        break

resistance_levels = high_count[high_count['count'].isin(hcounts)]['High']
print("Resistance levels : ",resistance_levels.values)


# Check CMP @ support
current_low_rounded = round(m15_prev_low/25)*25
current_price_rounded = round(m15_prev_close/25)*25
sp = [current_low_rounded,current_price_rounded]
for i in support_levels:
    if i==current_low_rounded:
        message1 = f"Low at support : {i}"
        payload1 = {
        "chat_id": CHAT_ID,
        "text": message1
        }
        rh = requests.post(url_15m, data=payload1)
        print("Message sent!" if rh.status_code == 200 else "Failed:", rh.text)

    if i==current_price_rounded:
        message2 = f"Close at support : {i}"
        payload2 = {
        "chat_id": CHAT_ID,
        "text": message2
        }
        rh = requests.post(url_15m, data=payload2)
        print("Message sent!" if rh.status_code == 200 else "Failed:", rh.text)






# Check CMP @ resistance
current_high_rounded = round(m15_prev_high/25)*25
current_price_rounded = round(m15_prev_close/25)*25
rs = [current_high_rounded,current_price_rounded]
for i in resistance_levels:
    if i==current_high_rounded:
        message3 = f"High at resistance : {i}"
        payload3 = {
        "chat_id": CHAT_ID,
        "text": message3
        }
        rh = requests.post(url_15m, data=payload3)
        print("Message sent!" if rh.status_code == 200 else "Failed:", rh.text)
    if i==current_price_rounded:
        message4 = f"Close at resistance : {i}"
        payload4 = {
        "chat_id": CHAT_ID,
        "text": message4
        }
        rh = requests.post(url_15m, data=payload4)
        print("Message sent!" if rh.status_code == 200 else "Failed:", rh.text)


# m15_prev_close,m15_prev_low,m15_prev_high

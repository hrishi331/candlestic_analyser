import yfinance as yf
from datetime import datetime,timedelta
import talib as ta
import requests

# For telegram bot messages
BOT_TOKEN = "<your access token by BOTFATHER>" # replace with your own
CHAT_ID = "1163765818"  # Replace with your chat ID
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

today = datetime.today()
start = today - timedelta(days=40)
end = today + timedelta(days=1)

df = yf.download(tickers="^NSEI",
                 start=start,
                 end=end,
                 interval="1d",
                 ignore_tz=True,
                 multi_level_index=False)

df.drop("Volume",axis=1,inplace=True)

talib_pattern_signals = {
    "CDL2CROWS": "Bearish",
    "CDL3BLACKCROWS": "Bearish",
    "CDL3INSIDE": "Both",
    "CDL3LINESTRIKE": "Both",
    "CDL3OUTSIDE": "Both",
    "CDL3STARSINSOUTH": "Bullish",
    "CDL3WHITESOLDIERS": "Bullish",
    "CDLABANDONEDBABY": "Both",
    "CDLADVANCEBLOCK": "Bearish",
    "CDLBELTHOLD": "Both",
    "CDLBREAKAWAY": "Both",
    "CDLCLOSINGMARUBOZU": "Both",
    "CDLCONCEALBABYSWALL": "Bullish",
    "CDLCOUNTERATTACK": "Both",
    "CDLDARKCLOUDCOVER": "Bearish",
    "CDLDOJI": "Neutral",
    "CDLDOJISTAR": "Neutral",
    "CDLDRAGONFLYDOJI": "Neutral",
    "CDLENGULFING": "Both",
    "CDLEVENINGDOJISTAR": "Bearish",
    "CDLEVENINGSTAR": "Bearish",
    "CDLGAPSIDESIDEWHITE": "Both",
    "CDLGRAVESTONEDOJI": "Neutral",
    "CDLHAMMER": "Bullish",
    "CDLHANGINGMAN": "Bearish",
    "CDLHARAMI": "Both",
    "CDLHARAMICROSS": "Both",
    "CDLHIGHWAVE": "Neutral",
    "CDLHIKKAKE": "Both",
    "CDLHIKKAKEMOD": "Both",
    "CDLHOMINGPIGEON": "Bullish",
    "CDLIDENTICAL3CROWS": "Bearish",
    "CDLINNECK": "Bearish",
    "CDLINVERTEDHAMMER": "Bullish",
    "CDLKICKING": "Both",
    "CDLKICKINGBYLENGTH": "Both",
    "CDLLADDERBOTTOM": "Bullish",
    "CDLLONGLEGGEDDOJI": "Neutral",
    "CDLLONGLINE": "Both",
    "CDLMARUBOZU": "Both",
    "CDLMATCHINGLOW": "Bullish",
    "CDLMATHOLD": "Bullish",
    "CDLMORNINGDOJISTAR": "Bullish",
    "CDLMORNINGSTAR": "Bullish",
    "CDLONNECK": "Bearish",
    "CDLPIERCING": "Bullish",
    "CDLRICKSHAWMAN": "Neutral",
    "CDLRISEFALL3METHODS": "Both",
    "CDLSEPARATINGLINES": "Both",
    "CDLSHOOTINGSTAR": "Bearish",
    "CDLSHORTLINE": "Both",
    "CDLSPINNINGTOP": "Neutral",
    "CDLSTALLEDPATTERN": "Bearish",
    "CDLSTICKSANDWICH": "Bullish",
    "CDLTAKURI": "Bullish",
    "CDLTASUKIGAP": "Both",
    "CDLTHRUSTING": "Bearish",
    "CDLTRISTAR": "Both",
    "CDLUNIQUE3RIVER": "Bullish",
    "CDLUPSIDEGAP2CROWS": "Bearish",
    "CDLXSIDEGAP3METHODS": "Both"
}


for i in talib_pattern_signals.keys():
    func = getattr(ta,i)
    df[i] = func(df['Open'],df['High'],df['Low'],df['Close'])

df.drop(['Open','High','Low','Close'],axis=1,inplace=True)

l = []
for k,v in zip(df.iloc[-1].keys(),df.iloc[-1].values):
    if v==100:
        k = k.replace("CDL","")
        l.append(f"{k} : Bullish")
    elif v==-100:
        k = k.replace("CDL","")
        l.append(f"{k} : Bearish")
    else:
        pass


t = df.iloc[-1:].index


print(f"@ {t[0]}")


if len(l)==0:
    # print("No pattern detected!")
    message="No pattern detected!"
    payload = {
    "chat_id": CHAT_ID,
    "text": message
    }

    r = requests.post(url, data=payload)
    print("Message sent!" if r.status_code == 200 else "Failed:", r.text)
else:
    text = ''
    for i in l:
        text = text + i + '\n'
        
    text = text + f"@ {t[0]}"
    message = text
    payload = {
    "chat_id": CHAT_ID,
    "text": message
    }

    r = requests.post(url, data=payload)
    print("Message sent!" if r.status_code == 200 else "Failed:", r.text)


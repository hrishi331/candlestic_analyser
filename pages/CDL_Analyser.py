import yfinance as yf
from datetime import datetime,timedelta
import talib as ta
from pushbullet import Pushbullet 
import pandas as pd
import streamlit as st


st.header("Candlestick Pattern Detector".upper())

# Select script
script = st.radio(label="Select script" , options=['NIFTY 50','NIFTY BANK'])
script_dict = {'NIFTY 50' : "^NSEI",'NIFTY BANK': "^NSEBANK"}


# Select data window
st.write("Select time window")
col1,col2 = st.columns(spec=2)
start = col1.date_input("From [inclusive]")
end = col2.date_input("To [exclusive]")

if start==end:
    st.stop()
else:
    pass

# Select time frame 
options1 = ['5m','15m','30m','1h','1d','1wk']


timeframe = st.radio(label="Select time-frame",options=options1)


df = yf.download(tickers=script_dict[script],
                 start=start,
                 end=end,
                 interval=timeframe,
                 ignore_tz=True,
                 multi_level_index=False)

if df.shape[0]>0:
    st.write("Data retrieved!")
else:
    st.write("Data window too large!")
    st.stop()

df.drop("Volume",axis=1,inplace=True)
print(df)
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

latest_index =df.iloc[-2:].index
t = []
p = []
for i in df.index:
    for j in df:
        val = df.loc[i,j]
        if val==100:
            # print(f"{i} : {j.replace("CDL","")} - Bullish")
            t.append(i)
            if talib_pattern_signals[j] == "Both":
                p.append(f"{j.replace("CDL","")} - Bullish")
            else:
                p.append(f"{j.replace("CDL","")} - {talib_pattern_signals[j]}")
        elif val == -100:
            # print(f"{i} : {j.replace("CDL","")} - Bearish")
            t.append(i)
            if talib_pattern_signals[j] == "Both":
                p.append(f"{j.replace("CDL","")} - Bearish")
            else:
                p.append(f"{j.replace("CDL","")} - {talib_pattern_signals[j]}")
        else:
            # print(f"{i} : No Pattern")
            t.append(i)
            p.append("No Pattern")

table = pd.DataFrame({"Timestamp" : t , "Pattern" : p})
table.drop_duplicates(inplace=True)
options2 = table['Timestamp'].iloc[::-1].unique()


ts = st.selectbox(label="Find candlestick pattern at specific timestamp : ",options=options2)
data = table[table['Timestamp']==ts]['Pattern'].values



if len(data)>1:
    for i in data:
        if i=="No Pattern":
            pass
        else:
            st.write(i)
else:
    for i in data:
        st.write(i)

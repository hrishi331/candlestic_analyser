import yfinance as yf 
import streamlit as st 
import pandas as pd 
import datetime


st.header("Index EDA")

script_input = st.radio("Select index : ",['NIFTY 50','BANK NIFTY'])
indices = {"NIFTY 50" : "^NSEI",
           "BANK NIFTY" : "^NSEBANK"}

script = indices[script_input]

# col1,col2 = st.columns(spec=2)
# start = col1.date_input("Select start date : ")
# end = col2.date_input("Select end date : ")

period = st.radio("Select period : ",options=['1y','2y','5y','10y','ytd','max'])

df = yf.download(tickers=script,
                 multi_level_index=False,
                 period = period)

st.write(df)
df.drop("Volume",axis=1,inplace=True)

for i in df:
    df[i] = df[i].pct_change()*100

df['Date'] = df.index
df['Month'] = df['Date'].dt.month_name()
df['Weekno'] = df['Date'].dt.isocalendar().week
df['Year'] = df['Date'].dt.year




data = df[['Close','Month','Weekno']]
data.index = [i for i in range(data.shape[0])]
st.write(data)

def n_day_ahead(df,n):
    for i in range(df.shape[0]):
        data = df.iloc[i+1:i+n+1,0]
        if all(i>0 for i in data):
            df.loc[i,f'{n}DayAhead'] = "Rally"
        elif all(i<0 for i in data):
            df.loc[i,f'{n}DayAhead'] = "Fall"
        else :
            df.loc[i,f'{n}DayAhead'] = "NA"
    return df

data1 = n_day_ahead(data,3)
data1 = n_day_ahead(data1,5)

months = ['January','February','March',
          'April','May','June','July',
          'August','September','October',
          'November','December']

st.subheader("Monthly analysis")
month_data = data1[['Month','3DayAhead']]
result1 = month_data.groupby(by=['Month','3DayAhead'])[['3DayAhead']].count()
result1.rename({"3DayAhead":"count"},inplace=True,axis=1)
with st.expander("Next 3 day"):
    st.html(result1)   


month_data = data1[['Month','5DayAhead']]
result1 = month_data.groupby(by=['Month','5DayAhead'])[['5DayAhead']].count()
result1.rename({"5DayAhead":"count"},inplace=True,axis=1)
with st.expander("Next 5 day"):
    st.html(result1)     


data2 = df[['Close','Month']]
result = data2.groupby(by='Month')['Close'].agg(['mean','std'])
with st.expander(label="mean/std of daily_change monthwise"):
    st.html(st.write(result))

# -----------------------

st.subheader("Weeknumber-wise analysis")
month_data = data1[['Weekno','3DayAhead']]
result1 = month_data.groupby(by=['Weekno','3DayAhead'])[['3DayAhead']].count()
result1.rename({"3DayAhead":"count"},inplace=True,axis=1)
with st.expander("Next 3 day [week number wise]"):
    st.html(st.write(result1))   

month_data = data1[['Weekno','5DayAhead']]
result1 = month_data.groupby(by=['Weekno','5DayAhead'])[['5DayAhead']].count()
result1.rename({"5DayAhead":"count"},inplace=True,axis=1)
with st.expander("Next 5 day [week number wise]"):
    st.html(st.write(result1))      


data2 = df[['Close','Weekno']]
result = data2.groupby(by='Weekno')['Close'].agg(['mean','std'])
with st.expander(label="mean/std of daily_change week-number wise"):
    st.html(st.write(result))
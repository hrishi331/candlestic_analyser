import streamlit as st

st.set_page_config("HOME",initial_sidebar_state="collapsed")

st.header("CANDLESTICK PATTERN DETECTOR",width='content')

text1 = """
1. This application recognises candlestick patterns for NIFTY and BANKNIFTY.
2. This gives candlestick pattern along with its sentiment i.e. bullish/neutral/bearish.
3. This app can be used on various time frame ranging from 5m to 1w.
"""
st.write(text1)

st.subheader("NOTE:")
st.write("1. Select larger time window for data if timeframes are larger.")
st.write("Upto 1h : select at least 6 days data window")
st.write("For 1 day : select at least 1 month data window")
st.write("For 1w : select at least 6 months data window")
st.write("2. From date is inclusive and To date is exclusive")
st.write("If you want candlestick patterns on say 25th aug 2025 through 28th aug 2025")
st.write("then select from date : 25th aug 2025")
st.write("then select to date : 29th aug 2025 [desired date + 1]")

c = st.checkbox(label="Read the above note? Click here for application".upper())

if c:
    if st.button(label="Application >>"):
        st.switch_page(page="pages/CDL_Analyser.py")
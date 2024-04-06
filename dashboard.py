import pickle
from pathlib import Path
import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objects as go
import datetime
import streamlit_authenticator as stauth

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


names = ["somesh raval", "raval somesh"]
usernames = ["somesh", "raval"]

START=datetime.datetime(2015, 1, 1)
TODAY= datetime.datetime(2024, 4, 4)

#TODAY=date.today().strftime("%y-%m-%d")

st.title("ForexTrade1 Market Prediction A.I")
#st.sidebar.write("Select Stock Here to Pridict")
#stock=("GC=F","GBPUSD=X","EURUSD=X")

#selected_stock=st.sidebar.selectbox("Select Stock For Pridiction",stock)




# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")



if authentication_status:

 authenticator.logout("Logout", "sidebar")
 st.sidebar.title(f"Welcome {name}")
 stock=st.sidebar.text_input("Type Symbol", value='GC=F')
 n_year=st.sidebar.slider("Year of Pridiction:",1,10)
 Period=n_year * 365


 @st.cache_data
 def load_data(ticker):
    data=yf.download(ticker,START,TODAY)
    data.reset_index(inplace=True)
    return data 

 data_load_state=st.text("Load data...")
 data = load_data(stock)
 data_load_state.text("Loading Data..Done")

 st.subheader('RAW DATA')
 st.write (data.tail())


 def plot_raw_data():
      fig=go.Figure()
      fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'], name='Stock_Open'))
      fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'], name='Stock_Close'))
      fig.layout.update(title_text="Time Serise Data", xaxis_rangeslider_visible=True)
      st.plotly_chart(fig)

      plot_raw_data()

 #forcasting

 df_train=data[['Date','Close']]
 #st.session_state.data 
 df_train = df_train.rename(columns={"Date": "ds","Close": "y"})
 m = Prophet()
 m.fit(df_train)
 future=m.make_future_dataframe(periods=Period)
 forecast =m.predict(future)
 st.subheader('Pridiction of Price')
 st.write (forecast.tail())
 st.write("Pridiction Data")
 fig1=plot_plotly(m, forecast)
 st.plotly_chart(fig1)
 st.write("Pridiction Component")
 fig2=m.plot_components(forecast)
 st.write(fig2)

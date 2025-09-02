import yfinance as yf

ticker = yf.Ticker("BF_B")
data = ticker.history(period="10y", interval="1mo", auto_adjust=True) 
print(data)
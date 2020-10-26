import yfinance as yf
import alphas.A101.alpha101Base as _alpha101Base
from alphas.A101.alpha101 import Alpha101
import pandas as pd
from stocks.stockpool import StockPool

# test on compute alpha
df = yf.download(["MMM","AMD","ABT","ADBE",'A','AAPL','AEE','AEP','AXP','AMGN','APH','CCL'],"2020-05-05","2020-07-07")
AP = Alpha101(df)
data = AP.calculate('ALL', threaded=False, groupby='stock')
data.to_csv('result.csv')

# test on mass download
pool = StockPool('nasdaq')
data = pool.download('2010-10-12', '2020-01-01')
data.to_csv('src/data/nasdaq.csv')

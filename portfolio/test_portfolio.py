from portfolio.portfolios import Portfolio
import pandas as pd

p_test = Portfolio()
stock_data = pd.read_csv('../data/dow.csv', header=[0, 1], index_col=[0])
# test 10 days
for i in range(10):
    if i%5==1:
        p_test.update_port(stock_data.iloc[i:i + 1,]['Adj Close'], new_portfolio={'AAPL': 0.35, 'AMGN': 0.56})
    else:
        p_test.update_port(stock_data.iloc[i:i + 1,]['Adj Close'])

print(p_test.holding)
print(p_test.ts_portvals)
print(p_test.cash_balance)
print(p_test.ts_profit)

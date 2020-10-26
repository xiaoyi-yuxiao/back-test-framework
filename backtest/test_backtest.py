from backtest.backTest import BackTest
from algos.test_algo.Algo import my_test_algo
import pandas as pd
import json as js


# read all the data
stock_data = pd.read_csv('../data/dow.csv', header=[0, 1], index_col=[0])

# process data
stock_data.drop(columns=['DOW'], level=1, inplace=True)
stock_data.fillna(method='backfill', inplace=True)
# build algo
my_algo = my_test_algo()

# build backtest
test_bt = BackTest(stock_data, algo=my_algo)
test_bt.run(update_frequency=20, rolling_range=20, save_result=True, plot_graph=True)






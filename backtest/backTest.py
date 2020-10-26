"""
@author: xiaoyi huang
@version: 0.1
@description: do the back test as time goes by
"""
from portfolio.portfolios import Portfolio
import json as js
import pandas as pd
import yfinance as yf


class BackTest(object):
    def __init__(self, stock_data, algo=None):
        """
        :param stock_data: dataframe, stock data from file
        :param: algo algobase attach algo to back test
        :param alphas: alpha to calculate factors
        """
        self.stock_data = stock_data
        self.close = stock_data['Adj Close']
        self.open = stock_data['Open']
        self.portfolio = Portfolio()
        if algo is not None:
            if hasattr(algo, 'calculate_weight'):
                self.algo = algo
            else:
                raise NotImplementedError('calculate weight method should be implemented')
        else:
            self.algo = algo

    def run(self, update_frequency=1, rolling_range=10, all_in=1, update_at_open=True,
            save_result=False,
            plot_graph=False,
            benchmark='^GSPC'):
        """
        :param update_frequency: int update frequency for the portfolio
        :param rolling_range: int calculate factors for range
        :param all_in: 0-1, how many percent you want to all in, must be implement, 不然会出现无限借钱
        :param update_at_open: boolean, update at open or close
        :param save_result: saving the result to local
        :param plot_graph: plot the profit graph
        :param benchmark: str dow, sp500, nasdaq, using ticker
        :return:
        """
        if self.algo is None:
            raise AttributeError('attach algo first')
        trading_times = len(self.stock_data.index)  # time series
        start_building_port_time = rolling_range  # the time we can build port is the time we have enough data
        for trade_time in range(start_building_port_time, trading_times):
            # update portfolio according to update_frequency
            if (trade_time-start_building_port_time) % update_frequency == 0:
                # feed all data in rolling range to the algo
                optimal_port = self.algo.calculate_weight(self.stock_data.iloc[trade_time-rolling_range:trade_time], )

                if update_at_open:
                    self.portfolio.update_port(self.open.iloc[trade_time:trade_time + 1, ],
                                               new_portfolio=optimal_port, all_in=all_in)  # feed row time's data
                else:
                    self.portfolio.update_port(self.close.iloc[trade_time:trade_time + 1, ],
                                               new_portfolio=optimal_port, all_in=all_in)
            else:
                if update_at_open:
                    self.portfolio.update_port(self.open.iloc[trade_time:trade_time + 1, ])  # feed row time's data
                else:
                    self.portfolio.update_port(self.close.iloc[trade_time:trade_time + 1, ])

        if save_result:
            # write holdings to json file
            jsobj = js.dumps(self.portfolio.ts_holdings)

            fileobj = open('tsHolding.json', 'w')
            fileobj.write(jsobj)
            fileobj.close()

            # save portval and profit
            # store dataframe
            pre_df = {'portval': self.portfolio.ts_portvals, 'profit': self.portfolio.ts_profit}
            df = pd.DataFrame(pre_df, index=self.stock_data.index[rolling_range:])
            df.to_csv('portfolio_result.csv')

        if plot_graph:
            # download benchmark
            start = self.stock_data.index[rolling_range]
            end = self.stock_data.index[-1]
            benchmark_close = yf.download(benchmark, start=start, end=end)['Adj Close']
            benchmark_return = benchmark_close.pct_change().dropna()

            # preparing portfolio return
            pre_df = {'portRet': self.portfolio.ts_portvals}  # has to be portval
            port_val_df = pd.DataFrame(pre_df, index=self.stock_data.index[rolling_range:])
            df_return = port_val_df.pct_change().dropna()

            # concat return data and portfolio data then save to csv
            Ret_result = pd.merge(df_return, benchmark_return, left_index=True, right_index=True, how='outer')
            Ret_result.to_csv('port_vs_benchmark_ret.csv')

            # rescale benchmark portfolio
            benchmark_close = benchmark_close * (self.portfolio.ts_portvals[0]/benchmark_close.iloc[0])
            value_result = pd.merge(port_val_df, benchmark_close, left_index=True, right_index=True, how='outer')
            value_result.to_csv('port_vs_benchmark_val.csv')


            # save plotting
            rx = Ret_result[1:].plot()
            rfig = rx.get_figure()
            rfig.savefig('profit_vs_benchmark_ret.png')

            vx = value_result[1:].plot()
            vfig = vx.get_figure()
            vfig.savefig('profit_vs_benchmark_val.png')


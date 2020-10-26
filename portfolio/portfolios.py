"""
@author: xiaoyi huang
@version: 0.1
@description: hold and record portfolio, manage bank account also
"""


class Portfolio(object):
    def __init__(self, cash_balance=10000):
        self.holding = {}  # dict the weight of each stocks in hand
        self.ts_holdings = {}
        self.ts_portvals = []  # list time series of portfolio value
        self.cur_portval = 0  # current portfolio value
        self.cash_balance = cash_balance  # float the cash balance
        self.initial_balance = cash_balance
        self.ts_profit = []  # list time series profit cur_portval - cash_balance

    def _calculate_portval(self, cur_price):
        """:param cur_price: dataframe 1 row"""
        # calculate portval
        cur_portval = 0
        for ticker in self.holding.keys():
            weight = self.holding[ticker]
            price = cur_price[ticker].values[0]  # get the price for current ticker
            cur_portval += weight * price
        return cur_portval

    def _sell_all(self):
        # update cash balance
        self.cash_balance += self.cur_portval
        self.holding = {}  # clear holdings
        self.cur_portval = 0  # clear portfolio

    def update_port(self, cur_price, new_portfolio=None, all_in=1):
        """
        update portfolios
        :param cur_price: dataframe current close price for all stocks
        :param new_portfolio: dict, ticker name and price if update, what is the new portfolio
        :param all_in: how many portion do you want all in every time
        :return:
        """
        # update holdings if new portfolio is provided
        if new_portfolio is not None:
            self._sell_all()  # cash all the stocks
            self.holding = new_portfolio  # change holding to new portfolio, so that calculate_portval can be perform
            port_val = self._calculate_portval(cur_price)

            # re-balancing portfolio weight to satisfy all in
            scale = self.cash_balance/port_val * all_in  # balance the weight, so that they sum to total cash
            for k,v in new_portfolio.items():
                new_portfolio[k] = v*scale

            self.holding = new_portfolio  # portfolio weight has changed
            self.cur_portval = self.cash_balance * all_in  # not very accurate but enough

            self.cash_balance -= self.cur_portval  # buying the port, same as self.cash_balance * (1-all_in)
            self.ts_holdings[cur_price.index[0]] = self.holding
            self.ts_portvals.append(self.cur_portval)  # update portfolio

        else:
            self.cur_portval = 0  # clear current portval and recalculate
            # calculate portval and record to ts_portval, no cash spent
            self.cur_portval = self._calculate_portval(cur_price)
            self.ts_portvals.append(self.cur_portval)

        # calculate profit once portfolio get updated
        self.ts_profit.append(self.cur_portval + self.cash_balance-self.initial_balance)

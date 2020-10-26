"""alpha 计算等等放进这里"""
from algos.algoBase import AlgoBase
import numpy as np


class my_test_algo(AlgoBase):
    def __init__(self, alphas=None):
        if alphas is not None:
            if hasattr(alphas, 'calculate'):
                self.alphas = alphas
            else:
                raise NotImplementedError('calculate method should be implemented')
        else:
            self.alphas = alphas

    def calculate_weight(self, stock_data):
        # 如果有计算feature的需求， 将在if这下面进行
        if self.alphas is not None:
            features = self.alphas.calculate(stock_data)

        stocks = list(stock_data['Adj Close'].columns)
        optimal_stock = list(np.random.choice(stocks, size=10, replace=False))
        weight = list(np.random.uniform(size=10))
        return dict(zip(optimal_stock, weight))

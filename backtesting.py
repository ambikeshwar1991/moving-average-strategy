"""
@Author : Ambikeshwar
"""

import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import fix_yahoo_finance as yf

from pandas.tseries.offsets import BDay


pwd:P@ssw0rd
username=ambi
class BackTesting(object):
    DEFAULT_INITIAL_CAPITAL = float(1000000.0)

    DEFAULT_QTY_TRADES = 100

    def __init__(self, ticker):
        self.ticker = ticker
        self.asset_prices = yf.download(self.ticker)
        self.signals = None
        self.portfolio = None
        self.positions = None


    def generate_signals(self):
        raise NotImplementedError("Child class needs to implement this method.")

    def plot_signals(self):
        raise NotImplementedError("Child class needs to implement this method.")

    def _generate_positions(self):
        self.positions = pd.DataFrame(index=self.signals.index).fillna(0.0)
        self.positions[self.ticker] = self.DEFAULT_QTY_TRADES * self.signals['signal']

    def backtest_portfolio(self):
        self._generate_positions()
        print(self.positions)
        # Initialize the portfolio with value owned
        self.portfolio = self.positions.multiply(self.asset_prices['Close'], axis=0)
        # Store the difference in shares owned
        pos_diff = self.positions.diff()
        # Add `holdings` to portfolio
        self.portfolio['holdings'] = (self.positions.multiply(self.asset_prices['Close'], axis=0)).sum(axis=1)
        # Add `cash` to portfolio
        self.portfolio['cash'] = self.DEFAULT_INITIAL_CAPITAL - \
                                 (pos_diff.multiply(self.asset_prices['Close'], axis=0)).sum(axis=1).cumsum()
        self.portfolio['total'] = self.portfolio['cash'] + self.portfolio['holdings']
        self.portfolio['returns'] = self.portfolio['total'].pct_change()

    def plot_portfolio(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')
        ax1.plot(self.signals.index.map(mdates.date2num), self.portfolio['total'])
        ax1.plot(self.portfolio.loc[self.signals.positions == 1.0].index,
                 self.portfolio.total[self.signals.positions == 1.0],
                 '^', markersize=10, color='m')
        ax1.plot(self.portfolio.loc[self.signals.positions == -1.0].index,
                 self.portfolio.total[self.signals.positions == -1.0],
                 'v', markersize=10, color='k')
        plt.show()


from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class RawDataAdapter(ABC):
    """
    Adapt raw responses inside a redis queue
    into a standard data strucutre, convert to
    json, and publish to an adapted redis stream.
    """

    def __init__(self):
        """Populate Constructor"""

    @abstractmethod
    async def get_funding_rates(self, *args, **kwargs) -> dict[str, float]:
        """
        Get funding rates

        :return: mapping between tickers and funding rates for all supported tokens (annualized)

        Example:
        {"BTC/USD" : 0.20, "ETH/USD" : -0.05, "ARB/USD": 0.10}
        """

    @abstractmethod
    async def get_oracle_prices(self, *args, **kwargs) -> dict[str, float]:
        """
        Get oracle prices

        :return: mapping between tickers and prices for all supported tokens

        ** Keep in mind redis stream also sends timestamp, you can use it
        when you are pushing it to db or if client wants it**

        Example:
        {"BTC/USD" : 39874.58, "ETH/USD" : 2645.55, "ARB/USD": 1.77}
        """

    @abstractmethod
    async def get_orderbook(self, ticker: str, *args, **kwargs) -> pd.DataFrame:
        """
        Get L2-orderbook data

        :param ticker: ticker whose market we are returning
        :return: dataframe of the first 50 bids and asks
            The columns should be multi-layer: first layer is bid/ask, followed by price/quantity.
            Bid prices should be descending, while asks should be ascending.

        Example:
            bid                 ask
            price   quantity    price   quantity
        0   100.25  50          100.30  40
        1   100.20  30          100.35  25
        2   100.15  20          100.40  15
        """

    @abstractmethod
    async def get_liquidation_prices(self, *args, **kwargs) -> dict[str, float]:
        """
        Get Liquidation Price

        :return: mapping of tickers to liquidation prices by ticker

        Example:
        {"BTC/USD" : 39874.58, "ETH/USD" : 2645.55, "ARB/USD": 1.77}
        """

    @abstractmethod
    async def get_positions(self, account: str, *args, **kwargs) -> pd.DataFrame:
        """
        Get account's positions

        :param account: identifier of the account whose positions we are fetching
        :return: mapping of positions with other traders' positions

        Example:
            tid     ticker      cost_basis  quantity    side    leverage
        0   123456  "BTC/USD"   39579.52    10          "buy"   4.21
        1   123457  "BTC/USD"   42000       5           "sell"  5.01
        2   123458  "BTC/USD"   39539.52    3.441       "sell"  10.00
        """

    @abstractmethod
    async def get_trade_history(self, account: str, *args, **kwargs) -> pd.DataFrame:
        """
        Get trade history for an account

        :param account: the unique identifier for an account
        :return: dataframe of the activities, as described below

        Example:
            timestamp   tid     ticker      price       quantity    side    order_type    status
        0   1706140448  123456  "BTC/USD"   39579.52    10          "buy"   "limit"       "filled"
        1   1706140449  123457  "BTC/USD"   39580.52    5           "sell"  "market"      "filled"
        2   1706140450  123458  "BTC/USD"   39539.52    3.441       "buy"   "limit"       "partial"
        """

    @abstractmethod
    async def get_order_history(self, account: str, *args, **kwargs) -> pd.DataFrame:
        """
        Get the order history associated with an account

        :param account: the unique identifier for an account
        :return: dataframe of the activities, as described below

        Example:
            timestamp   oid     ticker      price       quantity    side    order_type  status
        0   1706140448  123456  "BTC/USD"   39579.52    10          "buy"   "limit"     "canceled"
        1   1706140449  123457  "BTC/USD"   39580.52    5           "sell"  "market"    "filled"
        2   1706140450  123458  "BTC/USD"   39539.52    3.441       "buy"   "limit"     "partial"
        """

    @abstractmethod
    async def get_open_orders(self, account: str, *args, **kwargs) -> pd.DataFrame:
        """
        Get all open orders for an account

        :param account: the unique identifier for an account
        :return: dataframe of the activities, as described below

        Example:
            timestamp   oid     ticker      price       quantity    filled  side    order_type  status
        0   1706140448  123456  "BTC/USD"   39579.52    10          0       "buy"   "limit"     "open"
        1   1706140449  123457  "BTC/USD"   39580.52    5           4.5     "sell"  "limit"     "partial"
        2   1706140450  123458  "BTC/USD"   39539.52    3.441       1.111   "buy"   "limit"     "partial"
        """

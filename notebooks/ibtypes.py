from ib_insync import IB, util, Stock, Option, OptionChain
import sys
import json
from datetime import date, datetime, timezone, timedelta
from dataclasses import dataclass, field
from datetime import date, datetime, timezone

__all__ = ('OptionData').split()

UNSET_INTEGER = 2 ** 31 - 1
UNSET_DOUBLE = sys.float_info.max
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


@dataclass
class OptionData:

    conId: int = UNSET_INTEGER
    symbol: str = ''
    lastTradeDateOrContractMonth: str = ''
    strike: float = UNSET_DOUBLE
    right: str = ''
    multiplier: str = ''
    exchange: str = ''
    currency: str = ''
    localSymbol: str = ''
    tradingClass: str = ''

    date: date = field(default=EPOCH)

    timeToExpiration: int = UNSET_INTEGER

    bid: float = UNSET_DOUBLE
    ask: float = UNSET_DOUBLE
    last:  float = UNSET_DOUBLE

    bidSize: int = UNSET_INTEGER
    askSize: int = UNSET_INTEGER
    lastSize: int = UNSET_INTEGER

    open: float = UNSET_DOUBLE
    high: float = UNSET_DOUBLE
    low: float = UNSET_DOUBLE
    close: float = UNSET_DOUBLE
    volume: int = UNSET_INTEGER

    marketPrice: float = UNSET_DOUBLE
    spread: float = UNSET_DOUBLE
    optionYield: float = UNSET_DOUBLE

    impliedVol: float = UNSET_DOUBLE
    delta: float = UNSET_DOUBLE
    gamma: float = UNSET_DOUBLE
    vega: float = UNSET_DOUBLE
    theta: float = UNSET_DOUBLE
    optPrice: float = UNSET_DOUBLE
    pvDividend: float = UNSET_DOUBLE
    undPrice: float = UNSET_DOUBLE

    def __init__(self, t):

        self.conId = t.contract.conId
        self.symbol = t.contract.symbol
        self.lastTradeDateOrContractMonth = t.contract.lastTradeDateOrContractMonth

        self.date = datetime.strptime(
            self.lastTradeDateOrContractMonth, '%Y%m%d')
        delta = self.date-datetime.now()
        self.timeToExpiration = delta.days+1

        self.strike = t.contract.strike
        self.right = t.contract.right
        self.multiplier = t.contract.multiplier
        self.exchange = t.contract.exchange
        self.currency = t.contract.currency
        self.localSymbol = t.contract.localSymbol

        self.bid = t.bid
        self.ask = t.ask
        self.last = t.last
        self.bidSize = t.bidSize
        self.askSize = t.askSize
        self.lastSize = t.lastSize
        self.open = t.open
        self.high = t.high
        self.close = t.close
        self.volume = t.volume

        self.marketPrice = t.marketPrice()

        self.spread = (t.ask-t.bid)/t.ask

        if t.lastGreeks:
            self.impliedVol = t.lastGreeks.impliedVol
            self.delta = t.lastGreeks.delta
            self.gamma = t.lastGreeks.gamma
            self.vega = t.lastGreeks.vega
            self.theta = t.lastGreeks.theta
            self.optPrice = t.lastGreeks.optPrice
            self.pvDividend = t.lastGreeks.pvDividend
            self.undPrice = t.lastGreeks.undPrice
            self.optionYield = self.marketPrice / self.undPrice
        elif t.modelGreeks:
            self.impliedVol = t.modelGreeks.impliedVol
            self.delta = t.modelGreeks.delta
            self.gamma = t.modelGreeks.gamma
            self.vega = t.modelGreeks.vega
            self.theta = t.modelGreeks.theta
            self.optPrice = t.modelGreeks.optPrice
            self.pvDividend = t.modelGreeks.pvDividend
            self.undPrice = t.modelGreeks.undPrice
            self.optionYield = self.marketPrice / self.undPrice


def StockToJson(s: Stock) -> str:
    o = util.tree(s)
    return json.dumps(o)


def OptionChainToJson(c: OptionChain) -> str:
    o = util.tree(c)
    return json.dumps(o)


def StockFromJson(s: str) -> Stock:
    d = json.loads(s)['Stock']
    return Stock(conId=d['conId'], symbol=d['symbol'], exchange=d['exchange'], primaryExchange=d['primaryExchange'],
                 currency=d['currency'], localSymbol=d['localSymbol'], tradingClass=d['tradingClass'])

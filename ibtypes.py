from datetime import date, datetime, timezone, timedelta
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
import sys

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


"""
{'contract': Option(conId=441665906, symbol='INTC', lastTradeDateOrContractMonth='20200918', strike=48.0, right='P', multiplier='100', exchange='SMART', currency='USD', localSymbol='INTC  200918P00048000', tradingClass='INTC'),
 'time': datetime.datetime(2020, 9, 15, 14, 57, 24, 140327, tzinfo=datetime.timezone.utc),
 'marketDataType': 1,
 'bid': 0.06,
 'bidSize': 124,
 'ask': 0.07,
 'askSize': 446,
 'last': 0.06,
 'lastSize': 1,
 'prevBid': nan,
 'prevBidSize': nan,
 'prevAsk': nan,
 'prevAskSize': nan,
 'prevLast': nan,
 'prevLastSize': nan,
 'volume': 426,
 'open': nan,
 'high': 0.12,
 'low': 0.06,
 'close': 0.16,
 'vwap': nan,
 'low13week': nan,
 'high13week': nan,
 'low26week': nan,
 'high26week': nan,
 'low52week': nan,
 'high52week': nan,
 'bidYield': nan,
 'askYield': nan,
 'lastYield': nan,
 'markPrice': nan,
 'halted': nan,
 'rtHistVolatility': nan,
 'rtVolume': nan,
 'rtTradeVolume': nan,
 'avVolume': nan,
 'tradeCount': nan,
 'tradeRate': nan,
 'volumeRate': nan,
 'shortableShares': nan,
 'indexFuturePremium': nan,
 'futuresOpenInterest': nan,
 'putOpenInterest': nan,
 'callOpenInterest': nan,
 'putVolume': nan,
 'callVolume': nan,
 'avOptionVolume': nan,
 'histVolatility': nan,
 'impliedVolatility': nan,
 'dividends': None,
 'fundamentalRatios': None,
 'ticks': [],
 'tickByTicks': [],
 'domBids': [],
 'domAsks': [],
 'domTicks': [],
 'bidGreeks': OptionComputation(impliedVol=0.3492619998081223, delta=-0.06886604062744471, optPrice=0.05999999865889549, pvDividend=0.0, gamma=0.08050666951660163, vega=0.005958678203250606, theta=-0.03410706860382358, undPrice=50.36000061035156),
 'askGreeks': OptionComputation(impliedVol=0.3618305001551634, delta=-0.07521374166731695, optPrice=0.07000000029802322, pvDividend=0.0, gamma=0.08340405040201886, vega=0.0071819918119523304, theta=-0.037923634808577585, undPrice=50.36000061035156),
 'lastGreeks': OptionComputation(impliedVol=0.34624309068742476, delta=-0.06727193163246419, optPrice=0.05999999865889549, pvDividend=0.0, gamma=0.0797150641539949, vega=0.005958642595035202, theta=-0.03319035744229912, undPrice=50.36000061035156),
 'modelGreeks': OptionComputation(impliedVol=0.3533595420748609, delta=-0.07022943427026687, optPrice=0.052819474877298635, pvDividend=0.0, gamma=0.08080926034314502, vega=0.005959308678839925, theta=-0.03505727738819849, undPrice=50.369998931884766),
 'auctionVolume': nan,
 'auctionPrice': nan,
 'auctionImbalance': nan} """

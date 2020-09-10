#!/usr/bin/env python
from ib_insync import *

util.startLoop()
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1, readonly=True)

stock = Stock(symbol='AAPL', exchange='ISLAND')
chains = ib.reqSecDefOptParams(
    stock.symbol, '', stock.secType, stock.conId)

util.df(chains)


Ticker(
    contract=Option(conId=437258106, symbol='INTC', lastTradeDateOrContractMonth='20200911', strike=48.0, right='P',
                    multiplier='100', exchange='SMART', currency='USD', localSymbol='INTC  200911P00048000', tradingClass='INTC'),
    time=datetime.datetime(2020, 9, 10, 8, 31, 25, 481142,
                           tzinfo=datetime.timezone.utc),
    bid=-1.0, bidSize=0, ask=-1.0, askSize=0, close=0.08,
    bidGreeks=OptionComputation(impliedVol=None, delta=None, optPrice=None,
                                pvDividend=0.0, gamma=None, vega=None, theta=None, undPrice=49.41999816894531),
    askGreeks=OptionComputation(impliedVol=None, delta=None, optPrice=None,
                                pvDividend=0.0, gamma=None, vega=None, theta=None, undPrice=49.41999816894531),
    lastGreeks=OptionComputation(impliedVol=None, delta=None, optPrice=None,
                                 pvDividend=0.0, gamma=None, vega=None, theta=None, undPrice=49.41999816894531),
    modelGreeks=OptionComputation(impliedVol=0.35879614859202597, delta=-0.09864962435456381, optPrice=0.05333963493983114, pvDividend=0.0, gamma=0.15421188676731404, vega=0.005311501648670655, theta=-0.05333963493983114, undPrice=49.41999816894531))

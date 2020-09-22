#!/usr/bin/env python
from ib_insync import IB, util, Stock, Option
import click
import json
import logging
import pandas as pd
import math
from ibtypes import OptionData, StockFromJson, StockToJson, OptionChainToJson
pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)


@click.command()
@click.argument('symbol')
def main(symbol):
    # util.logToConsole(logging.DEBUG)
    util.logToFile('log.txt')

    s = symbol.upper()
    click.echo("Options for {} Loading: ".format(s), nl=False)

    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=3, readonly=True)

    contract = Stock(s, 'SMART', 'USD')
    ib.qualifyContracts(contract)

    click.echo('Chains ', nl=False)
    chains = ib.reqSecDefOptParams(
        contract.symbol, '', contract.secType, contract.conId)
    chain = next(c for c in chains if c.exchange == 'SMART')

    click.echo('Price '.format(s), nl=False)
    ib.reqMarketDataType(1)
    [ticker] = ib.reqTickers(contract)
    value = ticker.marketPrice()

    strikes = [strike for strike in chain.strikes
               if value*0.90 < strike < value*1.0]
    expirations = sorted(exp for exp in chain.expirations)[:2]
    rights = ['P', 'C']

    click.echo("Option Contracts {}@{} ".format(s, value), nl=False)
    contracts = [Option(s, expiration, strike, right, 'SMART', tradingClass=s)
                 for right in rights
                 for expiration in expirations
                 for strike in strikes]
    click.echo('Validate ', nl=False)
    contracts = ib.qualifyContracts(*contracts)
    click.echo(len(contracts), nl=False)

    ib.reqMarketDataType(4)
    click.echo(' Ticker')
    tickers = ib.reqTickers(*contracts)
    options = []
    for t in tickers:
        # click.echo(t)
        # calc = ib.calculateOptionPrice(
        #       t.contract, volatility=0.14, underPrice=value)
        # print(calc)
        options.append(OptionData(t))

    df = util.df(options, [
        'symbol', 'lastTradeDateOrContractMonth', 'strike', 'right', 'marketPrice', 'optionYield', 'timeToExpiration', 'spread', 'bid', 'ask', 'impliedVol', 'delta', 'gamma', 'vega'])
    click.echo(df)

    currentWeekPut = df[(df['right'] == 'P') & (
        df['lastTradeDateOrContractMonth'] == expirations[0])]

    click.echo(
        currentWeekPut.loc[(abs(abs(currentWeekPut.delta)-0.2)).sort_values().index].head(2))

    ib.disconnect()


if __name__ == "__main__":
    main()

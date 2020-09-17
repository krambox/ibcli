#!/usr/bin/env python
from ib_insync import *
import click
import json
import logging
import pandas as pd
import math
from ibtypes import OptionData
pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)


@click.command()
@click.argument('symbol')
def main(symbol):
    # util.logToConsole(logging.DEBUG)
    util.logToFile('log.txt')

    s = symbol.upper()
    click.echo("reqSecDefOptParams {}".format(s))

    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=3, readonly=True)

    contract = Stock(s, 'SMART', 'USD')
    ib.qualifyContracts(contract)
    click.echo(contract)

    ib.reqMarketDataType(2)
    [ticker] = ib.reqTickers(contract)
    click.echo(ticker)

    value = ticker.marketPrice()
    chains = ib.reqSecDefOptParams(
        contract.symbol, '', contract.secType, contract.conId)
    click.echo(chains)
    click.echo(util.df(chains))
    chain = next(c for c in chains if c.exchange == 'SMART')

    strikes = [strike for strike in chain.strikes
               if value*0.90 < strike < value*1.0]
    expirations = sorted(exp for exp in chain.expirations)[:2]
    rights = ['P', 'C']
    #rights = ['P']

    click.echo("Request Option Chain for {}@{} {} {} {} ".format(
        s, value, rights, expirations, strikes))
    contracts = [Option(s, expiration, strike, right, 'SMART', tradingClass=s)
                 for right in rights
                 for expiration in expirations
                 for strike in strikes]

    click.echo("qualifyContracts")
    contracts = ib.qualifyContracts(*contracts)
    click.echo(len(contracts))

    tickers = ib.reqTickers(*contracts)
    # click.echo(tickers)
    options = []
    for t in tickers:
        # click.echo(t)
        options.append(OptionData(t))

    click.echo(util.df(options, [
               'symbol', 'lastTradeDateOrContractMonth', 'strike', 'right', 'marketPrice', 'optionYield', 'timeToExpiration', 'spread', 'bid', 'ask', 'impliedVol', 'delta', 'gamma', 'vega']))


if __name__ == "__main__":
    main()

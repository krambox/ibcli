#!/usr/bin/env python
from ib_insync import *
import click


@click.command()
@click.argument('symbol')
# util.startLoop()  # uncomment this line when in a notebook
def main(symbol):
    s = symbol.upper()
    duration = '20 Y'
    click.echo("Fetch {}".format(s))

    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1, readonly=True)

    stock = Stock(symbol=s, exchange='ISLAND')
    trades = ib.reqHistoricalData(
        stock, endDateTime='', durationStr=duration,
        barSizeSetting='1 day', whatToShow='ADJUSTED_LAST', useRTH=True)

    iv = ib.reqHistoricalData(
        stock, endDateTime='', durationStr=duration,
        barSizeSetting='1 day', whatToShow='OPTION_IMPLIED_VOLATILITY', useRTH=True)

    hv = ib.reqHistoricalData(
        stock, endDateTime='', durationStr=duration,
        barSizeSetting='1 day', whatToShow='HISTORICAL_VOLATILITY', useRTH=True)

    # convert to pandas dataframe:
    trades_df = util.df(trades)
    iv_df = util.df(iv)
    hv_df = util.df(hv)
    # print(df)

    trades_df.to_csv(s+'_OHLC.csv', encoding='utf-8', index=False)
    iv_df.to_csv(s+'_IV.csv', encoding='utf-8', index=False)
    hv_df.to_csv(s+'_HV.csv', encoding='utf-8', index=False)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
from ib_insync import *
import click
import logging
import os.path
from os import path
from datetime import datetime
import time
import calendar

import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)


@click.command()
@click.argument('token')
@click.argument('queryid')
# util.startLoop()  # uncomment this line when in a notebook
def main(token, queryid):
    # util.logToConsole(logging.DEBUG)
    report = 'report.xml'

    ib = IB()
    #ib.connect('127.0.0.1', 7497, clientId=1, readonly=True)

    # click.echo(util.df(ib.portfolio()))

    r = FlexReport()
    if (path.exists(report)):
        r.load(report)
    else:
        r.download(token, queryid)
        r.save(report)

    df = r.df('Trade')

    df['stock'] = df.apply(lambda row: row.symbol if row.assetCategory ==
                           'STK' else row.underlyingSymbol, axis=1)
    df['shortLong'] = df.apply(lambda row: 'S' if row.buySell ==
                               'SELL' and row.openCloseIndicator == 'O' or row.buySell ==
                               'BUY' and row.openCloseIndicator == 'C' else 'L', axis=1)

    df['datetime_date'] = df.apply(lambda row: datetime.strptime(
        row.dateTime, '%Y-%m-%d %H:%M:%S'), axis=1)

    df['week'] = df.apply(
        lambda row: row.datetime_date.date().isocalendar()[1], axis=1)

    df['month'] = df.apply(lambda row: row.datetime_date.date().month, axis=1)

    c = calendar.Calendar(firstweekday=calendar.SUNDAY)

    def options_month(d):
        monthcal = c.monthdatescalendar(d.year, d.month)
        third_week = [day for week in monthcal for day in week if
                      day.weekday() == calendar.FRIDAY and
                      day.month == d.month][2]
        if d.day <= third_week.day+1:
            return d.month
        else:
            return d.month+1

    df['options_month'] = df.apply(
        lambda row: options_month(row.datetime_date), axis=1)

    # df.to_excel("report.xlsx")
    # df1 = df[['accountId', 'currency', 'fxRateToBase', 'assetCategory',
    #          'symbol', 'description', 'conid', 'underlyingSymbol', 'multiplier', 'strike', 'expiry', 'putCall', 'dateTime', 'quantity', 'tradePrice', 'tradeMoney', 'proceeds', 'taxes', #'ibCommission', 'ibCommissionCurrency', 'netCash', 'closePrice', 'openCloseIndicator', 'notes', 'cost', 'fifoPnlRealized', 'mtmPnl', 'buySell', 'Week', 'Month']].copy()

    # click.echo(df1)

    df_closed = df[(df['openCloseIndicator'] == 'C')]

    df_stock = df[(df['assetCategory'] == 'STK') &
                  (df['openCloseIndicator'] == 'C')]
    df_options = df[(df['assetCategory'] == 'OPT') &
                    (df['openCloseIndicator'] == 'C')]

    # click.echo(pd.pivot_table(
    #    df_options, index=["underlyingSymbol"], columns=['options_month', 'week'], values=["fifoPnlRealized"], fill_value=0, aggfunc=[np.sum], margins=True, margins_name='Total'))
    click.echo(pd.pivot_table(
        df_closed, index=['assetCategory', 'shortLong', 'stock'], columns=['options_month', 'week'], values=["fifoPnlRealized"], fill_value=0, aggfunc=[np.sum], margins=True, margins_name='Total'))

    ib.disconnect()


if __name__ == "__main__":
    main()

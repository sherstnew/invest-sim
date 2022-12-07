from datetime import datetime, timedelta

from pandas import DataFrame
import plotly.graph_objs as pltgo
from tinkoff.invest import Client, RequestError, CandleInterval, \
    HistoricCandle
import plotly.io as pltio
import pandas as pd

# import json_bd

figi_info = input()

t = "t.N7tYIuWUABuLI9d_6icZxTsfOkOna3nFLHbxQKmkxGfr9zTxN3rqVWisshKxSUCHu00uB5q2QDRFP-oKsVVHJw"

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def run_day():
    try:
        with Client(t) as client:
            r = client.market_data.get_candles(
                figi=figi_info,
                from_=datetime.utcnow() - timedelta(days=1),
                to=datetime.utcnow(),
                interval=CandleInterval.CANDLE_INTERVAL_5_MIN
            )

            df = create_df(r.candles)
            fig = pltgo.Figure()
            fig.add_trace(pltgo.Scatter(x=df["time"], y=df["cost"], name='', line=dict(color="black")))
            fig.update_traces(hovertemplate="Дата: %{x}<br>Цена: %{y}$")
            fig.update_layout(plot_bgcolor='#ffba43')
            fig.update_xaxes(rangeslider_visible=True)
            fig.write_html('shareframes/' + figi_info + '.html')

    except RequestError as e:
        print(str(e))

def run_month():
    try:
        with Client(t) as client:
            r = client.market_data.get_candles(
                figi=figi_info,
                from_=datetime.utcnow() - timedelta(days=30),
                to=datetime.utcnow(),
                interval=CandleInterval.CANDLE_INTERVAL_DAY
            )

            df = create_df(r.candles)
            fig = pltgo.Figure()
            fig.add_trace(pltgo.Scatter(x=df["time"], y=df["cost"], name='', line=dict(color="black")))
            fig.update_traces(hovertemplate="Дата: %{x}<br>Цена: %{y}$")
            fig.update_layout(plot_bgcolor='#ffba43')
            fig.write_html('shareframes/' + figi_info + '.html')

    except RequestError as e:
        print(str(e))
def create_df(candles: [HistoricCandle]):
    df = DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': cast_money(c.open),
        'cost': cast_money(c.close),
        'high': cast_money(c.high),
        'low': cast_money(c.low),
    } for c in candles])

    return df


def cast_money(v):
    return v.units + v.nano / 1e9


run_day()

from tinkoff.invest import Client, InstrumentStatus, CandleInterval
import pandas as pd
from datetime import datetime, timedelta
import json
import requests

op = 1
day_procent = 0
lasrprice = ""

name = 0
r = 0
s = []
lprice = []

t = "t.N7tYIuWUABuLI9d_6icZxTsfOkOna3nFLHbxQKmkxGfr9zTxN3rqVWisshKxSUCHu00uB5q2QDRFP-oKsVVHJw"

with Client(t) as cl:
    if op == 1:
        srs = cl.instruments.shares(
            instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)
        data = []
        for i in srs.instruments:
            if i.trading_status > 1:
                shares_info = {
                    'currency': i.currency,
                    'sector': i.sector,
                    'country': i.country_of_risk_name,
                    'exchange': i.exchange,
                    'name': i.name,
                    'figi': i.figi,
                    'lot': i.lot,
                    'trade_enable': i.trading_status,
                }

                data.append(shares_info)

        shares = pd.DataFrame(data)
        op += 1
#     if op == 2:
#         srs = cl.instruments.bonds(
#             instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)
#         data = []
#         for i in srs.instruments:
#             bonds_info = {
#                 'currency': i.currency,
#                 'sector': i.sector,
#                 'country': i.country_of_risk_name,
#                 'exchange': i.exchange,
#                 'perpetual': i.perpetual_flag,
#                 'amortization': i.amortization_flag,
#                 'short': i.short_enabled_flag,
#                 'name': i.name,
#                 'ticker': i.ticker,
#             }
#
#             data.append(bonds_info)
#
#         bonds = pd.DataFrame(data)
#         op += 1
#
#     if op == 3:
#         srs = cl.instruments.currencies(
#             instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)
#         data = []
#         for i in srs.instruments:
#             currencies_info = {
#                 'currency': i.currency,
#                 'country': i.country_of_risk_name,
#                 'exchange': i.exchange,
#                 'short': i.short_enabled_flag,
#                 'name': i.name,
#                 'ticker': i.ticker,
#             }
#
#             data.append(currencies_info)
#
#         currencies = pd.DataFrame(data)
#         op += 1
#
#     if op == 4:
#         srs = cl.instruments.etfs(
#             instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)
#         data = []
#         for i in srs.instruments:
#             etfs_info = {
#                 'currency': i.currency,
#                 'sector': i.sector,
#                 'country': i.country_of_risk_name,
#                 'exchange': i.exchange,
#                 'short': i.short_enabled_flag,
#                 'name': i.name,
#                 'ticker': i.ticker,
#             }
#
#             data.append(etfs_info)
#
#         etfs = pd.DataFrame(data)
#         op == 0
#
#
# # print(shares)
# # print(bonds)
# # print(currencies)
# # print(etfs)
shar = shares.set_index('figi').T.to_dict('list')

with open("static/shares.json", "w", encoding="utf-8") as f:
    json.dump(shar, f, ensure_ascii=False, indent=4)


def translate(figi):
    if shar[figi][1] == "other":
        shar[figi][1] = "????????????"
    elif shar[figi][1] == "health_care":
        shar[figi][1] = "??????????????????????????????"
    elif shar[figi][1] == "green_energy":
        shar[figi][1] = "?????????????? ????????????????????"
    elif shar[figi][1] == "it":
        shar[figi][1] = "???????????????????????????? ????????????????????"
    elif shar[figi][1] == "ecomaterials":
        shar[figi][1] = "?????????????????? ?????? ??????-????????????????????"
    elif shar[figi][1] == "industrials":
        shar[figi][1] = "???????????????????????????? ?? ??????????????????"
    elif shar[figi][1] == "real_estate":
        shar[figi][1] = "????????????????????????"
    elif shar[figi][1] == "consumer":
        shar[figi][1] = "?????????????????????????????? ???????????? ?? ????????????"
    elif shar[figi][1] == "materials":
        shar[figi][1] = "???????????????? ????????????????????????????"
    elif shar[figi][1] == "telecom":
        shar[figi][1] = "????????????????????????????????"
    elif shar[figi][1] == "financial":
        shar[figi][1] = "???????????????????? ????????????"
    elif shar[figi][1] == "electrocars":
        shar[figi][1] = "???????????????????????????????? ?? ??????????????????????????"
    elif shar[figi][1] == "utilities":
        shar[figi][1] = "??????????????????????????????????"

def last_price(figi):
    with Client(t) as cl:
        r = cl.market_data.get_candles(
            figi=figi,
            from_=datetime.utcnow() - timedelta(days=1),
            to=datetime.utcnow(),
            interval=CandleInterval.CANDLE_INTERVAL_5_MIN
        )
    for candle in r.candles:
        lprice.append(candle.close.units + candle.close.nano / 1e9)


# def sym_last_price(figi):
#     if shar[figi][0] == "usd":
#         lastprice = str(lprice[-1]) + "$"
#     elif shar[figi][0] == "eur":
#         lastprice = str(lprice[-1]) + "???"
#     elif shar[figi][0] == "rub":
#         lastprice = str(lprice[-1]) + "???"
#     return lastprice

def getCurrency(figi):
    if shar[figi][0] == "usd":
        currency = "$"
    elif shar[figi][0] == "eur":
        currency = "???"
    elif shar[figi][0] == "rub":
        currency = "???"
    return currency



def response(figi):
    last_price(figi)
    # lst_price = sym_last_price(figi)
    currency = getCurrency(figi)
    day_procent = (lprice[-1] * 100) / lprice[0] - 100
    # print(day_procent)
    translate(figi)
    sector = shar[figi][1]
    name = shar[figi][4]
    country = shar[figi][2]
    # print(name)
    lot = shar[figi][5]
    # print(lot)
    trade_enable = shar[figi][6]
    # print(trade_enable)
    exchange = shar[figi][3]
    share = {
        "name": name,
        "last_price": lprice[-1],
        "day_procent": day_procent,
        "lots": lot,
        "trade_state": trade_enable,
        "sector": sector,
        "country": country,
        "exchange": exchange,
        "currency": currency,
    }

    return share

from tinkoff.invest import Client, InstrumentStatus, CandleInterval
import pandas as pd
from datetime import datetime, timedelta
import json

op = 1

s = []

t = "t.N7tYIuWUABuLI9d_6icZxTsfOkOna3nFLHbxQKmkxGfr9zTxN3rqVWisshKxSUCHu00uB5q2QDRFP-oKsVVHJw"

with Client(t) as cl:
    if op == 1:
        srs = cl.instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)
        data = []
        for i in srs.instruments:
            shares_info = {
                # 'currency': i.currency,
                # 'sector': i.sector,
                # 'country': i.country_of_risk_name,
                # 'exchange': i.exchange,
                # 'short': i.short_enabled_flag,
                'name': i.name,
                # 'ticker': i.ticker,
            }

            data.append(shares_info)

        shares = pd.DataFrame(data)
        op += 1
    if op == 2:
        srs = cl.instruments.bonds(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)
        data = []
        for i in srs.instruments:
            bonds_info = {
                'currency': i.currency,
                'sector': i.sector,
                'country': i.country_of_risk_name,
                'exchange': i.exchange,
                'perpetual': i.perpetual_flag,
                'amortization': i.amortization_flag,
                'short': i.short_enabled_flag,
                'name': i.name,
                'ticker': i.ticker,
            }

            data.append(bonds_info)

        bonds = pd.DataFrame(data)
        op += 1

    if op == 3:
        srs = cl.instruments.currencies(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)
        data = []
        for i in srs.instruments:
            currencies_info = {
                'currency': i.currency,
                'country': i.country_of_risk_name,
                'exchange': i.exchange,
                'short': i.short_enabled_flag,
                'name': i.name,
                'ticker': i.ticker,
            }

            data.append(currencies_info)

        currencies = pd.DataFrame(data)
        op += 1

    if op == 4:
        srs = cl.instruments.etfs(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)
        data = []
        for i in srs.instruments:
            etfs_info = {
                'currency': i.currency,
                'sector': i.sector,
                'country': i.country_of_risk_name,
                'exchange': i.exchange,
                'short': i.short_enabled_flag,
                'name': i.name,
                'ticker': i.ticker,
            }

            data.append(etfs_info)

        etfs = pd.DataFrame(data)
        op == 0


def main(figi_info):
    with Client(t) as cl:
        r = cl.market_data.get_candles(
            figi=figi_info,
            from_=datetime.utcnow() - timedelta(days=1),
            to=datetime.utcnow(),
            interval=CandleInterval.CANDLE_INTERVAL_5_MIN # см. utils.get_all_candles
        )
        print(r)


print(shares)
print(bonds)
print(currencies)
print(etfs)

sg = shares.to_dict()
with open("static/shares.json", "w") as file:
    json.dump(sg, file, ensure_ascii=False)


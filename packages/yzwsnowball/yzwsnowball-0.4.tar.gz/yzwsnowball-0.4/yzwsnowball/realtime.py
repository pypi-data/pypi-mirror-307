import time
from yzwsnowball import api_ref
from yzwsnowball import utls


def quotec(symbols):
    url = api_ref.realtime_quote+symbols
    return utls.fetch_without_token(url)


def quote_detail(symbol):
    return utls.fetch(api_ref.realtime_quote_detail+symbol)


def pankou(symbol):
    url = api_ref.realtime_pankou+symbol
    return utls.fetch(url)


def kline(symbol, period="day", counts=100):
    return utls.fetch(api_ref.kline.format(symbol, int(time.time()*1000) + 24 * 60 * 60 * 1000, period, counts))

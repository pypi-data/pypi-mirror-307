import json
import os
from yzwsnowball import cons
from yzwsnowball import api_ref
from yzwsnowball import utls


def report(symbol):
    url = api_ref.report_latest_url+symbol
    return utls.fetch(url)


def earningforecast(symbol):
    url = api_ref.report_earningforecast_url+symbol
    return utls.fetch(url)

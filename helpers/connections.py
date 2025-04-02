import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ccxt
from helpers.constants import API_KEY, SECRET

BINANCE_NORMAL_CONNECTION = ccxt.binance()

EXCHANGE = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET,
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'},
})

EXCHANGE.set_sandbox_mode(True)

def get_balance(exchange):
    balance = exchange.fetch_balance()
    return balance['total']['USDT']

def calculate_value(balance, porcentage, actual_price):
    quantity = balance * porcentage / actual_price
    return quantity

def trade_buy(exchange, symbol, quantity):
    order = exchange.create_market_buy_order(symbol, quantity)
    return order

def trade_sell(exchange, symbol, quantity):
    order = exchange.create_market_sell_order(symbol, quantity)
    return order

import logging
import ccxt
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
SECRET = os.getenv('SECRET')

class MarketMaker:

    def __init__(
            self,
            exchange_id: str = 'binance', # Exchange to trade on
            base_asset: str = 'BTC', # Base asset to trade with
            quote_asset: str = 'USDT', # Quote asset to trade with
            order_size_percentage: float = 0.02, # Increased from 0.01
            spread_percentage: float = 0.5, # Slightly wider spread
            max_order_count: int = 5, # Limit number of concurred orders
            min_order_value: float = 10.00, # Minimum order value in quote currency
            risk_balance_limit: float = 0.07, # Slightly increased risk tolerance
            dynamic_spread_factor: float = 0.5, # Volatility-based spread adjustment
            order_refresh_interval: int = 20, # Seconds between order updates
            max_exposure_percentage: float = 0.1, # Maximum portfolio exposure
            #order_expiration: , # How long before an order is canceled (if not filled)
            ):
        
        self.exchange = exchange_id
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.order_size_percentage = order_size_percentage
        self.spread_percentage = spread_percentage
        self.max_order_count = max_order_count
        self.min_order_value = min_order_value
        self.risk_balance_limit = risk_balance_limit
        self.dynamic_spread_factor = dynamic_spread_factor
        self.order_refresh_interval = order_refresh_interval
        self.max_exposure_percentage = max_exposure_percentage

        exchange_class = getattr(ccxt, exchange_id)
        
        self.exchange = exchange_class({
            'apiKey': API_KEY,
            'secret': SECRET,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'  # Explicitly set spot trading
            }
        })
        self.exchange.set_sandbox_mode(True)
        

    def market_monitor(self):
        
        try:
            
            ticker = self.exchange.fetch_ticker(f'{self.base_asset}/{self.quote_asset}')
            order_book = self.exchange.fetch_order_book(f'{self.base_asset}/{self.quote_asset}')
            print("ticker", ticker)
            print("order_book", order_book)
        except Exception as e:
            print(e)
            return e

def main():
    market = MarketMaker()
    market.market_monitor()

if __name__ == "__main__":
    main()
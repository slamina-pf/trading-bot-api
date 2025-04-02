
import logging
import ccxt
from dotenv import load_dotenv
import os
import numpy as np
from typing import Dict
import time
from collections import deque

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
            spread_percentage: float = 0.1, # Slightly wider spread
            max_order_count: int = 5, # Limit number of concurred orders
            min_order_value: float = 10.00, # Minimum order value in quote currency
            risk_balance_limit: float = 0.07, # Slightly increased risk tolerance
            dynamic_spread_factor: float = 0.5, # Volatility-based spread adjustment
            order_refresh_interval: int = 20, # Seconds between order updates
            max_exposure_percentage: float = 0.1, # Maximum portfolio exposure
            #order_expiration: , # How long before an order is canceled (if not filled)
            ):
        
        # Advanced logging setup
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s: %(message)s',
            filename='market_maker.log'
        )
        self.logger = logging.getLogger(__name__)

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
        self.trading_pair = f'{self.base_asset}/{self.quote_asset}'
        self.order_history = deque()

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
        

    def market_data(self):
        """
            Fetch comprehensive market data with advanced analysis
        """
        try:
            
            ticker = self.exchange.fetch_ticker(self.trading_pair)
            order_book = self.exchange.fetch_order_book(self.trading_pair)
            
            # Calculate market depth metrics
            bids = order_book['bids']
            asks = order_book['asks']

            mid_price = (ticker['bid'] + ticker['ask']) / 2
            bid_volume = sum([bid[1] for bid in bids[:10]])
            ask_volume = sum([ask[1] for ask in asks[:10]])

            # Calculate price volatility
            recent_trades = self.exchange.fetch_trades(self.trading_pair, limit=50)
            price_changes = [trade['price'] for trade in recent_trades]
            volatility = np.std(price_changes) / mid_price

            return {
                'mid_price': mid_price,
                'volatility': volatility,
                'bid_volume': bid_volume,
                'ask_volume': ask_volume
            }
        
        except Exception as e:
            self.logger.error(f"Market data fetch error: {e}")
            return None
        
    def calculate_dynamic_spread(self, market_data: Dict[str, float]) -> float:
        """
            Dynamically adjust spread based on market volatility
        """
        base_spread = self.spread_percentage
        
        volatility_multiplier = 1 + (market_data['volatility'] * 
                                    self.dynamic_spread_factor)
        
        return base_spread * volatility_multiplier 

    def calculate_order_size(self, price: float) -> float:
        """
            Calculate order size based on current price and risk tolerance
        """

        try:
            self.exchange.load_time_difference()
            balance = self.exchange.fetch_balance()
            quote_balance = balance['free'].get(self.quote_asset, 0)
            print("Quote Balance: ", quote_balance)

            # Determine order size
            order_value = quote_balance * self.order_size_percentage
            print("Order Value: ", order_value)
            order_size = max(order_value / price, 0)
            print("Order Size: ", order_size)

            # Safety checks
            min_order_size = self.exchange.markets[self.trading_pair]['limits']['amount']['min']
            max_order_size = min(
                order_size, 
                balance['free'].get(self.base_asset, 0),
                quote_balance / price
            )

            if order_size < min_order_size or order_value < self.min_order_value:
                self.logger.warning("Order size too small, skipping order.")
                return 0

            return max_order_size, order_value
        except Exception as e:
            self.logger.error(f"Order size calculation error: {e}")

    def manage_orders(self):
        """
            Advanced order management with intelligent placement and cancellation
        """
        try:

            market_data = self.market_data()
            if not market_data:
                return
            
            dynamic_spread = self.calculate_dynamic_spread(market_data)
            mid_price = market_data['mid_price']

            spread = mid_price * (dynamic_spread / 100)
            buy_price = mid_price - spread
            sell_price = mid_price + spread

            order_size, order_value = self.calculate_order_size(mid_price)
            if order_size == 0:
                return
            
            # Cancel existing orders if they're too far from current market prices
            open_orders = self.exchange.fetch_open_orders(self.trading_pair)
            print("Open Orders: ", open_orders)
            for order in open_orders:
                if (abs(order['price'] - (buy_price if order['side'] == 'buy' else sell_price)) 
                    > spread * 0.2):
                    self.exchange.cancel_order(order['id'], self.trading_pair)

            # Limit total number of concurrent orders
            if len(open_orders) < self.max_order_count:
                # Place new orders
                self.exchange.create_limit_buy_order(self.trading_pair, order_size, buy_price)
                self.exchange.create_limit_sell_order(self.trading_pair, order_size, sell_price)
                
                self.logger.info(
                    f"Orders placed: Buy at {buy_price:.4f}, Sell at {sell_price:.4f}, "
                    f"Size: {order_size:.6f}"
                )

        except Exception as e:
            self.logger.error(f"Order management error: {e}")

    def run(self):
        """
            Main bot execution loop with comprehensive error handling
        """
        print("Market Maker Bot Starting...")
        self.logger.info("Market Maker Bot Starting...")
        
        try:
            while True:
                self.manage_orders()
                time.sleep(self.order_refresh_interval)
        
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user.")
        except Exception as e:
            self.logger.critical(f"Unexpected error: {e}")
        finally:
            # Cleanup: Cancel all orders on exit
            open_orders = self.exchange.fetch_open_orders(self.trading_pair)
            for order in open_orders:
                self.exchange.cancel_order(order['id'], self.trading_pair)
            self.logger.info("All orders canceled. Bot shutting down.")

def main():
    market_maker = MarketMaker()
    market_maker.run()
    
if __name__ == "__main__":
    main()

def track_profit(self):
    try:
        trades = self.exchange.fetch_my_trades(self.trading_pair)
        for trade in trades:
            if trade['id'] not in self.processed_trades:  # Need to track processed trades
                cost = trade['amount'] * trade['price']
                if trade['side'] == 'sell':
                    profit = (trade['price'] - self.get_average_buy_price()) * trade['amount']
                    self.logger.info(f"Trade Profit: {profit:.4f} {self.quote_asset}")
                self.processed_trades.add(trade['id'])
    except Exception as e:
        self.logger.error(f"Profit tracking error: {e}")
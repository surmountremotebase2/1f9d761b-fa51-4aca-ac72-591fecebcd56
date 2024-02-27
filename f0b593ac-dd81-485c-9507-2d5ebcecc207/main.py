from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, SMA
from surmount.logging import log
import numpy as np

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]  # The assets to trade

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"  # Daily data interval for this strategy

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Retrieve the close, high, and low prices for the asset
            close_prices = np.array([i[ticker]["close"] for i in data["ohlcv"]])
            high_prices = np.array([i[ticker]["high"] for i in data["ohlcv"]])
            low_prices = np.array([i[ticker]["low"] for i in data["ohlcv"]])

            if len(close_prices) < 20:
                # Insufficient data to process, assign no allocation
                allocation_dict[ticker] = 0
                continue

            # Determine the lowest low and highest high of the last 20 days
            lowest_20 = np.min(low_prices[-20:])
            highest_20 = np.max(high_prices[-20:])
            
            current_close = close_prices[-1]
            current_low = low_prices[-1]
            current_high = high_prices[-1]

            # Check buy and sell conditions
            if current_close == lowest_20 or current_low == lowest_20:
                # Buy condition met, allocate 25% to this asset
                allocation_dict[ticker] = 0.25
            elif current_close == highest_20 or current_high == highest_20:
                # Sell condition met, reduce or liquidate position (set to 0)
                allocation_dict[ticker] = 0
            else:
                # No clear signal, maintain current allocation (could be adjusted for more complex strategies)
                allocation_dict[ticker] = 0 
            
        # Ensure the sum of allocations does not exceed 1
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            # Normalize allocations if the sum exceeds 1
            allocation_dict = {k: v / total_allocation for k, v in allocation_dict.items()}
        
        return TargetAllocation(allocation_dict)
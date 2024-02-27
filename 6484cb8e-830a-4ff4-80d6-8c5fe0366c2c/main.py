from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # You can change these tickers as per your preference
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    
    @property
    def interval(self):
        # Using '1day' for swing trading strategies
        return "1day"
    
    @property
    def assets(self):
        # Returning the tickers that the strategy will trade
        return self.tickers
    
    @property
    def data(self):
        # No additional data sources are required for this example
        return []
    
    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Retrieve the EMA for a quick and slow period
            quick_ema = EMA(ticker, data["ohlcv"], length=10)
            slow_ema = EMA(ticker, data["ohlcv"], length=30)
            
            # Retrieve the RSI
            rsi = RSI(ticker, data["ohlcv"], length=14)
            
            if len(quick_ema) > 0 and len(slow_ema) > 0 and len(rsi) > 0:
                # Strategy logic:
                # - Buy signal: Quick EMA crosses above Slow EMA and RSI is above 30 (avoiding oversold conditions)
                # - Sell signal/avoid buying: Quick EMA is below Slow EMA or RSI exceeds 70 (overbought conditions)
                if quick_ema[-1] > slow_ema[-1] and rsi[-1] > 30 and rsi[-1] < 70:
                    allocation_dict[ticker] = 1.0 / len(self.tickers)  # Evenly distribute allocation among tickers
                else:
                    allocation_dict[ticker] = 0  # Allocate 0% to tickers not meeting buy criteria
            else:
                # If there's not enough data to compute EMA or RSI, avoid trading this ticker
                allocation_dict[ticker] = 0
        
        # Log the targeted allocations for review
        log(f"Target allocations: {allocation_dict}")
        
        return TargetAllocation(allocation_dict)
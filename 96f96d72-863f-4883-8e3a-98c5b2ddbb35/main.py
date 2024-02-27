from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import ATR
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset you are interested in
        self.tickers = ["AAPL"]
        self.data_list = [Asset(i) for i in self.tickers]

    @property
    def interval(self):
        # Specify the data interval
        return "1day"

    @property
    def assets(self):
        # Return the assets this strategy applies to
        return self.tickers

    @property
    def data(self):
        # Return the required data sources
        return self.data_list

    def run(self, data):
        # Donchian Channel Strategy implementation

        # Initialize dict for target allocation
        allocation_dict = {}

        # Get the high, low, and close prices from the data for the ticker
        for ticker in self.tickers:
            prices = data["ohlcv"]
            if len(prices) < 20:  # Make sure we have at least 20 days of data to work with
                allocation_dict[ticker] = 0.0  # No position if there isn't enough data
                continue

            # Define the Donchian Channel high and low boundaries
            high_20 = max([d[ticker]["high"] for d in prices[-20:]])
            low_20 = min([d[ticker]["low"] for d in prices[-20:]])

            # Current close price
            current_close = prices[-1][ticker]["close"]

            # Strategy logic to allocate positions
            if current_close >= high_20:
                allocation_dict[ticker] = 0.5  # Going long with 50% of the portfolio
            elif current_close <= low_20:
                allocation_dict[ticker] = -0.5  # Going short with -50% (demonstration purpose, adjust as needed)
            else:
                allocation_dict[ticker] = 0.0  # No position

        # Log the allocation for debugging
        log("Calculated allocation: {}".format(allocation_dict))

        return TargetAllocation(allocation_dict)
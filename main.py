# Import class from AlpacaMarkets and API keys from secret file
# Warning: this code will execute orders on your portfolio if you have connected an active API key
from AlpacaMarkets import TradingAPI
from secret_tokens import Alpaca_KeyID, Alpaca_SecretKey

# Initialize class object with your alpaca portfolio's api keys
AlpTrading = TradingAPI(Alpaca_KeyID, Alpaca_SecretKey)

# Get information on the account settings and preferences
print(AlpTrading.GetAccount())

# Create a new order with various input parameters: Buy 10 shares of AAPL, order is 'good-till canceled, and has a trailing stop of 3%
AlpTrading.CreateOrder(symbol='AAPL', qty=10, side='buy', type='trailing_stop', time_in_force='gtc', trail_percent=3)

# Get information on any orders that are open or have been executed
print(AlpTrading.GetOrders(status="all", symbols="AAPL"))  # Will display information on the previous order you placed

# Check if there is an existing position in your portfolio
print(AlpTrading.CurrentPositions('AAPL'))  # should be True
print(AlpTrading.CurrentPositions('BTCUSD'))  # should be False

# Close an existing open position (If no input symbol, will close all existing positions)
AlpTrading.ClosePosition("AAPL")  # Closes the 10 long shares of AAPL we bought earlier

# Generate the history of the portfolio and save it to a CSV file (use 'print' to display in console)
AlpTrading.PortfolioHistory(period='1W', timeframe='5Min', to_csv=True)

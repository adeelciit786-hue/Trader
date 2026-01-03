# Trader

A simple command-line trading application for managing a stock portfolio. This application allows users to buy and sell stocks, track their portfolio, and view transaction history.

## Features

- **Portfolio Management**: Track cash and stock holdings
- **Buy/Sell Orders**: Execute buy and sell orders for various stocks
- **Transaction History**: View all past transactions
- **Market Prices**: View current market prices for available stocks
- **Persistent Storage**: Portfolio data is saved and loaded automatically

## Available Stocks

- AAPL (Apple Inc.)
- GOOGL (Alphabet Inc.)
- MSFT (Microsoft Corporation)
- AMZN (Amazon.com Inc.)
- TSLA (Tesla Inc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/adeelciit786-hue/Trader.git
cd Trader
```

2. No external dependencies required! This application uses only Python standard library.

## Usage

### Running the Application

```bash
python trader.py
```

### Available Commands

- `help` - Show help message with all available commands
- `portfolio` - Display current portfolio (cash and holdings)
- `history` - Show transaction history
- `prices` - Display current market prices for all stocks
- `buy <symbol> <quantity>` - Buy shares (e.g., `buy AAPL 10`)
- `sell <symbol> <quantity>` - Sell shares (e.g., `sell AAPL 5`)
- `exit` or `quit` - Exit the application

### Example Session

```
$ python trader.py
Welcome to Trader!
Type 'help' for available commands

trader> prices
=== Market Prices ===
AAPL: $150.00
AMZN: $3300.00
GOOGL: $2800.00
MSFT: $300.00
TSLA: $800.00

trader> buy AAPL 10
Successfully bought 10 shares of AAPL at $150.00

trader> portfolio
=== Portfolio ===
Cash: $8500.00

Holdings:
  AAPL: 10 shares @ $150.00 = $1500.00

Total Portfolio Value: $10000.00

trader> sell AAPL 5
Successfully sold 5 shares of AAPL at $150.00

trader> history
=== Transaction History ===
2026-01-03T10:30:00: BUY 10 AAPL @ $150.00 (Total: $1500.00)
2026-01-03T10:31:00: SELL 5 AAPL @ $150.00 (Total: $750.00)

trader> exit
Goodbye!
```

## Testing

Run the test suite:

```bash
python test_trader.py
```

Or with verbose output:

```bash
python test_trader.py -v
```

## Data Storage

Portfolio data is automatically saved to `trader_data.json` in the current directory. This file is created automatically when you make your first transaction and is loaded on subsequent runs.

## Architecture

The application consists of two main classes:

### Portfolio Class
- Manages cash and stock holdings
- Executes buy and sell orders
- Tracks transaction history
- Calculates portfolio value
- Handles serialization/deserialization

### Trader Class
- Provides the main application interface
- Manages market prices
- Handles persistent storage
- Implements the command-line interface

## License

This project is open source and available under the MIT License.

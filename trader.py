#!/usr/bin/env python3
"""
Trader - A simple command-line trading application
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class Portfolio:
    """Manages the trading portfolio including cash and holdings."""
    
    def __init__(self, initial_cash: float = 10000.0):
        self.cash = initial_cash
        self.holdings: Dict[str, int] = {}  # symbol -> quantity
        self.transaction_history: List[Dict] = []
    
    def buy(self, symbol: str, quantity: int, price: float) -> bool:
        """Execute a buy order."""
        if quantity <= 0 or price < 0:
            return False
        
        total_cost = quantity * price
        if total_cost > self.cash:
            return False
        
        self.cash -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        
        self.transaction_history.append({
            'type': 'BUY',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_cost,
            'timestamp': datetime.now().isoformat()
        })
        return True
    
    def sell(self, symbol: str, quantity: int, price: float) -> bool:
        """Execute a sell order."""
        if quantity <= 0 or price < 0:
            return False
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False
        
        total_value = quantity * price
        self.cash += total_value
        self.holdings[symbol] -= quantity
        
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self.transaction_history.append({
            'type': 'SELL',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_value,
            'timestamp': datetime.now().isoformat()
        })
        return True
    
    def get_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """Calculate total portfolio value including cash and holdings."""
        holdings_value = sum(
            quantity * current_prices.get(symbol, 0)
            for symbol, quantity in self.holdings.items()
        )
        return self.cash + holdings_value
    
    def to_dict(self) -> Dict:
        """Convert portfolio to dictionary for serialization."""
        return {
            'cash': self.cash,
            'holdings': self.holdings,
            'transaction_history': self.transaction_history
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Portfolio':
        """Create portfolio from dictionary."""
        portfolio = cls(initial_cash=data['cash'])
        portfolio.holdings = data.get('holdings', {})
        portfolio.transaction_history = data.get('transaction_history', [])
        return portfolio


class Trader:
    """Main trading application class."""
    
    def __init__(self, data_file: str = 'trader_data.json'):
        self.data_file = data_file
        self.portfolio = self.load_portfolio()
        self.market_prices: Dict[str, float] = {
            'AAPL': 150.0,
            'GOOGL': 2800.0,
            'MSFT': 300.0,
            'AMZN': 3300.0,
            'TSLA': 800.0
        }
    
    def load_portfolio(self) -> Portfolio:
        """Load portfolio from file or create new one."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                return Portfolio.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                return Portfolio()
        return Portfolio()
    
    def save_portfolio(self):
        """Save portfolio to file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.portfolio.to_dict(), f, indent=2)
        except IOError as e:
            print(f"Error saving portfolio: {e}")
    
    def place_buy_order(self, symbol: str, quantity: int) -> bool:
        """Place a buy order."""
        if symbol not in self.market_prices:
            print(f"Error: Unknown symbol {symbol}")
            return False
        
        if quantity <= 0:
            print(f"Error: Quantity must be positive")
            return False
        
        price = self.market_prices[symbol]
        if self.portfolio.buy(symbol, quantity, price):
            print(f"Successfully bought {quantity} shares of {symbol} at ${price:.2f}")
            self.save_portfolio()
            return True
        else:
            print(f"Error: Insufficient funds to buy {quantity} shares of {symbol}")
            return False
    
    def place_sell_order(self, symbol: str, quantity: int) -> bool:
        """Place a sell order."""
        if symbol not in self.market_prices:
            print(f"Error: Unknown symbol {symbol}")
            return False
        
        if quantity <= 0:
            print(f"Error: Quantity must be positive")
            return False
        
        price = self.market_prices[symbol]
        if self.portfolio.sell(symbol, quantity, price):
            print(f"Successfully sold {quantity} shares of {symbol} at ${price:.2f}")
            self.save_portfolio()
            return True
        else:
            print(f"Error: Insufficient shares of {symbol} to sell")
            return False
    
    def show_portfolio(self):
        """Display current portfolio."""
        print("\n=== Portfolio ===")
        print(f"Cash: ${self.portfolio.cash:.2f}")
        print("\nHoldings:")
        if self.portfolio.holdings:
            for symbol, quantity in self.portfolio.holdings.items():
                price = self.market_prices.get(symbol, 0)
                value = quantity * price
                print(f"  {symbol}: {quantity} shares @ ${price:.2f} = ${value:.2f}")
        else:
            print("  No holdings")
        
        total_value = self.portfolio.get_portfolio_value(self.market_prices)
        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
    
    def show_transaction_history(self):
        """Display transaction history."""
        print("\n=== Transaction History ===")
        if not self.portfolio.transaction_history:
            print("No transactions yet")
            return
        
        for transaction in self.portfolio.transaction_history:
            print(f"{transaction['timestamp']}: {transaction['type']} {transaction['quantity']} "
                  f"{transaction['symbol']} @ ${transaction['price']:.2f} "
                  f"(Total: ${transaction['total']:.2f})")
    
    def show_market_prices(self):
        """Display current market prices."""
        print("\n=== Market Prices ===")
        for symbol, price in sorted(self.market_prices.items()):
            print(f"{symbol}: ${price:.2f}")
    
    def run_cli(self):
        """Run the command-line interface."""
        print("Welcome to Trader!")
        print("Type 'help' for available commands")
        
        while True:
            try:
                command = input("\ntrader> ").strip().lower()
                
                if command == 'help':
                    self.show_help()
                elif command == 'portfolio':
                    self.show_portfolio()
                elif command == 'history':
                    self.show_transaction_history()
                elif command == 'prices':
                    self.show_market_prices()
                elif command.startswith('buy '):
                    parts = command.split()
                    if len(parts) == 3:
                        try:
                            symbol = parts[1].upper()
                            quantity = int(parts[2])
                            self.place_buy_order(symbol, quantity)
                        except ValueError:
                            print("Error: Quantity must be a valid number")
                    else:
                        print("Usage: buy <symbol> <quantity>")
                elif command.startswith('sell '):
                    parts = command.split()
                    if len(parts) == 3:
                        try:
                            symbol = parts[1].upper()
                            quantity = int(parts[2])
                            self.place_sell_order(symbol, quantity)
                        except ValueError:
                            print("Error: Quantity must be a valid number")
                    else:
                        print("Usage: sell <symbol> <quantity>")
                elif command == 'exit' or command == 'quit':
                    print("Goodbye!")
                    break
                elif command == '':
                    continue
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
            except ValueError:
                print("Error: Invalid input. Please check your command.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        """Display help message."""
        print("\nAvailable commands:")
        print("  help                  - Show this help message")
        print("  portfolio             - Show current portfolio")
        print("  history               - Show transaction history")
        print("  prices                - Show current market prices")
        print("  buy <symbol> <qty>    - Buy shares (e.g., buy AAPL 10)")
        print("  sell <symbol> <qty>   - Sell shares (e.g., sell AAPL 5)")
        print("  exit / quit           - Exit the application")


def main():
    """Main entry point."""
    trader = Trader()
    trader.run_cli()


if __name__ == '__main__':
    main()

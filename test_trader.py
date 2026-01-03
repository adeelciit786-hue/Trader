#!/usr/bin/env python3
"""
Unit tests for the Trader application
"""

import unittest
import os
import json
from trader import Portfolio, Trader


class TestPortfolio(unittest.TestCase):
    """Test cases for Portfolio class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.portfolio = Portfolio(initial_cash=10000.0)
    
    def test_initial_cash(self):
        """Test portfolio initialization with cash."""
        self.assertEqual(self.portfolio.cash, 10000.0)
        self.assertEqual(len(self.portfolio.holdings), 0)
    
    def test_buy_success(self):
        """Test successful buy order."""
        result = self.portfolio.buy('AAPL', 10, 150.0)
        self.assertTrue(result)
        self.assertEqual(self.portfolio.cash, 8500.0)
        self.assertEqual(self.portfolio.holdings['AAPL'], 10)
        self.assertEqual(len(self.portfolio.transaction_history), 1)
    
    def test_buy_insufficient_funds(self):
        """Test buy order with insufficient funds."""
        result = self.portfolio.buy('AAPL', 100, 150.0)
        self.assertFalse(result)
        self.assertEqual(self.portfolio.cash, 10000.0)
        self.assertEqual(len(self.portfolio.holdings), 0)
    
    def test_sell_success(self):
        """Test successful sell order."""
        self.portfolio.buy('AAPL', 10, 150.0)
        result = self.portfolio.sell('AAPL', 5, 155.0)
        self.assertTrue(result)
        self.assertEqual(self.portfolio.cash, 9275.0)  # 8500 + 5*155
        self.assertEqual(self.portfolio.holdings['AAPL'], 5)
        self.assertEqual(len(self.portfolio.transaction_history), 2)
    
    def test_sell_insufficient_shares(self):
        """Test sell order with insufficient shares."""
        self.portfolio.buy('AAPL', 10, 150.0)
        result = self.portfolio.sell('AAPL', 20, 155.0)
        self.assertFalse(result)
        self.assertEqual(self.portfolio.holdings['AAPL'], 10)
    
    def test_sell_nonexistent_symbol(self):
        """Test sell order for symbol not in holdings."""
        result = self.portfolio.sell('GOOGL', 10, 2800.0)
        self.assertFalse(result)
    
    def test_sell_all_shares(self):
        """Test selling all shares removes symbol from holdings."""
        self.portfolio.buy('AAPL', 10, 150.0)
        self.portfolio.sell('AAPL', 10, 155.0)
        self.assertNotIn('AAPL', self.portfolio.holdings)
    
    def test_multiple_buys_same_symbol(self):
        """Test multiple buy orders for the same symbol."""
        self.portfolio.buy('AAPL', 10, 150.0)
        self.portfolio.buy('AAPL', 5, 155.0)
        self.assertEqual(self.portfolio.holdings['AAPL'], 15)
    
    def test_portfolio_value(self):
        """Test portfolio value calculation."""
        self.portfolio.buy('AAPL', 10, 150.0)
        self.portfolio.buy('GOOGL', 2, 2800.0)
        
        current_prices = {'AAPL': 160.0, 'GOOGL': 2900.0}
        value = self.portfolio.get_portfolio_value(current_prices)
        
        # Initial: 10000, After AAPL: 8500, After GOOGL: 2900
        expected = 2900.0 + (10 * 160.0) + (2 * 2900.0)  # cash + holdings
        self.assertEqual(value, expected)
    
    def test_to_dict(self):
        """Test portfolio serialization."""
        self.portfolio.buy('AAPL', 10, 150.0)
        data = self.portfolio.to_dict()
        
        self.assertIn('cash', data)
        self.assertIn('holdings', data)
        self.assertIn('transaction_history', data)
        self.assertEqual(data['cash'], 8500.0)
        self.assertEqual(data['holdings']['AAPL'], 10)
    
    def test_from_dict(self):
        """Test portfolio deserialization."""
        data = {
            'cash': 5000.0,
            'holdings': {'AAPL': 10, 'GOOGL': 2},
            'transaction_history': []
        }
        portfolio = Portfolio.from_dict(data)
        
        self.assertEqual(portfolio.cash, 5000.0)
        self.assertEqual(portfolio.holdings['AAPL'], 10)
        self.assertEqual(portfolio.holdings['GOOGL'], 2)


class TestTrader(unittest.TestCase):
    """Test cases for Trader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_file = 'test_trader_data.json'
        self.trader = Trader(data_file=self.test_file)
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_initialization(self):
        """Test trader initialization."""
        self.assertIsNotNone(self.trader.portfolio)
        self.assertIsNotNone(self.trader.market_prices)
        self.assertEqual(self.trader.data_file, self.test_file)
    
    def test_place_buy_order_success(self):
        """Test successful buy order."""
        result = self.trader.place_buy_order('AAPL', 10)
        self.assertTrue(result)
        self.assertEqual(self.trader.portfolio.holdings['AAPL'], 10)
    
    def test_place_buy_order_unknown_symbol(self):
        """Test buy order with unknown symbol."""
        result = self.trader.place_buy_order('UNKNOWN', 10)
        self.assertFalse(result)
    
    def test_place_sell_order_success(self):
        """Test successful sell order."""
        self.trader.place_buy_order('AAPL', 10)
        result = self.trader.place_sell_order('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.trader.portfolio.holdings['AAPL'], 5)
    
    def test_place_sell_order_insufficient_shares(self):
        """Test sell order with insufficient shares."""
        result = self.trader.place_sell_order('AAPL', 10)
        self.assertFalse(result)
    
    def test_save_and_load_portfolio(self):
        """Test saving and loading portfolio."""
        self.trader.place_buy_order('AAPL', 10)
        self.trader.save_portfolio()
        
        # Create new trader instance
        new_trader = Trader(data_file=self.test_file)
        self.assertEqual(new_trader.portfolio.holdings['AAPL'], 10)
    
    def test_market_prices_available(self):
        """Test that market prices are available."""
        self.assertIn('AAPL', self.trader.market_prices)
        self.assertIn('GOOGL', self.trader.market_prices)
        self.assertIn('MSFT', self.trader.market_prices)


if __name__ == '__main__':
    unittest.main()

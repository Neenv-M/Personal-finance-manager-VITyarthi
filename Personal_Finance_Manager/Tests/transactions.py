import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.transaction import Transaction
from models.user import User
from datetime import datetime

class TestTransactions(unittest.TestCase):
    def setUp(self):
        self.user = User.create("testuser_trans", "test_trans@example.com", "password123")
        self.assertIsNotNone(self.user)

    def test_transaction_creation(self):
        """Test transaction creation and retrieval"""
        transaction = Transaction(
            user_id=self.user.id,
            amount=100.50,
            description="Test transaction",
            category="Test",
            type="expense",
            transaction_date="2024-01-01"
        )
        
        result = transaction.save()
        self.assertTrue(result)
        self.assertIsNotNone(transaction.id)

    def test_transaction_retrieval(self):
        """Test retrieving user transactions"""
        transactions = Transaction.get_user_transactions(self.user.id)
        self.assertIsInstance(transactions, list)

    def test_transaction_deletion(self):
        """Test transaction deletion"""
        transaction = Transaction(
            user_id=self.user.id,
            amount=50.00,
            description="To be deleted",
            category="Test",
            type="expense"
        )
        transaction.save()
        
        result = Transaction.delete(transaction.id)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.user import User

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_user_creation(self):
        """Test user creation functionality"""
        user = User.create("testuser", "test@example.com", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_duplicate_username(self):
        """Test duplicate username prevention"""
        User.create("testuser2", "test2@example.com", "password123")
        user2 = User.create("testuser2", "test3@example.com", "password123")
        self.assertIsNone(user2)

    def test_password_hashing(self):
        """Test password hashing and verification"""
        user = User.create("testuser3", "test3@example.com", "password123")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.check_password("wrongpassword"))

if __name__ == '__main__':
    unittest.main()
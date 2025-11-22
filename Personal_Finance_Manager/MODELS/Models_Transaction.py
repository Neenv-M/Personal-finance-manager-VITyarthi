import mysql.connector
from config import Config
from datetime import datetime

class Transaction:
    def __init__(self, id=None, user_id=None, amount=0, description="", category="Other", 
                 type="expense", transaction_date=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.category = category
        self.type = type
        self.transaction_date = transaction_date or datetime.now().date()

    def save(self):
        try:
            conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
            cursor = conn.cursor()
            
            if self.id:
                cursor.execute(
                    """UPDATE transactions SET amount=%s, description=%s, category=%s, 
                    type=%s, transaction_date=%s WHERE id=%s""",
                    (self.amount, self.description, self.category, self.type, 
                     self.transaction_date, self.id)
                )
            else:
                cursor.execute(
                    """INSERT INTO transactions (user_id, amount, description, category, type, transaction_date) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (self.user_id, self.amount, self.description, self.category, 
                     self.type, self.transaction_date)
                )
                self.id = cursor.lastrowid
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving transaction: {e}")
            return False

    @staticmethod
    def get_user_transactions(user_id, limit=None):
        try:
            conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM transactions WHERE user_id = %s ORDER BY transaction_date DESC"
            if limit:
                query += " LIMIT %s"
                cursor.execute(query, (user_id, limit))
            else:
                cursor.execute(query, (user_id,))
            
            transactions_data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            transactions = []
            for data in transactions_data:
                transactions.append(Transaction(
                    id=data['id'],
                    user_id=data['user_id'],
                    amount=float(data['amount']),
                    description=data['description'],
                    category=data['category'],
                    type=data['type'],
                    transaction_date=data['transaction_date']
                ))
            
            return transactions
        except Exception as e:
            print(f"Error getting user transactions: {e}")
            return []

    @staticmethod
    def delete(transaction_id):
        try:
            conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
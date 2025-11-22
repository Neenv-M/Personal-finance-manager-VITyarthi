import mysql.connector
from config import Config

class Budget:
    def __init__(self, id=None, user_id=None, category=None, amount=0, month_year=None):
        self.id = id
        self.user_id = user_id
        self.category = category
        self.amount = amount
        self.month_year = month_year

    def save(self):
        try:
            conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
            cursor = conn.cursor()
            
            if self.id:
                cursor.execute(
                    """UPDATE budgets SET category=%s, amount=%s, month_year=%s WHERE id=%s""",
                    (self.category, self.amount, self.month_year, self.id)
                )
            else:
                cursor.execute(
                    """INSERT INTO budgets (user_id, category, amount, month_year) 
                    VALUES (%s, %s, %s, %s)""",
                    (self.user_id, self.category, self.amount, self.month_year)
                )
                self.id = cursor.lastrowid
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving budget: {e}")
            return False

    @staticmethod
    def get_user_budgets(user_id, month_year=None):
        try:
            conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            if month_year:
                cursor.execute(
                    "SELECT * FROM budgets WHERE user_id = %s AND month_year = %s",
                    (user_id, month_year)
                )
            else:
                cursor.execute(
                    "SELECT * FROM budgets WHERE user_id = %s",
                    (user_id,)
                )
            
            budgets_data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            budgets = []
            for data in budgets_data:
                budgets.append(Budget(
                    id=data['id'],
                    user_id=data['user_id'],
                    category=data['category'],
                    amount=float(data['amount']),
                    month_year=data['month_year']
                ))
            
            return budgets
        except Exception as e:
            print(f"Error getting user budgets: {e}")
            return []
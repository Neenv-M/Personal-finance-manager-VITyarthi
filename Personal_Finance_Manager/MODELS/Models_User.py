import mysql.connector
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get_by_id(user_id):
        try:
            conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash']
                )
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None

    @staticmethod
    def get_by_username(username):
        try:
            conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash']
                )
            return None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None

    @staticmethod
    def create(username, email, password):
        try:
            password_hash = generate_password_hash(password)
            conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash)
            )
            
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            return User(user_id, username, email, password_hash)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
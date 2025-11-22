import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    MYSQL_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'personal_finance',
        'auth_plugin': 'mysql_native_password'
    }
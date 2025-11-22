#!/usr/bin/env python3
"""
Personal Finance Manager - Startup Script
"""
import os
import mysql.connector
from app import app
from config import Config

def setup_database():
    """Initialize database with required tables"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_CONFIG['host'],
            user=Config.MYSQL_CONFIG['user'],
            password=Config.MYSQL_CONFIG['password']
        )
        cursor = conn.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS personal_finance")
        print("✅ Database created or already exists")
        
        cursor.close()
        conn.close()
        
        with open('database/schema.sql', 'r') as f:
            schema_sql = f.read()
        
        conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
        cursor = conn.cursor()
        
        for statement in schema_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database schema initialized successfully")
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        print("Please make sure MySQL is running and credentials in config.py are correct")

if __name__ == '__main__':
    print("🚀 Starting AI Personal Finance Manager...")
    
    setup_database()
    
    os.makedirs('ml_models/trained_models', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("✅ Starting Flask application...")
    print("📱 Application will be available at: http://localhost:5000")
    print("📍 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
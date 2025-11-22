from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.user import User
from models.transaction import Transaction
from models.budget import Budget
from ml_models.ai_categorizer import ExpenseCategorizer
from ml_models.spending_predictor import SpendingPredictor
from ml_models.anomaly_detector import AnomalyDetector
import mysql.connector
from config import Config
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# AI Models
categorizer = ExpenseCategorizer()
predictor = SpendingPredictor()
anomaly_detector = AnomalyDetector()

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.get_by_username(username):
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        user = User.create(username, email, password)
        if user:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    transactions = Transaction.get_user_transactions(current_user.id)
    
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expenses
    
    recent_transactions = transactions[:5]
    financial_health = calculate_financial_health(transactions)
    
    return render_template('dashboard.html',
                         total_income=total_income,
                         total_expenses=total_expenses,
                         balance=balance,
                         recent_transactions=recent_transactions,
                         financial_health=financial_health)

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form['description']
        transaction_type = request.form['type']
        date = request.form['date']
        
        category = categorizer.predict_category(description, amount, transaction_type)
        
        transaction = Transaction(
            user_id=current_user.id,
            amount=amount,
            description=description,
            category=category,
            type=transaction_type,
            transaction_date=date
        )
        
        if transaction.save():
            flash('Transaction added successfully!', 'success')
        else:
            flash('Error adding transaction', 'error')
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_transaction.html')

@app.route('/analytics')
@login_required
def analytics():
    transactions = Transaction.get_user_transactions(current_user.id)
    
    spending_trends = predictor.analyze_spending_trends(transactions)
    anomalies = anomaly_detector.detect_anomalies(transactions)
    predictions = predictor.predict_future_spending(transactions)
    
    return render_template('analytics.html',
                         spending_trends=spending_trends,
                         anomalies=anomalies,
                         predictions=predictions)

@app.route('/api/transaction_categories')
@login_required
def get_transaction_categories():
    transactions = Transaction.get_user_transactions(current_user.id)
    categories = {}
    
    for transaction in transactions:
        if transaction.type == 'expense':
            categories[transaction.category] = categories.get(transaction.category, 0) + transaction.amount
    
    return jsonify(categories)

def calculate_financial_health(transactions):
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    
    if total_income == 0:
        return 0
    
    savings_rate = (total_income - total_expenses) / total_income
    health_score = min(100, max(0, savings_rate * 100))
    
    return round(health_score)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
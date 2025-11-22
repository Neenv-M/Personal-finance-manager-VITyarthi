from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models.transaction import Transaction
from ml_models.spending_predictor import SpendingPredictor
from ml_models.anomaly_detector import AnomalyDetector

analytics_bp = Blueprint('analytics', __name__)
predictor = SpendingPredictor()
anomaly_detector = AnomalyDetector()

@analytics_bp.route('/analytics')
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

@analytics_bp.route('/api/transaction_categories')
@login_required
def get_transaction_categories():
    transactions = Transaction.get_user_transactions(current_user.id)
    categories = {}
    
    for transaction in transactions:
        if transaction.type == 'expense':
            categories[transaction.category] = categories.get(transaction.category, 0) + transaction.amount
    
    return jsonify(categories)

@analytics_bp.route('/api/spending_trends')
@login_required
def get_spending_trends():
    transactions = Transaction.get_user_transactions(current_user.id)
    trends = predictor.analyze_spending_trends(transactions)
    return jsonify(trends)
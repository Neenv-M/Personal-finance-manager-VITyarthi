from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models.transaction import Transaction
from ml_models.ai_categorizer import ExpenseCategorizer
from ml_models.spending_predictor import SpendingPredictor
from ml_models.anomaly_detector import AnomalyDetector

ai_insights_bp = Blueprint('ai_insights', __name__)
categorizer = ExpenseCategorizer()
predictor = SpendingPredictor()
anomaly_detector = AnomalyDetector()

@ai_insights_bp.route('/api/ai/predict_category', methods=['POST'])
@login_required
def predict_category():
    data = request.json
    description = data.get('description', '')
    amount = data.get('amount', 0)
    transaction_type = data.get('type', 'expense')
    
    category = categorizer.predict_category(description, amount, transaction_type)
    
    return jsonify({
        'category': category,
        'confidence': 'high'  # Simplified for demo
    })

@ai_insights_bp.route('/api/ai/financial_health')
@login_required
def get_financial_health():
    transactions = Transaction.get_user_transactions(current_user.id)
    
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    
    if total_income == 0:
        score = 0
    else:
        savings_rate = (total_income - total_expenses) / total_income
        score = min(100, max(0, savings_rate * 100))
    
    # Determine health level
    if score >= 80:
        level = "Excellent"
        advice = "Great job! You're managing your finances very well."
    elif score >= 60:
        level = "Good"
        advice = "You're doing well. Consider increasing your savings rate."
    elif score >= 40:
        level = "Fair"
        advice = "Your finances need attention. Try to reduce unnecessary expenses."
    else:
        level = "Poor"
        advice = "Immediate action needed. Review your spending habits and create a budget."
    
    return jsonify({
        'score': round(score),
        'level': level,
        'advice': advice,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': total_income - total_expenses
    })
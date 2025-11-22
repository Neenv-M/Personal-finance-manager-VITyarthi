import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import json

class SpendingPredictor:
    def __init__(self):
        self.model = LinearRegression()
    
    def analyze_spending_trends(self, transactions):
        if not transactions:
            return {
                "average_monthly_spending": 0,
                "spending_volatility": 0,
                "top_categories": {},
                "message": "Insufficient data for analysis"
            }
        
        df = pd.DataFrame([{
            'date': t.transaction_date,
            'amount': t.amount,
            'type': t.type,
            'category': t.category
        } for t in transactions])
        
        df['date'] = pd.to_datetime(df['date'])
        
        monthly_spending = df[df['type'] == 'expense'].groupby(
            df['date'].dt.to_period('M')
        )['amount'].sum()
        
        expense_transactions = df[df['type'] == 'expense']
        top_categories = expense_transactions['category'].value_counts().head(3).to_dict()
        
        trends = {
            'average_monthly_spending': monthly_spending.mean() if not monthly_spending.empty else 0,
            'spending_volatility': monthly_spending.std() if len(monthly_spending) > 1 else 0,
            'top_categories': top_categories,
            'total_transactions': len(transactions),
            'analysis_period': f"{len(monthly_spending)} months"
        }
        
        return trends
    
    def predict_future_spending(self, transactions, months_ahead=1):
        if len(transactions) < 5:
            return {
                'estimated_spending': 0,
                'confidence': 0,
                'prediction_period': f'Next {months_ahead} month(s)',
                'message': 'Insufficient data for prediction'
            }
        
        df = pd.DataFrame([{
            'date': t.transaction_date,
            'amount': t.amount if t.type == 'expense' else 0
        } for t in transactions])
        
        df['date'] = pd.to_datetime(df['date'])
        daily_spending = df.groupby('date')['amount'].sum()
        
        if len(daily_spending) < 5:
            return None
        
        days = np.array(range(len(daily_spending))).reshape(-1, 1)
        amounts = daily_spending.values
        
        self.model.fit(days, amounts)
        
        future_day = len(daily_spending) + (30 * months_ahead)
        predicted_amount = max(0, self.model.predict([[future_day]])[0])
        
        confidence = min(95, max(50, self.model.score(days, amounts) * 100))
        
        return {
            'estimated_spending': round(predicted_amount, 2),
            'confidence': round(confidence),
            'prediction_period': f'Next {months_ahead} month(s)',
            'data_points': len(daily_spending)
        }
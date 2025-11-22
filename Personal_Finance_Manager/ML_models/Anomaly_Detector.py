import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
    
    def detect_anomalies(self, transactions):
        if len(transactions) < 10:
            return []
        
        expense_transactions = [t for t in transactions if t.type == 'expense']
        
        if len(expense_transactions) < 5:
            return []
        
        features = []
        transaction_info = []
        
        for transaction in expense_transactions:
            features.append([
                transaction.amount,
                len(transaction.description),
                self.category_to_numeric(transaction.category),
                self.date_to_numeric(transaction.transaction_date)
            ])
            transaction_info.append(transaction)
        
        X = np.array(features)
        anomalies = self.model.fit_predict(X)
        
        anomalous_transactions = []
        for i, is_anomaly in enumerate(anomalies):
            if is_anomaly == -1:
                anomalous_transactions.append({
                    'description': transaction_info[i].description,
                    'amount': transaction_info[i].amount,
                    'category': transaction_info[i].category,
                    'date': transaction_info[i].transaction_date,
                    'reason': self.get_anomaly_reason(transaction_info[i])
                })
        
        return anomalous_transactions
    
    def category_to_numeric(self, category):
        category_mapping = {
            'Food': 1, 'Transportation': 2, 'Entertainment': 3,
            'Shopping': 4, 'Bills': 5, 'Healthcare': 6,
            'Education': 7, 'Other': 8, 'Income': 9
        }
        return category_mapping.get(category, 8)
    
    def date_to_numeric(self, date):
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        return date.toordinal()
    
    def get_anomaly_reason(self, transaction):
        reasons = []
        
        if transaction.amount > 500:
            reasons.append("Unusually high amount")
        
        if len(transaction.description) < 3:
            reasons.append("Very short description")
        
        if transaction.category == 'Other':
            reasons.append("Uncategorized transaction")
        
        return ", ".join(reasons) if reasons else "Unusual spending pattern"
    
    def calculate_anomaly_score(self, transaction):
        features = np.array([[
            transaction.amount,
            len(transaction.description),
            self.category_to_numeric(transaction.category),
            self.date_to_numeric(transaction.transaction_date)
        ]])
        
        score = self.model.decision_function(features)[0]
        return score
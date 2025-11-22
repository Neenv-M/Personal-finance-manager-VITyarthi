import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import joblib
import os
from models.transaction import Transaction

class ExpenseCategorizer:
    def __init__(self):
        self.model = None
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.scaler = StandardScaler()
        self.categories = ['Food', 'Transportation', 'Entertainment', 'Shopping', 'Bills', 'Healthcare', 'Education', 'Other']
        self.model_path = 'ml_models/trained_models/categorizer_model.joblib'
        self.vectorizer_path = 'ml_models/trained_models/vectorizer.joblib'
        self.scaler_path = 'ml_models/trained_models/scaler.joblib'
        
        self.load_or_train_model()

    def load_or_train_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.scaler = joblib.load(self.scaler_path)
                print("✅ AI Model loaded successfully")
                return
            except Exception as e:
                print(f"❌ Error loading model: {e}")
        
        self.train_with_sample_data()

    def train_with_sample_data(self):
        print("🔄 Training AI model with sample data...")
        
        sample_data = [
            # Food related
            {"description": "grocery store shopping", "amount": 85.50, "type": "expense", "category": "Food"},
            {"description": "restaurant dinner", "amount": 45.00, "type": "expense", "category": "Food"},
            {"description": "coffee shop", "amount": 5.75, "type": "expense", "category": "Food"},
            {"description": "pizza delivery", "amount": 25.99, "type": "expense", "category": "Food"},
            {"description": "supermarket", "amount": 120.00, "type": "expense", "category": "Food"},
            {"description": "bakery", "amount": 15.25, "type": "expense", "category": "Food"},
            
            # Transportation
            {"description": "gas station", "amount": 40.00, "type": "expense", "category": "Transportation"},
            {"description": "uber ride", "amount": 15.50, "type": "expense", "category": "Transportation"},
            {"description": "bus ticket", "amount": 2.50, "type": "expense", "category": "Transportation"},
            {"description": "train fare", "amount": 8.75, "type": "expense", "category": "Transportation"},
            {"description": "car maintenance", "amount": 85.00, "type": "expense", "category": "Transportation"},
            
            # Entertainment
            {"description": "movie tickets", "amount": 30.00, "type": "expense", "category": "Entertainment"},
            {"description": "netflix subscription", "amount": 15.99, "type": "expense", "category": "Entertainment"},
            {"description": "concert tickets", "amount": 75.00, "type": "expense", "category": "Entertainment"},
            {"description": "bowling", "amount": 25.50, "type": "expense", "category": "Entertainment"},
            
            # Shopping
            {"description": "clothing store", "amount": 75.00, "type": "expense", "category": "Shopping"},
            {"description": "electronics purchase", "amount": 299.99, "type": "expense", "category": "Shopping"},
            {"description": "amazon shopping", "amount": 45.80, "type": "expense", "category": "Shopping"},
            {"description": "book store", "amount": 32.50, "type": "expense", "category": "Shopping"},
            
            # Bills
            {"description": "electricity bill", "amount": 120.00, "type": "expense", "category": "Bills"},
            {"description": "internet bill", "amount": 65.00, "type": "expense", "category": "Bills"},
            {"description": "phone bill", "amount": 45.50, "type": "expense", "category": "Bills"},
            {"description": "rent payment", "amount": 500.00, "type": "expense", "category": "Bills"},
            
            # Healthcare
            {"description": "pharmacy", "amount": 35.50, "type": "expense", "category": "Healthcare"},
            {"description": "doctor visit", "amount": 100.00, "type": "expense", "category": "Healthcare"},
            {"description": "hospital", "amount": 250.00, "type": "expense", "category": "Healthcare"},
            {"description": "medicine", "amount": 28.75, "type": "expense", "category": "Healthcare"},
            
            # Education
            {"description": "book store", "amount": 45.00, "type": "expense", "category": "Education"},
            {"description": "online course", "amount": 89.99, "type": "expense", "category": "Education"},
            {"description": "university fees", "amount": 1200.00, "type": "expense", "category": "Education"},
            {"description": "stationery", "amount": 15.25, "type": "expense", "category": "Education"},
            
            # Income
            {"description": "salary payment", "amount": 1500.00, "type": "income", "category": "Income"},
            {"description": "freelance work", "amount": 300.00, "type": "income", "category": "Income"},
            {"description": "bonus", "amount": 200.00, "type": "income", "category": "Income"},
        ]
        
        df = pd.DataFrame(sample_data)
        X = self.preprocess_features(df[['description', 'amount', 'type']])
        y = df['category']
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        os.makedirs('ml_models/trained_models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        print("✅ AI Model trained and saved successfully")
        print(f"✅ Model accuracy: {self.model.score(X, y):.2f}")

    def preprocess_features(self, data):
        descriptions = data['description'].fillna('')
        text_features = self.vectorizer.fit_transform(descriptions).toarray()
        
        numerical_features = data[['amount']].values
        numerical_features = self.scaler.fit_transform(numerical_features)
        
        type_features = pd.get_dummies(data['type']).values
        
        features = np.hstack([text_features, numerical_features, type_features])
        return features

    def predict_category(self, description, amount, transaction_type):
        if self.model is None:
            return "Other" if transaction_type == "expense" else "Income"
        
        try:
            data = pd.DataFrame([{
                'description': description.lower(),
                'amount': amount,
                'type': transaction_type
            }])
            
            X = self.preprocess_features(data)
            prediction = self.model.predict(X)[0]
            return prediction
        except Exception as e:
            print(f"❌ Error predicting category: {e}")
            return "Other" if transaction_type == "expense" else "Income"

    def retrain_model(self):
        print("🔄 Retraining AI model with new data...")
        self.load_or_train_model()
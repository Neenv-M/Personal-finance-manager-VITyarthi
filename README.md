# **AI-Powered Personal Finance Manager**

## 📋 **Project Overview**

A comprehensive web-based personal finance management system with **AI-powered insights** for expense categorization, spending predictions, and financial health analysis. Built with **Python Flask** and integrated **Machine Learning algorithms**.

---

## 🚀 **Features**

### **Core Features**

* **User Authentication** – Secure registration and login system
* **Transaction Management** – Add, view, and manage income/expense transactions
* **Financial Dashboard** – Real-time financial overview and health scoring

### **AI-Powered Features**

* 🤖 **Smart Categorization** – Automatic expense categorization using Random Forest
* 🔮 **Spending Predictions** – Future expense forecasting using Linear Regression
* ⚠️ **Anomaly Detection** – Identify unusual spending patterns using Isolation Forest
* 📊 **Financial Health Scoring** – Comprehensive financial well-being assessment

---

## 🛠 **Technology Stack**

* **Backend:** Python Flask
* **Database:** MySQL
* **AI/ML:** Scikit-learn, Pandas, NumPy
* **Frontend:** HTML5, Bootstrap 5, Chart.js
* **Authentication:** Flask-Login with password hashing

---

## 📥 **Installation & Setup**

### **Prerequisites**

* Python 3.8 or higher
* MySQL Server
* pip (Python package manager)

### **Step 1: Download and Extract Project**

1. Download all project files
2. Create a folder named **PersonalFinanceManager**
3. Place all files according to the structure shown below

### **Step 2: Set Up Python Environment**

```bash
cd PersonalFinanceManager
python -m venv venv

# Activate environment
# Windows
env/Script/activate
# Mac/Linux
source venv/bin/activate
```

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 4: Configure Database**

Edit `config.py` with your MySQL credentials:

```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'personal_finance',
    'auth_plugin': 'mysql_native_password'
}
```

### **Step 5: Run the Application**

```bash
python run.py
```

### **Step 6: Access the Application**

Open your browser at:

```
http://localhost:5000
```

### 👤 **Default Demo Account**

* **Username:** demo
* **Password:** password

---

## 📁 **Project Structure**

```
PersonalFinanceManager/
├── app.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
├── statement.md
├── models/
│   ├── user.py
│   ├── transaction.py
│   └── budget.py
├── routes/
│   ├── auth.py
│   ├── transactions.py
│   ├── analytics.py
│   └── ai_insights.py
├── ml_models/
│   ├── ai_categorizer.py
│   ├── spending_predictor.py
│   └── anomaly_detector.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── add_transaction.html
│   └── analytics.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── database/
│   └── schema.sql
└── tests/
    ├── test_auth.py
    └── test_transactions.py
```

---

## 🎯 **How to Use**

### **1. First-Time Setup**

Run:

```bash
python run.py
```

This will automatically:

* Create database
* Set up tables
* Load sample data
* Train AI models

### **2. User Registration/Login**

Go to **[http://localhost:5000](http://localhost:5000)** and either:

* Register a new account
* Log in using the demo credentials

### **3. Adding Transactions**

1. Click **Add Transaction**
2. Enter transaction details (Type, Amount, Description, Date)
3. AI automatically categorizes the transaction

### **4. Viewing Analytics**

Visit **Analytics & AI Insights** to view:

* Spending patterns
* AI predictions
* Anomaly detection results
* Financial health score

---

## 🤖 **AI/ML Features Explained**

### **1. Expense Categorization**

* **Algorithm:** Random Forest Classifier
* **Input:** Description, amount, type
* **Output:** Category prediction
* **Categories:** Food, Transportation, Entertainment, Shopping, Bills, Healthcare, Education, Other

### **2. Spending Prediction**

* **Algorithm:** Linear Regression
* **Input:** Historical spending data
* **Output:** Future monthly spending estimate

### **3. Anomaly Detection**

* **Algorithm:** Isolation Forest
* **Purpose:** Detect unusual spending behavior
* **Inputs:** Amount, description length, category patterns

---

## 🐛 **Troubleshooting**

### **Common Issues**

**Port in use**

```bash
# Change port in run.py
app.run(debug=True, host='127.0.0.1', port=5001)
```

**MySQL Connection Error**

* Ensure MySQL is running
* Verify credentials in `config.py`
* Ensure database exists

**Module Not Found**

```bash
pip install -r requirements.txt
```

**Cannot Access localhost**

* Try [http://127.0.0.1:5000](http://127.0.0.1:5000)
* Try [http://0.0.0.0:5000](http://0.0.0.0:5000)
* Check firewall

### **Debugging Checklist**

```bash
python --version
mysql -u root -p
pip list
```

Check terminal logs from:

```bash
python run.py
```

---

## 📊 **API Endpoints**

* **GET /** – Homepage
* **GET /dashboard** – Dashboard
* **GET/POST /add_transaction** – Add transaction
* **GET /analytics** – AI analytics
* **GET /api/transaction_categories** – Chart data

---

## 🧪 **Testing**

Run all tests:

```bash
python -m pytest tests/
```

Run individual tests:

```bash
python tests/test_auth.py
python tests/test_transactions.py
```

---

## 📝 **GitHub Upload Instructions**

### **Method 1: Drag & Drop**

1. Create new GitHub repository
2. Drag all files into it

### **Method 2: Git Commands**

```bash
git init
git add .
git commit -m "Initial commit: AI Personal Finance Manager"
git remote add origin https://github.com/yourusername/personal-finance-manager.git
git push -u origin main
```

---

## 🔧 **Development**

### **Add New Features**

* Add new route files in `/routes`
* Add new templates in `/templates`
* Update navigation in `base.html`

### **Modify AI Models**

* Edit files in `/ml_models`
* Delete trained model files to retrain automatically

---

## 📞 **Support**

* Check troubleshooting section
* Verify prerequisites
* Ensure correct file structure
* Review terminal error logs

---

## 📄 **License**

**Academic Project – VIT Bhopal University**
Course: *Fundamentals in AIML (CSA2001)*
Submitted By: **Neenv Mimani (25BCY10011)**

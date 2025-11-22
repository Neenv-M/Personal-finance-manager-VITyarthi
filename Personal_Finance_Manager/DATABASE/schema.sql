-- Personal Finance Manager Database Schema
-- Created for AI-Powered Personal Finance Management System

SET FOREIGN_KEY_CHECKS=0;

-- Create database
CREATE DATABASE IF NOT EXISTS personal_finance;
USE personal_finance;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    category VARCHAR(50) DEFAULT 'Other',
    type ENUM('income', 'expense') NOT NULL,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_category (category),
    INDEX idx_type (type)
);

-- Budgets table
CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    month_year VARCHAR(7) NOT NULL, -- Format: YYYY-MM
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_budget (user_id, category, month_year),
    INDEX idx_user_month (user_id, month_year)
);

-- Financial goals table
CREATE TABLE IF NOT EXISTS financial_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    target_amount DECIMAL(10,2) NOT NULL,
    current_amount DECIMAL(10,2) DEFAULT 0,
    target_date DATE,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- Insert sample data for demonstration
INSERT IGNORE INTO users (id, username, email, password_hash) VALUES 
(1, 'demo', 'demo@example.com', 'pbkdf2:sha256:260000$K1eBcT6U$hashed_password_here');

-- Sample transactions for demo user
INSERT IGNORE INTO transactions (user_id, amount, description, category, type, transaction_date) VALUES
-- Income transactions
(1, 1500.00, 'Monthly Salary', 'Income', 'income', '2024-11-01'),
(1, 300.00, 'Freelance Work', 'Income', 'income', '2024-11-05'),
(1, 200.00, 'Bonus Payment', 'Income', 'income', '2024-11-10'),

-- Expense transactions - Food
(1, 85.50, 'Grocery shopping at supermarket', 'Food', 'expense', '2024-11-02'),
(1, 45.00, 'Dinner at restaurant', 'Food', 'expense', '2024-11-03'),
(1, 5.75, 'Coffee at Starbucks', 'Food', 'expense', '2024-11-04'),
(1, 25.99, 'Pizza delivery', 'Food', 'expense', '2024-11-07'),

-- Expense transactions - Transportation
(1, 40.00, 'Gas station refill', 'Transportation', 'expense', '2024-11-02'),
(1, 15.50, 'Uber ride to office', 'Transportation', 'expense', '2024-11-06'),
(1, 8.75, 'Train ticket', 'Transportation', 'expense', '2024-11-08'),

-- Expense transactions - Bills
(1, 120.00, 'Electricity bill payment', 'Bills', 'expense', '2024-11-05'),
(1, 65.00, 'Internet bill', 'Bills', 'expense', '2024-11-05'),
(1, 45.50, 'Mobile phone bill', 'Bills', 'expense', '2024-11-06'),

-- Expense transactions - Entertainment
(1, 30.00, 'Movie tickets', 'Entertainment', 'expense', '2024-11-07'),
(1, 15.99, 'Netflix subscription', 'Entertainment', 'expense', '2024-11-10'),

-- Expense transactions - Shopping
(1, 75.00, 'Clothing store purchase', 'Shopping', 'expense', '2024-11-09'),
(1, 45.80, 'Amazon online shopping', 'Shopping', 'expense', '2024-11-11'),

-- Expense transactions - Healthcare
(1, 35.50, 'Pharmacy medicines', 'Healthcare', 'expense', '2024-11-12'),
(1, 100.00, 'Doctor consultation', 'Healthcare', 'expense', '2024-11-12'),

-- Expense transactions - Education
(1, 45.00, 'Book store purchase', 'Education', 'expense', '2024-11-13'),
(1, 89.99, 'Online course subscription', 'Education', 'expense', '2024-11-14');

-- Sample budgets for demo user
INSERT IGNORE INTO budgets (user_id, category, amount, month_year) VALUES
(1, 'Food', 300.00, '2024-11'),
(1, 'Transportation', 150.00, '2024-11'),
(1, 'Bills', 250.00, '2024-11'),
(1, 'Entertainment', 100.00, '2024-11'),
(1, 'Shopping', 200.00, '2024-11'),
(1, 'Healthcare', 150.00, '2024-11'),
(1, 'Education', 100.00, '2024-11');

-- Sample financial goals
INSERT IGNORE INTO financial_goals (user_id, title, target_amount, current_amount, target_date, category) VALUES
(1, 'New Laptop', 50000.00, 15000.00, '2025-06-01', 'Electronics'),
(1, 'Emergency Fund', 100000.00, 25000.00, '2025-12-01', 'Savings'),
(1, 'Vacation Trip', 30000.00, 5000.00, '2025-03-01', 'Travel');

SET FOREIGN_KEY_CHECKS=1;

-- Display creation summary
SELECT 
    'Database Schema Created Successfully' as message,
    COUNT(*) as tables_created 
FROM information_schema.tables 
WHERE table_schema = 'personal_finance';
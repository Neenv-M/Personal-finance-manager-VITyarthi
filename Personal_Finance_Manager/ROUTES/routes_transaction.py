from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.transaction import Transaction
from ml_models.ai_categorizer import ExpenseCategorizer

transactions_bp = Blueprint('transactions', __name__)
categorizer = ExpenseCategorizer()

@transactions_bp.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        try:
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
        
        except ValueError:
            flash('Invalid amount entered', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('add_transaction.html')

@transactions_bp.route('/delete_transaction/<int:transaction_id>')
@login_required
def delete_transaction(transaction_id):
    if Transaction.delete(transaction_id):
        flash('Transaction deleted successfully', 'success')
    else:
        flash('Error deleting transaction', 'error')
    
    return redirect(url_for('dashboard'))

@transactions_bp.route('/api/transactions')
@login_required
def get_transactions_api():
    transactions = Transaction.get_user_transactions(current_user.id)
    transactions_data = []
    
    for transaction in transactions:
        transactions_data.append({
            'id': transaction.id,
            'amount': transaction.amount,
            'description': transaction.description,
            'category': transaction.category,
            'type': transaction.type,
            'date': transaction.transaction_date.strftime('%Y-%m-%d')
        })
    
    return jsonify(transactions_data)
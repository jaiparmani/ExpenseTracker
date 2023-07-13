from flask import Flask, jsonify, request
from dataclasses import dataclass
import datetime

app = Flask(__name__)

# database dictionary to store the expenses
expenses_db = {
    'Food': [Expense('Pizza', 8.5, 'Food', '2022-08-03 10:30:00'),
             Expense('Burger', 6.75, 'Food', '2022-08-03 12:15:00'),
             Expense('Groceries', 40.0, 'Food', '2022-08-04 14:20:00')
             ],
    'Fun': [Expense('Movie', 12.5, 'Fun', '2022-08-01 18:30:00'),
            Expense('Bowling', 15.0, 'Fun', '2022-08-02 14:15:00')
            ]
}


@dataclass
class Expense:
    description: str
    amount: float
    category: str
    timestamp: str


@app.route('/expense/<string:category>', methods=['GET'])
def get_expenses(category):
    result = []
    if category in expenses_db:
        result = [expense.__dict__ for expense in expenses_db[category]]
    return jsonify(result)


@app.route('/add_expense', methods=['POST'])
def add_expense():
    expense_data = request.get_json()
    expense = Expense(
        description=expense_data['description'],
        amount=expense_data['amount'],
        category=expense_data['category'],
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    expenses_db[expense.category].append(expense)
    return "Expense added", 201


if __name__ == '__main__':
    app.run(debug=True)

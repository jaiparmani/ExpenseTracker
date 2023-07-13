import json
from datetime import datetime
from typing import Dict, List

from flask import Flask, jsonify, request

app = Flask(__name__)

filepath = "data.json"


class Expense:
    def __init__(self, desc: str, amt: float, category: str, timestamp: datetime) -> None:
        self.desc = desc
        self.amt = amt
        self.category = category
        self.timestamp = timestamp

    def to_dict(self) -> Dict:
        return {
            "description": self.desc,
            "amount": self.amt,
            "category": self.category,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }


class User:
    def __init__(self, username: str, expenses: List[Expense]) -> None:
        self.username = username
        self.expenses = expenses

    def to_dict(self) -> Dict:
        return {
            "username": self.username,
            "expenses": [expense.to_dict() for expense in self.expenses],
        }


def load_data() -> Dict:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return {}


def save_data(data: Dict) -> None:
    with open(filepath, "w") as f:
        json.dump(data, f)


def add_expense(username: str, desc: str, amt: float, category: str, timestamp: datetime) -> str:
    data = load_data()
    if username not in data:
        data[username] = {"expenses": []}
    user = User(username, [Expense(desc, amt, category, timestamp)])
    data[username]["expenses"].append(user.to_dict()["expenses"][0])
    save_data(data)
    return "Added expense successfully."


def get_expenses(username: str) -> List[Expense]:
    data = load_data()
    if username in data:
        user_dict = data[username]
        expenses_dicts = user_dict.get("expenses", [])
        return [Expense(**d) for d in expenses_dicts]
    return []
    

def get_expenses_by_category(username: str, category: str) -> List[Expense]:
    expenses = get_expenses(username)
    return [expense for expense in expenses if expense.category == category]


@app.route("/api/users/<int:user_id>/expenses", methods=["GET", "POST"])
def expenses(user_id: int):
    if request.method == "GET":
        expenses = get_expenses(f"user{user_id}")
        return jsonify([expense.to_dict() for expense in expenses])
    elif request.method == "POST":
        data = request.get_json()
        desc = data.get("description", "")
        amt = data.get("amount", 0.0)
        category = data.get("category", "")
        timestamp = datetime.now()
        result = add_expense(f"user{user_id}", desc, amt, category, timestamp)
        return jsonify({"result": result})


@app.route("/api/users/<int:user_id>/categories/<category>", methods=["GET"])
def expenses_by_category(user_id: int, category: str):
    expenses = get_expenses_by_category(f"user{user_id}", category)
    return jsonify([expense.to_dict() for expense in expenses])


if __name__ == "__main__":
    app.run(debug=True)
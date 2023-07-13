import json
from datetime import datetime
from typing import Dict, List

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

filepath = "data.json"


class Expense:
    def __init__(self, desc: str, amt: float, category: str, timestamp: datetime) -> None:
        self.desc = desc
        self.amt = amt
        self.category = category
        self.timestamp = timestamp

    def to_dict(self) -> Dict:
        return {
            "desc": self.desc,
            "amt": self.amt,
            "category": self.category,
            "timestamp": self.timestamp#.strftime("%Y-%m-%d %H:%M:%S"),
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
        print('dumping te data')
        json.dump(data, f)
    print("Dumped")


def add_expense(username: str, desc: str, amt: float, category: str, timestamp: datetime) -> str:
    print("Adiding inside ad_expsen")
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
@cross_origin()
def expenses(user_id: int):
    print("Fuk")
    if request.method == "GET":
        expenses = get_expenses(f"user{user_id}")
        return jsonify([expense.to_dict() for expense in expenses])
    elif request.method == "POST":
        print("adding useer")
        data = request.get_json()
        desc = data.get("desc", "")
        amt = data.get("amt", 0.0)
        category = data.get("category", "")
        timestamp = str(datetime.now())
        result = add_expense(f"user{user_id}", desc, amt, category, timestamp)
        print("Added")
        return jsonify({"result": result})
    else:
        print("LkAT GAYA",request.method)

@app.route("/api/users/<int:user_id>/categories/<category>", methods=["GET"])
def expenses_by_category(user_id: int, category: str):
    expenses = get_expenses_by_category(f"user{user_id}", category)
    return jsonify([expense.to_dict() for expense in expenses])

@app.route("/")
def hello():
    return "Hello"
from datetime import datetime
if __name__ == "__main__":

    add_expense("user1","Khana", 100, "food", "")

    app.run(debug=True)
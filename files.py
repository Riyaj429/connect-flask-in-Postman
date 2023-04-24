from flask import Blueprint, jsonify, request, render_template
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
import json

views = Blueprint("views", __name__)
auth = HTTPBasicAuth(scheme='USERS')

with open('data.json') as f:
    data = json.load(f)

@views.route("/")
def home():
    return jsonify(data)

# Endpoint to get data by ID
@views.route("/<int:id>", methods=["GET"])
def get_data_by_id(id):
    result = [d for d in data if d['id'] == id]
    return jsonify(result)

# Endpoint to add new data
@views.route("/", methods=["POST"])
@auth.login_required
def add_data():
    new_data = request.get_json()
    if any(d.get('id') == new_data['id'] or d.get('ID') == new_data['id'] for d in data):
        return jsonify({"message": "Data already exists"}), 409
    else:
        data.append(new_data)
        return jsonify({"message": "Data added successfully"})


# Endpoint to update data by ID
@views.route("/<int:id>", methods=["PUT"])
@auth.login_required
def update_data(id):
    for d in data:
        if d['id'] == id:
            d.update(request.get_json())
            return jsonify({"message": "Data updated successfully"})
    return jsonify({"message": "Data not found"}), 404


# Endpoint to delete data by ID
@views.route("/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_data(id):
    global data
    data = [d for d in data if d['id'] != id]
    return jsonify({"message": "Data deleted successfully"})
    

# Token authentication function
@auth.verify_password
def verify_password(username, password):
    # dictionary of valid usernames and passwords
    USERS = {
        "Riyaz": "12345678",
        "Zudeen": "87654321"
    }
    if username in USERS and password == USERS[username]:
        return username
    return None


def create_app():
    from flask import Flask

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"

    app.register_blueprint(views, url_prefix="/")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

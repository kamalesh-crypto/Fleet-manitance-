from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = "change-this-to-a-secure-random-secret"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    return jsonify({
        "message": "Demo login successful",
        "username": username
    })


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


if __name__ == "__main__":
    app.run(debug=True)

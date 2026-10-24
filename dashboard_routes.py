import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)
DATABASE = "fleetpulse.db"


@app.route("/dashboard", methods=["GET"])
def dashboard():
    conn = sqlite3.connect(DATABASE)

    total_vehicles = conn.execute(
        "SELECT COUNT(*) FROM vehicles"
    ).fetchone()[0]

    total_services = conn.execute(
        "SELECT COUNT(*) FROM maintenance"
    ).fetchone()[0]

    total_cost = conn.execute(
        "SELECT COALESCE(SUM(cost), 0) FROM maintenance"
    ).fetchone()[0]

    conn.close()

    return jsonify({
        "total_vehicles": total_vehicles,
        "total_services": total_services,
        "total_maintenance_cost": total_cost
    })


if __name__ == "__main__":
    app.run(debug=True)

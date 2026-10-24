from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = "fleetpulse.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return jsonify({
        "project": "FleetPulse",
        "description": "Advanced Fleet Maintenance System",
        "status": "Running"
    })


if __name__ == "__main__":
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            vehicle_type TEXT NOT NULL,
            registration TEXT UNIQUE NOT NULL,
            mileage INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

    app.run(debug=True)

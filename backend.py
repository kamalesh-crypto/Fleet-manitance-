from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "fleetpulse_backend.db"


def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = connect_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_name TEXT NOT NULL,
            vehicle_number TEXT NOT NULL UNIQUE,
            vehicle_type TEXT NOT NULL,
            status TEXT DEFAULT 'Active'
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return jsonify({
        "message": "FleetPulse Backend API is running"
    })


@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    conn = connect_db()
    vehicles = conn.execute(
        "SELECT * FROM vehicles"
    ).fetchall()
    conn.close()

    return jsonify([dict(vehicle) for vehicle in vehicles])


@app.route("/vehicles", methods=["POST"])
def add_vehicle():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    required_fields = [
        "vehicle_name",
        "vehicle_number",
        "vehicle_type"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    conn = connect_db()

    try:
        conn.execute("""
            INSERT INTO vehicles
            (vehicle_name, vehicle_number, vehicle_type, status)
            VALUES (?, ?, ?, ?)
        """, (
            data["vehicle_name"],
            data["vehicle_number"],
            data["vehicle_type"],
            data.get("status", "Active")
        ))

        conn.commit()
        return jsonify({"message": "Vehicle added successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Vehicle number already exists"
        }), 409

    finally:
        conn.close()


@app.route("/vehicles/<int:vehicle_id>", methods=["PUT"])
def update_vehicle(vehicle_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    conn = connect_db()

    vehicle = conn.execute(
        "SELECT * FROM vehicles WHERE id = ?",
        (vehicle_id,)
    ).fetchone()

    if vehicle is None:
        conn.close()
        return jsonify({"error": "Vehicle not found"}), 404

    vehicle_name = data.get("vehicle_name", vehicle["vehicle_name"])
    vehicle_number = data.get("vehicle_number", vehicle["vehicle_number"])
    vehicle_type = data.get("vehicle_type", vehicle["vehicle_type"])
    status = data.get("status", vehicle["status"])

    try:
        conn.execute("""
            UPDATE vehicles
            SET vehicle_name = ?,
                vehicle_number = ?,
                vehicle_type = ?,
                status = ?
            WHERE id = ?
        """, (
            vehicle_name,
            vehicle_number,
            vehicle_type,
            status,
            vehicle_id
        ))

        conn.commit()
        return jsonify({"message": "Vehicle updated successfully"})

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Vehicle number already exists"
        }), 409

    finally:
        conn.close()


@app.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    conn = connect_db()

    cursor = conn.execute(
        "DELETE FROM vehicles WHERE id = ?",
        (vehicle_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify({"message": "Vehicle deleted successfully"})


if __name__ == "__main__":
    create_table()
    app.run(debug=True)

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = "fleetpulse.db"


@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("SELECT * FROM vehicles").fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route("/vehicles", methods=["POST"])
def add_vehicle():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    vehicle_type = data.get("vehicle_type")
    registration = data.get("registration")

    if not name or not vehicle_type or not registration:
        return jsonify({"error": "Required fields are missing"}), 400

    try:
        conn = sqlite3.connect(DATABASE)

        conn.execute("""
            INSERT INTO vehicles
            (name, vehicle_type, registration, mileage)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            vehicle_type,
            registration,
            data.get("mileage", 0)
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Vehicle added successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Registration already exists"}), 409


@app.route("/vehicles/<int:vehicle_id>", methods=["PUT"])
def update_vehicle(vehicle_id):
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    mileage = data.get("mileage")

    conn = sqlite3.connect(DATABASE)

    cursor = conn.execute("""
        UPDATE vehicles
        SET name = COALESCE(?, name),
            mileage = COALESCE(?, mileage)
        WHERE id = ?
    """, (name, mileage, vehicle_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated == 0:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify({"message": "Vehicle updated successfully"})


@app.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    conn = sqlite3.connect(DATABASE)

    cursor = conn.execute(
        "DELETE FROM vehicles WHERE id = ?",
        (vehicle_id,)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify({"message": "Vehicle deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)

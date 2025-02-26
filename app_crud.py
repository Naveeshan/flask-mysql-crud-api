from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Configure MySQL Connection
db = pymysql.connect(
    host="localhost",
    user="DB_USER",  # Replace with your MySQL username
    password="DB_PASS",  # Replace with your MySQL password
    database="crud_db"  # Replace with your MySQL database name
)

cursor = db.cursor()

# CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL
)
""")
db.commit()

# CREATE
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data['name']
    price = data['price']
    cursor.execute("INSERT INTO items (name, price) VALUES (%s, %s)", (name, price))
    db.commit()
    return jsonify({"message": "Item created successfully", "id": cursor.lastrowid}), 201

# READ ALL
@app.route('/items', methods=['GET'])
def get_items(): 
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    results = [{"id": item[0], "name": item[1], "price": item[2]} for item in items]
    return jsonify({"items": results}), 200

# READ SINGLE
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if item:
        result = {"id": item[0], "name": item[1], "price": item[2]}
        return jsonify(result), 200
    return jsonify({"message": "Item not found"}), 404

# UPDATE
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    name = data['name']
    price = data['price']
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    if cursor.fetchone():
        cursor.execute("UPDATE items SET name = %s, price = %s WHERE id = %s", (name, price, item_id))
        db.commit()
        return jsonify({"message": "Item updated successfully"}), 200
    return jsonify({"message": "Item not found"}), 404
 
# DELETE
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        db.commit()
        return jsonify({"message": "Item deleted successfully"}), 200
    return jsonify({"message": "Item not found"}), 404  

if __name__ == "__main__":
    app.run(debug=True)
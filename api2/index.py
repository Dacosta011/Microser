from mysql import connector
from mysql.connector import Error
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def conection():
    try:
        con = connector.connect(
            host = "localhost",
            user = "root",
            passwd = "root",
            database = "Paises"
        )
        if con.is_connected():
            print("Conectado a la base de datos")
            return con
    except Error as e:
        print(e)

def desconection(con):
    con.close()

@app.route('/api1', methods=['GET'])
def all():
    con = conection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Pais")
    data = cursor.fetchall()
    result = []
    for i in data:
        result.append({"id": i[0], "nombre": i[1], "continente": i[2]})
    desconection(con)
    return jsonify(result)

@app.route('/api1/<id>', methods=['GET'])
def one(id):
    con = conection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Pais WHERE id = %s", (id,))
    data = cursor.fetchone()
    result = {"id": data[0], "nombre": data[1], "continente": data[2]}
    desconection(con)
    return jsonify(result)

@app.route('/api1', methods=['POST'])
def create():
    con = conection()
    cursor = con.cursor()
    data = request.get_json()
    cursor.execute("INSERT INTO Pais (id,nombre, continente) VALUES (%s,%s,%s)", (data["id"], data["nombre"], data["continente"]))
    con.commit()
    desconection(con)
    return jsonify({"message": "País creado"})

@app.route('/api1/<id>', methods=['PUT'])
def update(id):
    con = conection()
    cursor = con.cursor()
    data = request.get_json()
    cursor.execute("UPDATE Pais SET nombre = %s, continente = %s WHERE id = %s", (data["nombre"], data["continente"], id))
    con.commit()
    desconection(con)
    return jsonify({"message": "País actualizado"})

@app.route('/api1/<id>', methods=['DELETE'])
def delete(id):
    try:
        con = conection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM Pais WHERE id = %s", [id])
        con.commit()
        desconection(con)
        return jsonify({"message": "País eliminado"})
    except(Exception) as e:
        return jsonify({"message": "No se puede eliminar"})
        print(e)


if __name__ == '__main__':
    app.run(host='localhost', port=5000 , debug=True)

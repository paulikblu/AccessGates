from flask import Flask, request, jsonify
import mysql.connector 
from users import User

app = Flask(__name__)

connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()

@app.route('/inregistrare', methods=['POST'])
def inregistrare_utilizator():
    data = request.get_json()
    nume = data['nume']
    prenume = data['prenume']
    companie = data['companie']
    id_manager = data['id_manager']
    user=User(nume,prenume,companie,id_manager)
    user.get_user()
    connect.commit()
    return "Utilizator înregistrat cu succes!"

if __name__ == '__main__':
    app.run(debug=True)
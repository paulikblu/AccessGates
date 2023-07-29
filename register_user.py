import mysql.connector
from flask import Flask, render_template,request
app = Flask(__name__)

connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()


@app.route('/user',methods=["POST"])
def get_user():
    data=request.get_json()
    nume=data['nume']
    prenume=data['prenume']
    companie=data['companie']
    idManager=data['idManager']
    querry=f"INSERT INTO users values(null,'{nume}','{prenume}','{companie}','{idManager}')"
    print(querry)
    cursor.execute(querry)
    connect.commit()
    return "Datele au fost inserate"

if __name__ == '__main__':
    app.run(debug=True)
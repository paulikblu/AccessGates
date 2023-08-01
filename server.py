import mysql.connector
from flask import Flask, render_template,request,redirect,url_for
from users import User
app = Flask(__name__)
number = "7"

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

@app.route('/',methods=["GET","POST"])
def get_user():
    if request.method=="POST":
        nume = request.form["nume"]
        prenume = request.form["prenume"]
        companie = request.form["companie"]
        id_manager = request.form["id_manager"]
        cursor.execute(f"INSERT INTO USERS VALUES (null,'{nume}','{prenume}','{companie}','{id_manager}')")
        connect.commit()
        return redirect(url_for('success'))

    return render_template('form.html')

@app.route('/success')
def success():
    return f"Angajatul a fost înregistrat!"

@app.route('/person',methods=["POST"])
def getPerson():
    datas=request.get_json()
    data=datas['data']
    sens=datas['sens']
    idPersoana=datas['idPersoana']
    idPoarta=datas['idPoarta']
    querry=f"INSERT INTO gate3 values(null,'{data}','{sens}','{idPersoana}','{idPoarta}')"
    print(querry)
    cursor.execute(querry)
    connect.commit()
    return "Datele au fost inserate"

if __name__ == '__main__':
    app.run(debug=True)
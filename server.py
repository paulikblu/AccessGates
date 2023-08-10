import mysql.connector
from flask import Flask, render_template,request,redirect,url_for
from users import User
app = Flask(__name__)
number = "7"

# Establish a connection to the MySQL database
connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()

# Route for user registration
@app.route('/inregistrare', methods=['GET','POST'])
def inregistrare_utilizator():
    """
    Handle user registration request.

    Expects JSON data with user information:
    {
        "nume": "example_nume",
        "prenume": "example_prenume",
        "companie": "example_company",
        "idManager": "a number"
    }
    """
    data = request.get_json()
    nume = data['nume']
    prenume = data['prenume']
    companie = data['companie']
    idManager = data['idManager']
    user=User(nume,prenume,companie,idManager)
    user.get_user()
    connect.commit()
    return "Utilizator înregistrat cu succes!"

# Route for user registration form
@app.route('/',methods=["GET","POST"])
def get_user():
    """
    Render a user registration form and handle form submission.
    """
    if request.method=="POST":
        nume = request.form["nume"]
        prenume = request.form["prenume"]
        companie = request.form["companie"]
        id_manager = request.form["id_manager"]
        cursor.execute(f"INSERT INTO USERS VALUES (null,'{nume}','{prenume}','{companie}','{id_manager}')")
        connect.commit()
        return redirect(url_for('success'))

    return render_template('form.html')

# Route for success page after user registration
@app.route('/success')
def success():
    """
    Display a success message after user registration.
    """
    return f"Angajatul a fost înregistrat!"

# Route for registrating access data from gate entries
@app.route('/person',methods=["POST"])
def getPerson():
    """
    Capture and insert access data from gate entries.
    
    Expects JSON data with access information:
    {
        "data": "YYYY-MM-DD",
        "sens": "in/out",
        "idPersoana": "numbers",
        "idPoarta": "number"
    }
    """
    datas=request.get_json()
    data=datas['data']
    sens=datas['sens']
    idPersoana=datas['idPersoana']
    idPoarta=datas['idPoarta']
    data=data.strip("Z")
    data=data.split("T")
    ziua=data[0]
    ora=data[1]

    # Insert access data into the database
    querry=f"INSERT INTO acces_point values('{idPersoana}','{idPoarta}','{ziua}','{ora}','{sens}')"
    print(querry)
    cursor.execute(querry)
    connect.commit()
    return "Datele au fost inserate"

if __name__ == '__main__':
    app.run(debug=True)
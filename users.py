import mysql.connector
import requests

connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()

class User():
    def __init__(self, nume, prenume, companie, IdManager):
            self.nume=nume
            self.prenume=prenume
            self.companie=companie
            self.IdManager=IdManager
    def get_user(self):
            query = f"INSERT INTO users VALUES (null, '{self.nume}', '{self.prenume}', '{self.companie}', '{self.IdManager}')" 
            cursor.execute(query)
            connect.commit()
            return 'User registered successfully!'



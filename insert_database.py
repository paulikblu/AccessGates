import mysql.connector
from files import Fisier,Csv,Txt

connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()

def citire_txt():
    fisier=Txt("Poarta1.txt")
    fisier.citire_fisier()
    # id=file[0]
    # time=file[1]
    # way=file[2].strip(";")
    # query=f"INSERT INTO ACCES_POINT values('{id}','{time}','{way}')"
    # cursor.execute(query)
    # connect.commit()
    # print(query)
citire_txt()

# def insert_txt():
#     file=citire_txt()
#     print(file)


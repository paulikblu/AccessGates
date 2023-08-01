import shutil
import csv
import os
from datetime import datetime, date
import mysql.connector

connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()

intrari='intrari/'
backup='backup_intrari/'

class Fisier():
    def __init__(self,numeFisier):
        self.numeFisier = numeFisier
    def citire_fisier(self):
        pass
    def muta_fisier(self):
        pass
    
class Txt(Fisier):
    timp=date.today()
    def __init__(self,numeFisier):
        super().__init__(numeFisier)
    def citire_fisier(self):
        try:
            with open(intrari+self.numeFisier,"r") as file:
                reader=file.readlines()
                for line in reader:
                    line=line.strip().split(",")
                    id=int(line[0])
                    time=line[1]
                    time=time.strip("Z")
                    time=time.split("T")
                    data=time[0]
                    ora=time[1]
                    way=line[2].strip(";")
                    query=f"INSERT INTO ACCES_POINT values('{id}','1','{data}','{ora}','{way}')"
                    cursor.execute(query)
                    connect.commit()
                    print(query)
        except FileNotFoundError:
            print("No new registers found at Gate 1")
    def muta_fisier(self):
        sursa=os.path.join(intrari,self.numeFisier)
        newfile=f"backupPoarta1 - {self.timp}.txt"
        destinatia=os.path.join(backup,newfile)
        shutil.move(sursa,destinatia)

# fisier=Txt("Poarta1.txt")
# fisier.citire_fisier()
        
class Csv(Fisier):
    timp=date.today()
    def __init__(self,numeFisier):
        super().__init__(numeFisier)
    def citire_fisier(self):
        try:
            with open(intrari+self.numeFisier,"r") as file:
                heading=next(file)
                reader=csv.reader(file)
                for row in reader:
                    id=row[0]
                    time=row[1]
                    time=time.strip("Z")
                    time=time.split("T")
                    data=time[0]
                    ora=time[1]
                    way=row[2]
                    query=f"INSERT INTO ACCES_POINT values('{id}','2','{data}','{ora}','{way}')"
                    cursor.execute(query)
                    connect.commit()
                    print(query)
        except FileNotFoundError:
            print("No new registers found at Gate 2")
    def muta_fisier(self):
        sursa=os.path.join(intrari,self.numeFisier)
        newfile=f"backupPoarta2 - {self.timp}.csv"
        destinatia=os.path.join(backup,newfile)
        shutil.move(sursa,destinatia)

# fisier=Csv("Poarta2.csv")
# fisier.citire_fisier()

def checkingNewFileS():
    new_files=[]
    files=os.listdir(intrari)
    if len(new_files) != len(files):
        for file in files:
            if file[-1]=="t":
                fisier=Txt(file)
                fisier.muta_fisier()
            if file[-1]=="v":
                fisier=Csv(file)
                fisier.muta_fisier()
    else:
        print("No new files")
    new_files=files

# checkingNewFileS()
            







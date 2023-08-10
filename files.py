import shutil
import csv
import os
from datetime import datetime, date
import mysql.connector

# Establish a connection to the MySQL database
connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()

intrari='intrari/'
backup='backup_intrari/'

# Defining the base class for files manipulation
class Fisier():
    """
    The base class for files manipulation.
    """
    def __init__(self,numeFisier):
        """
        Initiates a Fisier object with the given name of the file.

        Args:
            numeFisier (str): The name of the file.
        """
        self.numeFisier = numeFisier
    def citire_fisier(self):
        """
        Abstract method for reading the content of the file.

        """
        pass
    def muta_fisier(self):
        """
        Abstract method for moving the file in the backup folder.
        
        """
        pass

# Defining the class for the TXT files   
class Txt(Fisier):
    """
    The class for reading TXT files.
    """
    timp=date.today()
    def __init__(self,numeFisier):
        """
        Initiates a Txt object with the given name of the file.
        
        Args:
            numeFisier (str): The name of the file.
        """
        super().__init__(numeFisier)
    def citire_fisier(self):
        """
        Reads the content of the TXT file and inserts the extracted data into the database.
        
        """
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
        """
        Moves the TXT file in the backup folder.
        
        """
        sursa=os.path.join(intrari,self.numeFisier)
        newfile=f"backupPoarta1 - {self.timp}.txt"
        destinatia=os.path.join(backup,newfile)
        shutil.move(sursa,destinatia)

# Defining the class for CSV files.
class Csv(Fisier):
    """
    The class for reading CSV files.
   
    """
    timp=date.today()
    def __init__(self,numeFisier):
        """
        Initiates a Csv object with the given name of the file.
        
        Args:
            numeFisier (str): The name of the file.
        """
        super().__init__(numeFisier)
    def citire_fisier(self):
        """
        Reads the content of the CSV file and inserts the extracted data into the database.
        """
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
        """
        Moves the CSV file in the backup folder.
        """
        sursa=os.path.join(intrari,self.numeFisier)
        newfile=f"backupPoarta2 - {self.timp}.csv"
        destinatia=os.path.join(backup,newfile)
        shutil.move(sursa,destinatia)


# Function for checking and moving new files 
def checkingNewFileS():
    """
    Checks if there are new files in the initial folder and moves them in the backup folder.
    
    """
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


            







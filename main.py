import datetime
import csv
import mysql.connector
import shutil
import os
import requests
import json
import schedule
import move
import subprocess
import threading
from files import Fisier,Txt,Csv,checkingNewFileS
import time
from checkinghours import checking_hours

connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()

intrari="intrari"
backup="backup_intrari"

def main():
    while True:
        poarta1=Txt("Poarta1.txt")
        poarta2=Csv("Poarta2.csv")
        poarta1.citire_fisier()
        poarta2.citire_fisier()
        checkingNewFileS()
        time.sleep(5)
        schedule.every().day.at("20:00").do(checking_hours)
        schedule.run_pending()

main()

# def server():
#     subprocess.run(["python","server.py"],check=True)

# t1 = threading.Thread(target=main)
# t2 = threading.Thread(target=server)

# t1.start()
# t2.start()

# t1.join()
# t2.join()






from datetime import datetime, date
import mysql.connector
from email.message import EmailMessage
import ssl
import smtplib


connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()


def sending_email(text):
    email_sender = 'paulmuntean.blu@gmail.com'
    email_password = 'mtxyauztfvawowoe'
    email_receiver = 'paul.muntean93@gmail.com'
    subject = "Avertisment angajat!"
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(text)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def difference_time(start, end):

    start_time = datetime.strptime(start, "%H:%M:%S")
    end_time = datetime.strptime(end, "%H:%M:%S")
    delta = end_time - start_time
    sec = delta.total_seconds()
    hours = sec / (60 * 60)
    return int(hours)

def checking_hours():
    data = date.today()
    employees = {}
    cursor.execute(f"SELECT * FROM ACCES_POINT WHERE Data='{str(data)}'")
    # cursor.execute(f"SELECT * FROM ACCES_POINT")
    angajati = cursor.fetchall()
    for angajat in angajati:
        idAngajat = angajat[0]
        ore_lucrate = angajat[3]
        way = angajat[4]
        if idAngajat not in employees:
            employees[idAngajat] = {"intrare": [], "iesire": []}
        if way == 'in':
            employees[idAngajat]['intrare'].append(ore_lucrate[:8])
        elif way == 'out':
            employees[idAngajat]['iesire'].append(ore_lucrate[:8])
            
    numar_ore = []
    for idAngajat, time_dict in employees.items():
        intrari = time_dict['intrare']
        iesiri = time_dict['iesire']
        total_ore_lucrate = 0
        
        # Calculate total working hours for each entry-exit pair
        for intrare, iesire in zip(intrari, iesiri):
            ore_lucrate = difference_time(intrare, iesire)
            total_ore_lucrate += ore_lucrate
        
        angajat_data = {"IDangajat": idAngajat, "nrOreLucrate": total_ore_lucrate}
        numar_ore.append(angajat_data)
        
    numar_ore_sub = []
    for element in numar_ore:
        if element["nrOreLucrate"] < 8:
            numar_ore_sub.append(element)
            
    if len(numar_ore_sub) > 0:
        text = ""
        for el in numar_ore_sub:
            idan = el['IDangajat']
            ore = el['nrOreLucrate']
            text += f"Atenție! Angajatul cu ID-ul {idan} a lucrat {ore} ore în data de {data}\n"
    else:
        text = f"Toți angajații au lucrat cel puțin 8 ore în data de {data}\n"
        
    print(text)
    sending_email(text)   
    
       
checking_hours()



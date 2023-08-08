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

# Funcția pentru trimiterea de emailuri
def sending_email(text):
    """
    Sends an email with the specified text content.

    Args:
        text (str): The content of the email.

    Returns:
        None
    """
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

# Funcția pentru calcularea diferenței de timp în ore
def difference_time(start, end):
    """
    Calculates the time difference between two time values.

    Args:
        start (str): The start time in the format HH:MM:SS.
        end (str): The end time in the format HH:MM:SS.

    Returns:
        int: The time difference in hours.
    """

    start_time = datetime.strptime(start, "%H:%M:%S")
    end_time = datetime.strptime(end, "%H:%M:%S")
    delta = end_time - start_time
    sec = delta.total_seconds()
    hours = sec / (60 * 60)
    return int(hours)

# Funcția pentru verificarea orelor lucrate ale angajaților și trimiterea unui mail managerului
def checking_hours():
    """
    Checks the hours worked by employees and sends warnings via email.

    Retrieves data from the database for the current date, calculates the hours worked by each employee,
    and sends an email if an employee worked less than 8 hours.

    Returns:
        None
    """
    data = date.today()
    employees = {}
     # Interogarea bazei de date pentru a obține înregistrările pentru data curentă
    cursor.execute(f"SELECT * FROM ACCES_POINT WHERE Data='{str(data)}'")

    # Parcurgerea fiecărei înregistrări și procesarea datelor
    angajati = cursor.fetchall()
    for angajat in angajati:
        idAngajat = angajat[0]
        ore_lucrate = angajat[3]
        way = angajat[4]

        # Adăugarea înregistrărilor în dicționarul employees
        if idAngajat not in employees:
            employees[idAngajat] = {"intrare": [], "iesire": []}
        if way == 'in':
            employees[idAngajat]['intrare'].append(ore_lucrate[:8])
        elif way == 'out':
            employees[idAngajat]['iesire'].append(ore_lucrate[:8])

    # Calcularea totalului orelor lucrate de fiecare angajat și adăugarea lor într-o listă        
    numar_ore = []
    for idAngajat, time_dict in employees.items():
        intrari = time_dict['intrare']
        iesiri = time_dict['iesire']
        total_ore_lucrate = 0
        for intrare, iesire in zip(intrari, iesiri):
            ore_lucrate = difference_time(intrare, iesire)
            total_ore_lucrate += ore_lucrate
        
        angajat_data = {"IDangajat": idAngajat, "nrOreLucrate": total_ore_lucrate}
        numar_ore.append(angajat_data)

    # Creearea unei liste cu angajații care au lucrat mai puțin de 8 ore și trimiterea emailului la manager    
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
    
       
# checking_hours()



import requests
import mysql.connector
import random
import datetime,time,csv,os
import colorlog,logging
import shutil

#verificare insert user in baza de date
def test_1(id_manager, URL, cale, nume_tabel):
    users = [
        ["Badea", "Mihai", "IT Shool", id_manager],
        ["Muntean", "Paul", "IT School", id_manager],
        ["Olteanu", "Leontin", "IT School", id_manager],
        ["Angiu", "Natalia", "Google", id_manager]
    ]
    for user in users:
        jsonData = {
            "nume": user[0],
            "prenume": user[1],
            "companie": user[2],
            "idManager": id_manager
        }
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.post(URL + cale, json=jsonData, headers=headers)
        print(r.status_code)

    connect = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
    cursor = connect.cursor()

    cursor.execute(f"SELECT * from {nume_tabel}")
    results = cursor.fetchall()

    for row in users:
        found = False
        contor = 0
        while not found and contor < len(results):
            flag = True
            for i in range(len(row)):
                if row[i] != results[contor][i + 1]:
                    flag = False
            if flag:
                found = True
            else:
                contor += 1
        if not found:
            return "Test 1 failed..."
    
    return "Test 1 passed.."

    cursor.close()
    connect.close()

# test_1("1","http://127.0.0.1:5000","/inregistrare","users")

#verificare intrare fisiere csv si txt
def test_2(cale,type):
    persoane=[]
    linii=[]
    
    for i in range(6):
        alegere=random.randint(0,1)
        output={
                "data":datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
                "idPoarta":random.randint(1,3)
            }
        aIntrat=False
        if(alegere==1):
            #intrare
            idPersoana=random.randint(1,5)
            while(idPersoana in persoane):
                idPersoana=random.randint(1,5)
            output["sens"]="in"
            output["idPersoana"]=idPersoana
            persoane.append(output['idPersoana'])
            aIntrat=True
        else:
            #iesire 
            if(len(persoane)>0):
                idPersoana=persoane[random.randint(0,len(persoane)-1)]
                output["sens"]="out"
                output["idPersoana"]=idPersoana
                persoane.remove(idPersoana)
                aIntrat=True
        if(aIntrat):
            linii.append(output)

        if type=="csv":
            with open(cale,"w",newline="") as file:
                writer=csv.writer(file)
                header="IdPersoana","Data","Sens"
                writer.writerow(header)
                for line in linii:
                    array=[str(line["idPersoana"]),line["data"],line["sens"]]
                    writer.writerow(array)
        else:
            with open(cale,"w")as file:
                for line in linii:
                    array=f"{line['idPersoana']},{line['data']},{line['sens']};\n"
                    file.write(array)
    final_path=r"C:/Users/Paul/Desktop/curs Python/ProiectFinal/intrari"
    shutil.move(cale,final_path)
    return final_path


# test_2("Poarta2.csv","csv")

import datetime

def test_3(fisier_input):
    initial_path = os.listdir(r"C:/Users/Paul/Desktop/curs Python/ProiectFinal/intrari")
    backup_path = os.listdir(r"C:/Users/Paul/Desktop/curs Python/ProiectFinal/backup_intrari")
    extension=fisier_input.split(".")[1]
    filename=fisier_input.split(".")[0]
    flag = False

    for file in initial_path:
        if file == fisier_input:
            flag = True

    for file in backup_path:
        if file == filename + "-" + str(datetime.datetime.now().date()) + "."+extension:
            flag = True

    return flag

# test_3("Poarta1.txt")

    
# verificare ca nu exista fisiere mai vechi de 5 secunde in directorul de intrari
def test_4(path): 
    createdTime=os.path.getatime(path)
    current_time=time.time()
    flag=True

    for file in os.listdir(path):
        if createdTime<= current_time-5:
            flag=False
            print("Test 4 failed...")
        else:
            print("Test 4 passed...")
    return flag

# test_4(r"C:/Users/Paul/Desktop/curs Python/ProiectFinal/intrari")

 # Define the log format with colors
log_format = (
    '%(log_color)s%(levelname)s%(reset)s '
    '%(log_color)s%(asctime)s%(reset)s '
    '%(log_color)s%(message)s%(reset)s'
)

# Create a logger
logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)  # Set the desired log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Create a stream handler to output logs to the console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(colorlog.ColoredFormatter(log_format))
logger.addHandler(stream_handler)


def check():
    punctaj=0
    if test_1("1","http://127.0.0.1:5000","/inregistrare","users"):
        punctaj+=2.5
        logging.info("Test 1 passed...")
    else:
        logging.error("Test 1 failed...")
    if test_2("Poarta1.txt","txt"):
        punctaj+=2.5
        logging.info("Test 2 passed...")
    else:
        logging.error("Test 2 failed...")
    if test_3("Poarta1.txt"):
        punctaj+=2.5
        logging.info("Test 3 passed...")
    else:
        logging.error("Test 3 failed...")
    if test_4(r"C:/Users/Paul/Desktop/curs Python/ProiectFinal/intrari"):
        punctaj+=2.5
        logging.info("Test 4 passed...")
    else:
        logging.error("Test 4 failed...")


    if punctaj <=5:
        logging.error("Punctajul este"+str(punctaj))
    if punctaj > 5 and punctaj <=7.5:
        logging.warning("Punctajul este"+ str(punctaj))
    if punctaj >7.5:
        logging.info("Punctajul este"+ str(punctaj))

check()
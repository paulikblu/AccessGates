import mysql.connector

# Establish a connection to the MySQL database
connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pri.Pri.69",
        database="proiectf"
    )
cursor=connect.cursor()

class User():
    """
    Class to represent a user and interact with the database for user registration.
    """
    def __init__(self, nume, prenume, companie, IdManager):
            """
        Initialize a User object with provided information.
        
        Args:
            nume (str): User's last name.
            prenume (str): User's first name.
            companie (str): User's company.
            IdManager (str): User's manager's ID.
        """
            self.nume=nume
            self.prenume=prenume
            self.companie=companie
            self.IdManager=IdManager
    def get_user(self):
            """
        Insert user information into the database.
        
        Returns:
            str: Message indicating successful user registration.
        """
            query = f"INSERT INTO users VALUES (null, '{self.nume}', '{self.prenume}', '{self.companie}', '{self.IdManager}')" 
            cursor.execute(query)
            connect.commit()
            return 'User registered successfully!'



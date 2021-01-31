"""
A flask app that lists various charities and social services in Portland.
data is stored in a SQLite database that looks something like the following:

+------------+------------------+------------+----------------+
| Name       | Email            | signed_on  | message        |
+============+==================+============+----------------+
| John Doe   | jdoe@example.com | 2012-05-28 | Hello world    |
+------------+------------------+------------+----------------+

This can be created with the following SQL (see bottom of this file):

    create table infobook (name text, description text, streetAddress text, typesOfService text, phoneNumber number, 
    hoursOfOperation text, reviews text);

"""
from datetime import date
from .Model import Model
import sqlite3
DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from infobook")
        except sqlite3.OperationalError:
            cursor.execute("create table infobook (name text, email text, signed_on date, message)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: name, description, streetAddress, typesOfServices, phoneNumber, hoursOfOperation, reviews, email =
        :return: List of lists containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM infobook")
        return cursor.fetchall()

    def insert(self, name, description, streetAdress, typesOfService, phoneNumber, hoursOfOperation, reviews):
        """
        Inserts entry into database
        :param name: String
        :param description: String
        :param streetAdress: String
        :param typesOfService: String
        :param phoneNumber: String
        :param hoursOfOperation: String
        :param reviews: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'name':name, 'description':description, 'streetAdress':streetAdress, 'typesOfServices':typesOfService, 
                'phoneNumber':phoneNumber, 'hoursOfOperation':hoursOfOperation, 'reviews':reviews}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into socialbook (name, description, streetAdress, typesOfService, phoneNumber, hoursOfOperation, reviews, email) \
        VALUES (:name, :description, :streetAdress, :typesOfService, :phoneNumber, :hoursOfOperation, :reviews)", params)

        connection.commit()
        cursor.close()
        return True



"""
Python list model
"""
from datetime import date
from .Model import Model

class model(Model):
    def __init__(self):
        self.infoentries = []

    def select(self):
        """
        Returns infoentries list of lists
        Each list in infoentries contains: name, description, streetAddress, typesOfServices, phoneNumber, hoursOfOperation, reviews
        :return: List of lists
        """
        return self.socialentries

    def insert(self, name, description, streetAdress, typesOfService, phoneNumber, hoursOfOperation, reviews):
        """
        Appends a new list of values representing new message into socialentries
        :param name: String
        :param description: String
        :param streetAdress: String
        :param typesOfService: String
        :param phoneNumber: String
        :param hoursOfOperation: String
        :param reviews: String
        :return: True
        """
        params = [name, description, streetAdress, typesOfService, phoneNumber, hoursOfOperation, reviews]
        self.infoentries.append(params)
        return True

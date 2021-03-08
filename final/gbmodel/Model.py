class Model():
    def select(self):
        """
        Gets all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

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
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass

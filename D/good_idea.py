from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        print("saving data to MySQL database...")

class PostgresDatabase(Database):
    def save(self, data):
        print("saving data to Postgres database...")

class App:
    def __init__(self, database: Database):
        self.database = database
    def save_data(self, data):
        self.databade.save(data)

    

import psycopg2
import os

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=os.environ['DATABASE_NAME'],
            host=os.environ['DATABASE_HOST'],
            user=os.environ['DATABASE_USER'],
            password=os.environ['DATABASE_PASSWORD'],
            port=os.environ['DATABASE_PORT']
        )
        self.cursor = self.conn.cursor()

    def sendQuery(self, query:str, params = None):
        self.cursor.execute(query, params)

    def commit(self):
        self.conn.commit()

    def fetchOne(self):
        return self.cursor.fetchone()
    
    def fetchAll(self):
        return self.cursor.fetchall()
    
    def fetchMany(self, size:int):
        return self.cursor.fetchmany(size=size)

    def close(self):
        self.cursor.close()
        self.conn.close()
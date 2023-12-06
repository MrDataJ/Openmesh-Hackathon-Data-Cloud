import sqlite3
from sqlite3 import Error

class DBManager:
    def __init__(self, db_file):
        """ Initialize the database manager with a database file. """
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        """ Create a database connection. """
        try:
            self.conn = sqlite3.connect(self.db_file)
            print("SQLite connection is established.")
        except Error as e:
            print(e)

    def close_connection(self):
        """ Close the database connection. """
        if self.conn:
            self.conn.close()

    def create_table(self, create_table_sql):
        """ Create a table from the create_table_sql statement. """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_data(self, table, data):
        """ Insert data into the table. """
        columns = ', '.join(data.keys())
        placeholders = ':' + ', :'.join(data.keys())
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        try:
            c = self.conn.cursor()
            c.execute(sql, data)
            self.conn.commit()
        except Error as e:
            print(e)

    def query_data(self, query):
        """ Query data from the database. """
        try:
            c = self.conn.cursor()
            c.execute(query)
            return c.fetchall()
        except Error as e:
            print(e)

# Example usage
if __name__ == "__main__":
    db_manager = DBManager("my_database.db")

    # Create a new database connection
    db_manager.create_connection()

    # Create table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS data (
        id integer PRIMARY KEY,
        content text NOT NULL
    );
    """
    db_manager.create_table(create_table_sql)

    # Insert data
    db_manager.insert_data("data", {"content": "Sample data"})

    # Query data
    all_data = db_manager.query_data("SELECT * FROM data")
    print("Data in the database:", all_data)

    # Close the connection
    db_manager.close_connection()

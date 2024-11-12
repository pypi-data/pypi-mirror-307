import mysql.connector
from mysql.connector import Error
import FeasMsgCls


class FeasDBCls:
    """Class for MySQL Database Connectivity"""

    def __init__(self, host="localhost", user="root", password="MeOnly@007", database="feas"):
        """Initialize with database connection parameters."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

        self.MsgFactory = FeasMsgCls.FeasMsgCls()



    def open_connection(self):
        """Open a connection to the MySQL database."""

        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

    def close_connection(self):
        """Close the connection to the MySQL database."""
        #if self.connection is not None and self.connection.is_connected():
        if self.connection.is_connected():

            self.connection.close()
            print("MySQL connection is closed")

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor
        # get all records
        #records = cursor.fetchall()
        """Execute a query on the MySQL database."""
        #if self.connection is None:
        #    print("No connection available. Open a connection first.")
        #    return None

        #cursor = self.connection.cursor()
        #try:
        #    mycur = cursor.execute(query)
         #   self.connection.commit()
         #   print("Query executed successfully")
         #   return mycur
        #except Error as e:
        #    print(f"Error executing query: {e}")
        #    return None

    #def fetch_all(self, query, params=None):
    def fetch_all(self, query: object) -> object:
        """Fetch all results from a SELECT query."""
        cursor = self.execute_query(query)
        print(f"Query executed successfully in fetch_all")
        if cursor:
            return cursor.fetchall()
        return None

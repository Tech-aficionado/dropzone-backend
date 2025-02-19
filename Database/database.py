from Database.databaseCredentials import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_USER
import mysql.connector
from mysql.connector import Error
import emoji

# Establish a connection
try:
    connection = mysql.connector.connect(
        host=DB_HOST,  # Database host address
        database=DB_DATABASE,  # Name of the database
        user=DB_USER,  # Your username
        password=DB_PASSWORD,  # Your password
        port=3600,
    )

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MariaDB server version 1.10.1", db_Info)
        cursor = connection.cursor()
        cursor.execute(f"USE {DB_DATABASE};")
        record = cursor.fetchone()
        print(emoji.emojize("Connected to Database \U0001F44D"))

        rows = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

        for row in rows:
            print(row)

except Error as e:
    print(emoji.emojize("Error while connecting to MySQL \U0001F621"))


class DatabaseOperation:
    def selectDB(query: str, params: str):
        try:

            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MariaDB server version 1.10.1", db_Info)
                cursor = connection.cursor(dictionary=True)
                cursor.execute(f"USE {DB_DATABASE};")
                print("Connected to database: ")

                # Sample query execution
                cursor.execute(query, params)
                rows = cursor.fetchall()

                print("Total number of rows in table: ", cursor.rowcount)

                if cursor.rowcount != 0:
                    return dict(row=cursor.rowcount, detail=rows)
                else:
                    return dict(row=cursor.rowcount, detail="")
            else:
                return
        except Error as e:
            print("Error while connecting to MySQL", e)

    def CrudOperationsDB(query: str, params: str):
        try:

            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MariaDB server version 1.10.1", db_Info)
                cursor = connection.cursor()
                cursor.execute(f"USE {DB_DATABASE};")
                print("Connected to database: ")

                # Sample query execution
                cursor.execute(query, params)
                rows = cursor.fetchall()
                print("Total number of rows in table: ", cursor.rowcount)

                return dict(row=cursor.rowcount, detail=cursor.fetchall())

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            connection.commit()

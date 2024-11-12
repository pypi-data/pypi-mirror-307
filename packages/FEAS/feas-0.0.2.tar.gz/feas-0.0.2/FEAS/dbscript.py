import mysql.connector
import os

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MeOnly@007',
    'database': 'feas'
}


# Connect to the MySQL database
def connect_to_db(config):
    return mysql.connector.connect(**config)


# Fetch all tables in the database
def fetch_tables(cursor):
    cursor.execute("SHOW TABLES")
    return [table[0] for table in cursor.fetchall()]


# Get the structure of a table
def get_table_structure(cursor, table_name):
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    return cursor.fetchone()[1]


# Get the data from a table
def get_table_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()


# Generate INSERT statements for the table data
def generate_insert_statements(cursor, table_name, data):
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [column[0] for column in cursor.fetchall()]
    insert_statements = []
    for row in data:
        values = ', '.join([f"'{str(value)}'" if value is not None else 'NULL' for value in row])
        insert_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values});")
    return insert_statements


# Create a script to recreate the database and tables
def create_script():
    connection = connect_to_db(DB_CONFIG)
    cursor = connection.cursor()

    # Start the script with database creation
    script = f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']};\nUSE {DB_CONFIG['database']};\n\n"

    # Get all tables
    tables = fetch_tables(cursor)

    # Loop through each table, get the structure and data
    for table in tables:
        # Get table structure (CREATE TABLE statement)
        table_structure = get_table_structure(cursor, table)
        script += f"{table_structure};\n\n"

        # Get table data (INSERT statements)
        table_data = get_table_data(cursor, table)
        if table_data:
            insert_statements = generate_insert_statements(cursor, table, table_data)
            script += "\n".join(insert_statements) + "\n\n"

    # Write the script to a .sql file
    script_file = "database_export_script.sql"
    with open(script_file, 'w') as f:
        f.write(script)

    print(f"Script generated and saved to {script_file}")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_script()

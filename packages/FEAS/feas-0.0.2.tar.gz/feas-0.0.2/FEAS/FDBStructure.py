import mysql.connector

# Database connection details
hostname = 'localhost'
username = 'root'
password = 'MeOnly@007'
database = 'feas'

# List of tables to describe
tables = [
    'tcmp_city', 'tcmp_country', 'tcmp_dept', 'tcmp_fcexits', 'tcmp_firedata',
    'tcmp_floor', 'tcmp_flrmsgs', 'tcmp_flrside', 'tcmp_heatdata', 'tcmp_loc',
    'tcmp_msgdb', 'tcmp_province', 'tcmp_smokedata', 'tcmp_stations',
    'tcmp_sysadmin', 'temp_level', 'temp_main', 'temp_type'
]


def get_table_description(cursor, table_name):
    cursor.execute(f"DESC {database}.{table_name}")
    columns = cursor.fetchall()
    description = []
    for column in columns:
        col_name, data_type, is_nullable, key, default, extra = column
        col_info = {
            'Column Name': col_name,
            'Data Type': data_type,
            'Is Nullable': is_nullable,
            'Key': key,
            'Default': default,
            'Extra': extra
        }
        description.append(col_info)
    return description


def generate_documentation(cursor):
    documentation = ""
    for table in tables:
        description = get_table_description(cursor, table)
        documentation += f"### Table: {table}\n\n"
        documentation += "| Column Name | Data Type | Is Nullable | Key | Default | Extra |\n"
        documentation += "|-------------|-----------|-------------|-----|---------|-------|\n"
        for col in description:
            documentation += f"| {col['Column Name']} | {col['Data Type']} | {col['Is Nullable']} | {col['Key']} | {col['Default']} | {col['Extra']} |\n"
        documentation += "\n\n"
    return documentation


# Connect to the database and generate documentation
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='MeOnly@007',
        database='feas'
    )

    cursor = connection.cursor()
    documentation = generate_documentation(cursor)

    # Save documentation to file
    with open('database_documentation.md', 'w') as f:
        f.write(documentation)

    print("Database documentation generated successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

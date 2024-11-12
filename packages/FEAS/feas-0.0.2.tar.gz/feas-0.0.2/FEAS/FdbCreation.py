import mysql.connector
from mysql.connector import Error

# Database connection details
host = "localhost"
user = "root"
password = "MeOnly@007"
database = "feas"

# SQL script for creating tables with referential integrity and inserting data
sql_script = """
CREATE DATABASE IF NOT EXISTS feas;

USE feas;

-- Creating table warehouse_layout
CREATE TABLE IF NOT EXISTS warehouse_layout (
    floor_id INT PRIMARY KEY AUTO_INCREMENT,
    floor_number INT,
    room_id INT,
    exit_point VARCHAR(255),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE
);

-- Creating table rooms
CREATE TABLE IF NOT EXISTS rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_name VARCHAR(255),
    room_type VARCHAR(255),
    floor_id INT,
    FOREIGN KEY (floor_id) REFERENCES warehouse_layout(floor_id) ON DELETE CASCADE
);

-- Creating table sensors
CREATE TABLE IF NOT EXISTS sensors (
    sensor_id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_type VARCHAR(255),
    location_id INT,
    status VARCHAR(50),
    FOREIGN KEY (location_id) REFERENCES rooms(room_id) ON DELETE CASCADE
);

-- Creating table evacuation_routes
CREATE TABLE IF NOT EXISTS evacuation_routes (
    route_id INT PRIMARY KEY AUTO_INCREMENT,
    floor_id INT,
    exit_point VARCHAR(255),
    route_description TEXT,
    FOREIGN KEY (floor_id) REFERENCES warehouse_layout(floor_id) ON DELETE CASCADE
);

-- Creating table emergency_alerts
CREATE TABLE IF NOT EXISTS emergency_alerts (
    alert_id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id INT,
    alert_time DATETIME,
    alert_type VARCHAR(255),
    severity VARCHAR(50),
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE CASCADE
);

-- Creating table evacuation_logs
CREATE TABLE IF NOT EXISTS evacuation_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    evacuation_time DATETIME,
    route_id INT,
    people_evacuated INT,
    status VARCHAR(255),
    FOREIGN KEY (route_id) REFERENCES evacuation_routes(route_id) ON DELETE CASCADE
);

-- Creating table users
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255)
);

-- Inserting some initial data
INSERT INTO rooms (room_name, room_type, floor_id) VALUES 
('Storage Room', 'Storage', 1),
('Office 101', 'Office', 1),
('Conference Room', 'Meeting', 2);

INSERT INTO warehouse_layout (floor_number, room_id, exit_point) VALUES
(1, 1, 'East Exit'),
(1, 2, 'West Exit'),
(2, 3, 'South Exit');

INSERT INTO sensors (sensor_type, location_id, status) VALUES
('Fire', 1, 'active'),
('Smoke', 2, 'active'),
('Heat', 3, 'inactive');

INSERT INTO evacuation_routes (floor_id, exit_point, route_description) VALUES
(1, 'East Exit', 'Use east exit to leave the building'),
(2, 'South Exit', 'Proceed to south exit for evacuation');

INSERT INTO emergency_alerts (sensor_id, alert_time, alert_type, severity) VALUES
(1, NOW(), 'Fire', 'High'),
(2, NOW(), 'Smoke', 'Medium');

INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'administrator'),
('operator', 'op123', 'operator');
"""

# Log file
log_file = "dbcreation.txt"

def execute_sql_script(script):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            for statement in script.split(';'):
                if statement.strip():
                    cursor.execute(statement)

            # Commit the transaction
            connection.commit()

            # Write to log file for successful execution
            with open(log_file, 'a') as log:
                log.write("***************************************\n")
                log.write("Success: Database creation completed.\n")
                log.write("***************************************\n")

    except Error as e:
        # Write error details to the log file
        with open(log_file, 'a') as log:
            log.write("***************************************\n")
            log.write(f"Error: {e}\n")
            log.write("Unsuccessful: Database creation failed.\n")
            log.write("***************************************\n")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Initialize log file and write initial message
with open(log_file, 'w') as log:
    log.write("Starting database creation...\n")

# Execute the SQL script
execute_sql_script(sql_script)

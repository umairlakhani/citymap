import csv
import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'dbname': 'map',
    'user': 'postgres',
    'password': 'Guizza@123',
    'host': 'localhost',
    'port': '5432',
}

# CSV file path
csv_file_path = 'map/data/town.csv'

# Table name in the database
table_name = 'map_address'

# Open a connection to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()
# Open and read the CSV file
with open(csv_file_path, 'r', encoding='utf-8') as file:
    # Create a CSV reader
    reader = csv.reader(file)
    
    # Skip the header if the CSV file has one
    next(reader)

    # Use the COPY command to insert data into the table
    columns = ["street","long","lat","city_id","town_id","neighborhood","postal"]
    # columns = ['nil' if not column else column for column in columns]
    cursor.copy_from(file, table_name, sep=',', columns=columns)

# Commit changes and close the connection
conn.commit()
conn.close()

print(f'Data from {csv_file_path} inserted into {table_name} table.')

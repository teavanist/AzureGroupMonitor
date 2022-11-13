import psycopg2
import os 

def get_db(file):
    with open(path_to_yaml_file, 'r') as file:
        configuration = yaml.safe_load(file)

    host = configuration["DB_HOST"]
    database = configuration["DB_NAME"]
    user = configuration["DB_USER"]
    password = configuration["DB_PASS"]

    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    return conn



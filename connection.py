import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
PGDATABASE = os.getenv('PGDATABASE')
PGHOST = os.getenv('PGHOST')
PGPASSWORD = os.getenv('PGPASSWORD')
PGPORT = os.getenv('PGPORT')
PGUSER = os.getenv('PGUSER')

def get_connection():
    try:
        conn = psycopg2.connect(host = PGHOST, database = PGDATABASE, user = PGUSER, password = PGPASSWORD, port = PGPORT)
        return conn
    except:
        print("Falló la conexión a la base de datos.")
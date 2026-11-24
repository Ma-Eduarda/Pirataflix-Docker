import os
import psycopg

def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME", "dbPirataFlix"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
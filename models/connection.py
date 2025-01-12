from decouple import config
import pymysql
from pymysql.cursors import DictCursor

DB_CONFIG = {
    'host': config('DB_HOST'),
    'user': config('DB_USER'),
    'password': config('DB_PASSWORD'),
    'database': config('DB_NAME'),
    'cursorclass': DictCursor
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)
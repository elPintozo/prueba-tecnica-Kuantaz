import psycopg2
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_database_uri():
    db_name = "kuantaz_db"
    db_user = "postgres"
    db_password = "postgres"
    db_host = "localhost"
    db_port = "5432"  # puerto por defecto de PostgreSQL

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def get_database_uri_test():
    db_name = "kuantaz_db"
    db_user = "postgres"
    db_password = "postgres"
    db_host = "localhost"
    db_port = "5432"  # puerto por defecto de PostgreSQL

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?options=-c%20search_path=test"

def get_db_conn():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(get_database_uri())
        cursor = conn.cursor()
        return conn, cursor
    except psycopg2.DatabaseError as e:
        print(f"Error de conexión a la base de datos: {e}")
        if conn:
            conn.rollback()
        raise

class Config:
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    db = None
    
    @staticmethod
    def init_app(app):
        with app.app_context():
            db.init_app(app)
            db.create_all()
        
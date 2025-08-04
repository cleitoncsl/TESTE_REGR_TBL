import os
import pyodbc
from dotenv import load_dotenv

class SQLServerConnector:
    def __init__(self, env_path=".env"):
        load_dotenv(env_path)
        self.server = os.getenv("SQL_SERVER")
        self.database = os.getenv("SQL_DATABASE")
        self.username = os.getenv("SQL_USERNAME")
        self.password = os.getenv("SQL_PASSWORD")
        self.driver = "ODBC Driver 17 for SQL Server"

    def get_connection(self):
        conn_str = (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password}"
        )
        try:
            conn = pyodbc.connect(conn_str, timeout=5)
            print(f"✅ Autenticado com sucesso em '{self.server}\\{self.database}'")
            return conn
        except pyodbc.Error as e:
            print("❌ Falha ao conectar no SQL Server.")
            print(f"Erro: {e}")
            raise

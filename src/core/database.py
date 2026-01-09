import socket

from sqlalchemy import create_engine, text

class DBManager:

    DB_CONFIGS = {
        5432: {"name": "PostgreSQL", "color": "blue", "type": "SQL"},
        3306: {"name": "MySQL/MariaDB", "color": "orange3", "type": "SQL"},
        1433: {"name": "MSSQL", "color": "white", "type": "SQL"},
        #8123: {"name": "ClickHouse", "color": "yellow", "type": "Analytical"},
    }

    @classmethod
    def scan_local_dbs(cls):
        found_dbms = ['a','b']
        for port, info in cls.DB_CONFIGS.items():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex(("127.0.0.1", port)) == 0:
                    found_dbms.append(info['name'])
        return found_dbms


    @staticmethod
    def get_databases_list(engine_url):
        engine = create_engine(engine_url)
        with engine.connect() as connection:
            # Запрос возвращает все базы, кроме системных шаблонов
            query = text("SELECT datname FROM pg_database WHERE datistemplate = false;")
            result = connection.execute(query)
            return [row[0] for row in result]

    @staticmethod
    def build_url(dbms_type, user, password, database="", host="127.0.0.1"):
        driver = "postgresql+psycopg2" if dbms_type == "PostgreSQL" else "mysql+pymysql"
        port = 5432 if dbms_type == "PostgreSQL" else 3306
        return f"{driver}://{user}:{password}@{host}:{port}/{database}"

    @staticmethod
    def get_tables_list(engine_url):
        from sqlalchemy import create_engine, inspect
        engine = create_engine(engine_url)
        inspector = inspect(engine)
        return inspector.get_table_names(schema="public")
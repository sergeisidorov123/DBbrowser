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
        found_dbms = []
        for port, info in cls.DB_CONFIGS.items():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex(("127.0.0.1", port)) == 0:
                    found_dbms.append(info['name'])
        return sorted(list(dict.fromkeys(found_dbms)))


    @staticmethod
    def get_databases_list(engine_url):
        engine = create_engine(engine_url)
        try:
            with engine.connect() as connection:
                # Запрос возвращает все базы, кроме системных шаблонов
                if "postgresql" in engine_url:
                    query = text("SELECT datname FROM pg_database WHERE datistemplate = false;")
                elif "mysql" in engine_url or "pymysql" in engine_url:
                    query = text("SHOW DATABASES;")
                else:
                    query = text("SELECT name FROM sys.databases;")
                result = connection.execute(query)
                # Попробуем вернуть скаляры (обычно для простых запросов это будет список имён)
                try:
                    names = result.scalars().all()
                    if names:
                        return [str(n) for n in names]
                except Exception:
                    pass
                # Фоллбек — пройти по строкам результата
                return [row[0] for row in result]
        except Exception as exc:
            raise RuntimeError(f"Failed to list databases: {exc}") from exc

    @staticmethod
    def build_url(dbms_type, user, password, database="", host="127.0.0.1"):
        driver = "postgresql+psycopg2" if dbms_type == "PostgreSQL" else "mysql+pymysql"
        port = 5432 if dbms_type == "PostgreSQL" else 3306
        url = f"{driver}://{user}:{password}@{host}:{port}"
        if database:
            url += f"/{database}"
        return url

    @staticmethod
    def get_tables_list(engine_url):
        from sqlalchemy import create_engine, inspect
        engine = create_engine(engine_url)
        try:
            inspector = inspect(engine)
        except Exception as exc:
            raise RuntimeError(f"Failed to create inspector: {exc}") from exc

        try:
            tables = inspector.get_table_names(schema="public")
            if tables:
                return tables
        except Exception:
            pass

        try:
            return inspector.get_table_names()
        except Exception as exc:
            raise RuntimeError(f"Failed to get table names: {exc}") from exc
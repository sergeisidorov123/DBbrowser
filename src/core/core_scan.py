from src.core.database import DBManager
from src.console.console import ConsoleUI


class DBBrowserApp:
    def __init__(self):
        self.ui = ConsoleUI()

    def run(self):
        self.ui.show_banner()

        active_dbms = self._discover_step()
        if not active_dbms: return

        dbms_type = self.ui.select_from_list("Choose DBM:", active_dbms)
        credentials = self._login_step(dbms_type)

        self._explore_databases(dbms_type, credentials)

    def _discover_step(self):
        with self.ui.show_status("Scanning"):
            found = DBManager.scan_local_dbs()
        if not found:
            # TODO менять порты
            self.ui.show_error("No DBMS on default ports")
        return found

    def _login_step(self, dbms_type):
        user = self.ui.get_input(f"Login ({dbms_type}):")
        password = self.ui.get_input("Password:", is_password=True)
        return {"user": user, "password": password}

    def _explore_databases(self, dbms_type, creds):
        base_db = "postgres" if dbms_type == "PostgreSQL" else ""
        url = DBManager.build_url(dbms_type, creds['user'], creds['password'], database=base_db)

        try:
            with self.ui.show_status("Loading..."):
                databases = DBManager.get_databases_list(url)

            if not databases:
                self.ui.show_error("No databases or access is restricted")
                return

            selected_db = self.ui.select_from_list("Choose database:", databases)

            new_url = DBManager.build_url(dbms_type, creds['user'], creds['password'], database=selected_db)

            with self.ui.show_status(f"Load from {selected_db}..."):
                tables = DBManager.get_tables_list(new_url)

            if not tables:
                self.ui.console.print(f"\n[yellow]! No tables in {selected_db}.[/yellow]")
            else:
                self.ui.show_table(
                    title=f"Tablse: {selected_db}",
                    columns=["Name"],
                    rows=[[t] for t in tables]
                )

        except Exception as e:
            self._handle_error(e)

    def _handle_error(self, e):
        error_msg = str(e)
        if "authentication failed" in error_msg:
            self.ui.show_error(f"Wrong pass or pg_hba.conf error:{error_msg}")
        else:
            self.ui.show_error(f"Ошибка: {error_msg}")
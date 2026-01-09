from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from InquirerPy import inquirer


class ConsoleUI:
    def __init__(self):
        self.console = Console()

    def show_banner(self):
        self.console.print(
            Panel("[bold blue]DB Browser CLI[/bold blue]", expand=False))

    @staticmethod
    def select_from_list(message, choices):
        return inquirer.select(
            message=message,
            choices=choices,
            pointer=">",
        ).execute()

    @staticmethod
    def get_input(message, is_password=False):
        if is_password:
            return inquirer.secret(message=message).execute()
        return inquirer.text(message=message).execute()

    def show_error(self, message):
        self.console.print(f"[bold red]❌ Ошибка:[/bold red] {message}")

    def show_table(self, title, columns, rows):
        table = Table(title=title, show_header=True, header_style="bold magenta")
        for col in columns:
            table.add_column(col)
        for row in rows:
            table.add_row(*[str(item) for item in row])
        self.console.print(table)

    def show_status(self, message):
        return self.console.status(f"[bold green]{message}...")
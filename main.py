import sys
from src.core.core_scan import DBBrowserApp

def main():
    app = DBBrowserApp()
    with app.ui.console.screen():
        app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
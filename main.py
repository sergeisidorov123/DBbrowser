import sys
from src.core.core_scan import DBBrowserApp

def main():
    app = DBBrowserApp()
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)
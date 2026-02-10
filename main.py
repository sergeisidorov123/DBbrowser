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
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
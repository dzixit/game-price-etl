import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("ITAD_API_KEY", "").strip()

    if not api_key:
        print("Brak klucza API. Uzupełnij ITAD_API_KEY w pliku .env.")
        return 1

    print("Klucz API został wczytany.")
    print("Konfiguracja jest gotowa do sprawdzenia połączenia z API.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
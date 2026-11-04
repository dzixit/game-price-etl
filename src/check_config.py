import os
from pathlib import Path

from dotenv import load_dotenv


# Ustalamy folder projektu na podstawie położenia tego pliku.
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():
    # Wczytujemy konfigurację z pliku .env w folderze projektu.
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)

    # Pobieramy klucz bez wyświetlania jego wartości.
    api_key = os.getenv("ITAD_API_KEY", "").strip()

    if not api_key:
        print("Brak klucza API. Uzupełnij ITAD_API_KEY w pliku .env.")
        return

    print("Klucz API został wczytany.")
    print("Konfiguracja jest gotowa do sprawdzenia połączenia z API.")


if __name__ == "__main__":
    main()
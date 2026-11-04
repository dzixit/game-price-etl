import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
API_URL = "https://api.isthereanydeal.com/games/search/v1"


def main():
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("ITAD_API_KEY", "").strip()

    if not api_key:
        print("Brak klucza API w konfiguracji.")
        return 1

    # Parametry określają tytuł i maksymalną liczbę wyników.
    params = {
        "title": "Hollow Knight",
        "results": 5,
    }

    # Klucz przesyłamy w nagłówku, zamiast umieszczać go w URL.
    headers = {
        "ITAD-API-Key": api_key,
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            headers=headers,
            timeout=30,
        )

        print(f"Status HTTP: {response.status_code}")

        # Odpowiedź błędna, np. 401 lub 500, wywoła wyjątek.
        response.raise_for_status()
        games = response.json()

    except requests.exceptions.Timeout:
        print("Przekroczono czas oczekiwania na API.")
        return 1

    except requests.exceptions.HTTPError:
        print("API zwróciło błąd. Sprawdź wyświetlony status HTTP.")
        return 1

    except requests.exceptions.JSONDecodeError:
        print("Odpowiedź API nie jest poprawnym JSON-em.")
        return 1

    except requests.exceptions.RequestException:
        print("Nie udało się wykonać zapytania do API.")
        return 1

    # Każde pobranie zapisujemy osobno, bez zmieniania treści odpowiedzi.
    raw_dir = PROJECT_ROOT / "data" / "raw"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output_path = raw_dir / f"search_hollow_knight_{timestamp}.json"

    try:
        raw_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(response.content)
    except OSError:
        print("Nie udało się zapisać odpowiedzi do pliku.")
        return 1

    print(f"Zapisano odpowiedź: {output_path}")

    # Sprawdzamy strukturę przed odczytaniem wyników.
    if not isinstance(games, list) or not all(
        isinstance(game, dict) and "title" in game and "id" in game
        for game in games
    ):
        print("Nieoczekiwana struktura danych. Sprawdź zapisany JSON.")
        return 1

    if not games:
        print("Brak wyników wyszukiwania.")
        return 0

    print(f"\nLiczba wyników: {len(games)}")

    for game in games:
        print(f"Tytuł: {game['title']}")
        print(f"ID: {game['id']}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
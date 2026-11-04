import csv
import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

GAME_ID = "018d937f-1ae9-734c-ba47-bd357cf07edd"
COUNTRY = "US"

INPUT_PATH = PROJECT_ROOT / "data" / "raw" / (
    f"history_{GAME_ID}_{COUNTRY}_20261104T202606533724Z.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / f"{INPUT_PATH.stem}.csv"
)

COLUMNS = [
    "game_id",
    "country",
    "shop_id",
    "shop_name",
    "timestamp_utc",
    "price",
    "regular_price",
    "currency",
    "source_file",
]


def read_amount(value):
    """Odczytuje nieujemną, skończoną kwotę."""
    if isinstance(value, bool) or not isinstance(value, (int, Decimal)):
        raise ValueError("Kwota musi być liczbą")

    amount = Decimal(value)

    if not amount.is_finite() or amount < 0:
        raise ValueError("Kwota musi być skończona i nieujemna")

    return amount


def transform_record(record):
    """Zamienia pojedynczy rekord JSON na płaski wiersz."""
    shop_id = record["shop"]["id"]
    shop_name = record["shop"]["name"]

    if type(shop_id) is not int:
        raise ValueError("ID sklepu musi być liczbą całkowitą")

    if not isinstance(shop_name, str) or not shop_name.strip():
        raise ValueError("Brak nazwy sklepu")

    timestamp = datetime.fromisoformat(
        record["timestamp"].replace("Z", "+00:00")
    )

    if timestamp.tzinfo is None:
        raise ValueError("Data nie zawiera strefy czasowej")

    price_data = record["deal"]["price"]
    regular_data = record["deal"]["regular"]

    currency = price_data["currency"]

    if not isinstance(currency, str) or not currency.strip():
        raise ValueError("Brak waluty")

    if currency != regular_data["currency"]:
        raise ValueError("Cena oferty i regularna mają różne waluty")

    price = read_amount(price_data["amount"])
    regular_price = read_amount(regular_data["amount"])

    return {
        "game_id": GAME_ID,
        "country": COUNTRY,
        "shop_id": shop_id,
        "shop_name": shop_name,
        "timestamp_utc": timestamp.astimezone(timezone.utc).isoformat(),
        "price": format(price, "f"),
        "regular_price": format(regular_price, "f"),
        "currency": currency,
        "source_file": INPUT_PATH.name,
    }


def main():
    try:
        with INPUT_PATH.open(encoding="utf-8") as file:
            # Liczby dziesiętne odczytujemy bezpośrednio jako Decimal.
            history = json.load(file, parse_float=Decimal)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Nie udało się odczytać danych: {error}")
        return 1

    if not isinstance(history, list) or not history:
        print("Oczekiwano niepustej listy rekordów.")
        return 1

    rows = []
    errors = []

    for index, record in enumerate(history, start=1):
        try:
            rows.append(transform_record(record))
        except (
            KeyError,
            TypeError,
            ValueError,
            AttributeError,
            InvalidOperation,
        ) as error:
            errors.append((index, str(error)))

    print(f"Rekordy wejściowe: {len(history)}")
    print(f"Rekordy przekształcone: {len(rows)}")
    print(f"Rekordy z błędami: {len(errors)}")

    # Nie publikujemy częściowej tabeli bez wyraźnej informacji.
    if errors:
        for index, reason in errors:
            print(f"Rekord {index}: {reason}")

        print("Nie zapisano nowego CSV. Poprzedni wynik pozostaje bez zmian.")
        return 1

    rows.sort(
        key=lambda row: (
            row["shop_id"],
            row["timestamp_utc"],
            row["currency"],
        )
    )

    # Najpierw zapis tymczasowy, potem zastąpienie pliku docelowego.
    temporary_path = OUTPUT_PATH.with_suffix(".csv.tmp")

    try:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        with temporary_path.open(
            "w", encoding="utf-8", newline=""
        ) as file:
            writer = csv.DictWriter(file, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

        temporary_path.replace(OUTPUT_PATH)

    except OSError as error:
        print(f"Nie udało się zapisać CSV: {error}")
        return 1

    print(f"Zapisano: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
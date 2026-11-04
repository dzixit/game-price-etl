import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from src import transform_history


def make_record():
    return {
        "timestamp": "2024-01-02T01:30:00+02:00",
        "shop": {
            "id": 61,
            "name": "Steam",
        },
        "deal": {
            "price": {
                "amount": 9.99,
                "amountInt": 999,
                "currency": "USD",
            },
            "regular": {
                "amount": 19.99,
                "amountInt": 1999,
                "currency": "USD",
            },
        },
    }


class TestTransformHistory(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)

        self.root = Path(temporary.name)
        self.input_path = self.root / "input.json"
        self.output_path = self.root / "processed" / "output.csv"

    def write_input(self, records):
        self.input_path.write_text(
            json.dumps(records),
            encoding="utf-8",
        )

    def run_transform(self):
        with (
            patch.object(
                transform_history, "INPUT_PATH", self.input_path
            ),
            patch.object(
                transform_history, "OUTPUT_PATH", self.output_path
            ),
            redirect_stdout(io.StringIO()),
        ):
            return transform_history.main()

    def read_output(self):
        with self.output_path.open(
            encoding="utf-8", newline=""
        ) as file:
            reader = csv.DictReader(file)
            return reader.fieldnames, list(reader)

    def test_csv_values_and_utc(self):
        self.write_input([make_record()])

        self.assertEqual(self.run_transform(), 0)

        columns, rows = self.read_output()
        self.assertEqual(columns, transform_history.COLUMNS)
        self.assertEqual(len(rows), 1)

        row = rows[0]
        self.assertEqual(row["shop_id"], "61")
        self.assertEqual(row["shop_name"], "Steam")
        self.assertEqual(
            row["timestamp_utc"],
            "2024-01-01T23:30:00+00:00",
        )
        self.assertEqual(Decimal(row["price"]), Decimal("9.99"))
        self.assertEqual(
            Decimal(row["regular_price"]), Decimal("19.99")
        )
        self.assertEqual(row["currency"], "USD")
        self.assertEqual(row["game_id"], transform_history.GAME_ID)
        self.assertEqual(row["country"], transform_history.COUNTRY)
        self.assertEqual(row["source_file"], "input.json")

    def test_rerun_does_not_append_rows(self):
        self.write_input([make_record()])

        self.assertEqual(self.run_transform(), 0)
        first_result = self.output_path.read_bytes()

        self.assertEqual(self.run_transform(), 0)

        self.assertEqual(
            self.output_path.read_bytes(),
            first_result,
        )
        _, rows = self.read_output()
        self.assertEqual(len(rows), 1)

    def test_invalid_input_preserves_previous_csv(self):
        self.write_input([make_record()])
        self.assertEqual(self.run_transform(), 0)
        previous_result = self.output_path.read_bytes()

        invalid_record = make_record()
        del invalid_record["deal"]["price"]

        # Jeden poprawny i jeden błędny rekord:
        # nie wolno opublikować częściowego wyniku.
        self.write_input([make_record(), invalid_record])

        self.assertEqual(self.run_transform(), 1)
        self.assertEqual(
            self.output_path.read_bytes(),
            previous_result,
        )


if __name__ == "__main__":
    unittest.main()
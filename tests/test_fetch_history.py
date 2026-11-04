import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from src import fetch_history


def make_record():
    return {
        "timestamp": "2024-01-01T00:00:00Z",
        "shop": {"id": 61, "name": "Steam"},
        "deal": {
            "price": {
                "amount": 10,
                "amountInt": 1000,
                "currency": "USD",
            },
        },
    }


class TestFetchHistory(unittest.TestCase):
    def run_fetch(self, records):
        response = Mock()
        response.status_code = 200
        response.content = json.dumps(records).encode("utf-8")
        response.json.return_value = records

        with tempfile.TemporaryDirectory() as directory:
            project_root = Path(directory)

            with (
                patch.object(fetch_history, "PROJECT_ROOT", project_root),
                patch.object(fetch_history, "load_dotenv"),
                patch.dict(
                    os.environ,
                    {"ITAD_API_KEY": "test-placeholder"},
                    clear=True,
                ),
                patch.object(
                    fetch_history.requests,
                    "get",
                    return_value=response,
                ),
                redirect_stdout(io.StringIO()),
            ):
                exit_code = fetch_history.main()

            # Sprawdzamy, czy odpowiedź zachowano mimo ewentualnych błędów.
            saved_files = list((project_root / "data" / "raw").glob("*.json"))
            self.assertEqual(len(saved_files), 1)
            self.assertEqual(saved_files[0].read_bytes(), response.content)

            return exit_code

    def test_valid_records(self):
        self.assertEqual(self.run_fetch([make_record()]), 0)

    def test_all_records_invalid(self):
        self.assertEqual(self.run_fetch([{}]), 1)

    def test_partially_invalid_records(self):
        self.assertEqual(self.run_fetch([make_record(), {}]), 1)

    def test_empty_history(self):
        self.assertEqual(self.run_fetch([]), 0)


if __name__ == "__main__":
    unittest.main()
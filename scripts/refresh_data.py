"""Run the scheduled application data refresh."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.refresh import refresh_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh application data from raw CSV files")
    parser.add_argument("--raw-path", default=None, help="Optional raw CSV directory")
    args = parser.parse_args()
    result = refresh_data(args.raw_path)
    print(f"Refresh {result['status']}: {result['rows_loaded']} rows loaded (run {result['run_id']})")


if __name__ == "__main__":
    main()

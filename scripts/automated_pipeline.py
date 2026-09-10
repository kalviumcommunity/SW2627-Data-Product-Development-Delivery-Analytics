"""
Automated Data Pipeline (LU 2.58)
Ingests raw CSVs, cleans, aggregates, and outputs processed data.

Usage:
    python scripts/automated_pipeline.py --input data/raw --output data/processed
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

RAW_FILES = {
    "employee_master_raw.csv": "employee_master",
    "timesheets_raw.csv": "timesheets",
    "allocations_raw.csv": "allocations",
    "billing_raw.csv": "billing",
}


def ingest(source_dir: Path) -> dict[str, pd.DataFrame]:
    """Stage 1: Load raw CSV files."""
    logger.info("Ingesting data from: %s", source_dir)
    frames = {}
    for filename, label in RAW_FILES.items():
        file_path = source_dir / filename
        if not file_path.exists():
            logger.error("Missing source file: %s", file_path)
            sys.exit(1)
        df = pd.read_csv(file_path)
        logger.info("Ingested %s: %d rows, %d columns", label, len(df), len(df.columns))
        frames[label] = df
    return frames


def clean(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Stage 2: Drop nulls in key columns, coerce numeric types."""
    logger.info("Cleaning data...")
    cleaned = {}

    emp = frames["employee_master"].copy()
    initial = len(emp)
    emp = emp.dropna(subset=["employee_id", "department"])
    logger.info("employee_master: %d -> %d rows", initial, len(emp))
    cleaned["employee_master"] = emp

    ts = frames["timesheets"].copy()
    initial = len(ts)
    ts = ts.dropna(subset=["employee_id", "hours_logged"])
    ts["hours_logged"] = pd.to_numeric(ts["hours_logged"], errors="coerce")
    ts["billable_hours"] = pd.to_numeric(ts["billable_hours"], errors="coerce")
    ts = ts[ts["hours_logged"] > 0]
    logger.info("timesheets: %d -> %d rows", initial, len(ts))
    cleaned["timesheets"] = ts

    alloc = frames["allocations"].copy()
    initial = len(alloc)
    alloc = alloc.dropna(subset=["employee_id", "project_id"])
    alloc["allocated_hours"] = pd.to_numeric(alloc["allocated_hours"], errors="coerce")
    alloc = alloc[alloc["allocated_hours"] > 0]
    logger.info("allocations: %d -> %d rows", initial, len(alloc))
    cleaned["allocations"] = alloc

    bill = frames["billing"].copy()
    initial = len(bill)
    bill = bill.dropna(subset=["employee_id", "billed_amount"])
    bill["billed_amount"] = pd.to_numeric(bill["billed_amount"], errors="coerce")
    bill["billable_hours"] = pd.to_numeric(bill["billable_hours"], errors="coerce")
    bill = bill[bill["billed_amount"] > 0]
    logger.info("billing: %d -> %d rows", initial, len(bill))
    cleaned["billing"] = bill

    return cleaned


def aggregate(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Stage 3: Compute department-level and team-level aggregations."""
    logger.info("Aggregating...")
    results = {}

    ts = frames["timesheets"]
    dept_utilization = (
        ts.groupby("task_category")
        .agg(
            total_hours=("hours_logged", "sum"),
            total_billable=("billable_hours", "sum"),
            entry_count=("timesheet_id", "count"),
        )
        .reset_index()
    )
    dept_utilization["utilization_rate"] = (
        dept_utilization["total_billable"] / dept_utilization["total_hours"] * 100
    ).round(2)
    logger.info("Utilization by task_category: %d rows", len(dept_utilization))
    results["utilization_by_category"] = dept_utilization

    bill = frames["billing"]
    billing_summary = (
        bill.groupby("client_id")
        .agg(
            total_billed=("billed_amount", "sum"),
            total_hours=("billable_hours", "sum"),
            invoice_count=("invoice_id", "count"),
        )
        .reset_index()
    )
    logger.info("Billing by client: %d rows", len(billing_summary))
    results["billing_by_client"] = billing_summary

    emp = frames["employee_master"]
    team_headcount = (
        emp.groupby(["department", "team"])
        .agg(headcount=("employee_id", "count"))
        .reset_index()
    )
    logger.info("Team headcount: %d rows", len(team_headcount))
    results["team_headcount"] = team_headcount

    alloc = frames["allocations"]
    project_allocations = (
        alloc.groupby("project_id")
        .agg(
            total_allocated_hours=("allocated_hours", "sum"),
            employee_count=("employee_id", "nunique"),
        )
        .reset_index()
    )
    logger.info("Project allocations: %d rows", len(project_allocations))
    results["project_allocations"] = project_allocations

    return results


def output(frames: dict[str, pd.DataFrame], agg: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Stage 4: Write cleaned and aggregated CSVs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Writing output to: %s", output_dir)

    for label, df in frames.items():
        path = output_dir / f"{label}_cleaned.csv"
        df.to_csv(path, index=False)
        logger.info("Wrote %s (%d rows)", path.name, len(df))

    for label, df in agg.items():
        path = output_dir / f"{label}.csv"
        df.to_csv(path, index=False)
        logger.info("Wrote %s (%d rows)", path.name, len(df))

    logger.info("Pipeline complete.")


def main():
    parser = argparse.ArgumentParser(description="Automated data pipeline")
    parser.add_argument("--input", default="data/raw", help="Source directory with raw CSVs")
    parser.add_argument("--output", default="data/processed", help="Output directory for processed CSVs")
    args = parser.parse_args()

    source_dir = Path(args.input)
    output_dir = Path(args.output)

    raw = ingest(source_dir)
    cleaned = clean(raw)
    agg = aggregate(cleaned)
    output(cleaned, agg, output_dir)


if __name__ == "__main__":
    main()

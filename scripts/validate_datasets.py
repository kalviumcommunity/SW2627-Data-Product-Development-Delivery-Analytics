"""
Dataset Validation Script
Validates raw datasets before ingestion.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.ingestion.validate_sources import run_full_validation


# Define expected schemas for each dataset
SCHEMAS = {
    "employee_master_raw.csv": {
        "columns": [
            "employee_id", "employee_name", "department", "team", 
            "designation", "employment_type", "experience_years",
            "joining_date", "location", "manager_id", "skill_primary",
            "skill_secondary", "grade_level", "employment_status",
            "cost_center", "capacity_hours_monthly"
        ],
        "min_rows": 100
    },
    "timesheets_raw.csv": {
        "columns": [
            "timesheet_id", "employee_id", "work_date", "month", "week",
            "project_id", "task_id", "task_category", "hours_logged",
            "billable_hours", "non_billable_hours", "admin_hours",
            "training_hours", "internal_hours", "leave_hours",
            "overtime_hours", "work_location", "timesheet_status",
            "approval_date", "entry_source", "description"
        ],
        "min_rows": 1000
    },
    "allocations_raw.csv": {
        "columns": [
            "allocation_id", "employee_id", "project_id", "client_id",
            "allocation_start_date", "allocation_end_date",
            "allocated_hours", "allocation_percentage",
            "planned_billable_hours", "planned_non_billable_hours",
            "project_role", "project_status", "priority",
            "staffing_status", "expected_utilization"
        ],
        "min_rows": 100
    },
    "billing_raw.csv": {
        "columns": [
            "billing_id", "client_id", "project_id", "employee_id",
            "billing_date", "billing_month", "billable_hours",
            "billing_rate", "billed_amount", "invoice_id",
            "invoice_status", "payment_status", "currency",
            "billing_type", "writeoff_hours", "writeoff_amount"
        ],
        "min_rows": 100
    }
}


def validate_all_datasets(data_dir: str) -> None:
    """
    Validate all raw datasets in the data directory.
    
    Args:
        data_dir: Path to the raw data directory
    """
    data_path = Path(data_dir)
    
    print("=" * 60)
    print("DATASET VALIDATION REPORT")
    print("=" * 60)
    
    all_valid = True
    
    for filename, schema in SCHEMAS.items():
        file_path = data_path / filename
        print(f"\n{'─' * 60}")
        print(f"Validating: {filename}")
        print(f"{'─' * 60}")
        
        if not file_path.exists():
            print(f"  ❌ FILE NOT FOUND: {file_path}")
            all_valid = False
            continue
        
        try:
            df = load_csv(str(file_path))
            results = run_full_validation(df, schema)
            
            print(f"  Shape: {results['shape']}")
            print(f"  Row count valid: {results['row_count']['valid']}")
            print(f"  Empty columns: {not results['empty_columns']['valid']}")
            
            if "schema" in results:
                print(f"  Schema valid: {results['schema']['valid']}")
                if results['schema']['missing_columns']:
                    print(f"    Missing: {results['schema']['missing_columns']}")
            
            if results["overall_valid"]:
                print(f"  ✅ PASSED")
            else:
                print(f"  ⚠️  ISSUES FOUND")
                all_valid = False
                
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            all_valid = False
    
    print(f"\n{'=' * 60}")
    if all_valid:
        print("OVERALL: ✅ ALL VALIDATIONS PASSED")
    else:
        print("OVERALL: ⚠️  SOME VALIDATIONS FAILED")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_datasets.py <data_directory>")
        sys.exit(1)
    
    validate_all_datasets(sys.argv[1])

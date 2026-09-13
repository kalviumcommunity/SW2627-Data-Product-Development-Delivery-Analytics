# Employee Utilization Analytics

Employee Utilization Analytics is a workforce planning and operations dashboard
for understanding employee capacity, project allocation, timesheet activity,
billable utilization, and billing performance.

It combines raw workforce CSV files with a SQLite-backed FastAPI service and a
Streamlit dashboard. Operations teams and managers can identify overloaded or
under-utilized employees, compare teams and projects, review data-quality
signals, plan work, and export filtered reports.

## Features

- Workforce overview with dataset statistics, KPIs, and charts
- Employee, department, team, and project analysis
- Capacity load and billable utilization metrics
- Weekly work planning with assignment management
- Rule-based insights and alerts for overload, under-utilization, unused capacity, and assignment conflicts
- CSV, JSON, and Excel report exports
- FastAPI authentication, role-based access, refresh endpoints, and health checks
- Automated data validation and weekly processed-data refreshes with GitHub Actions

## Dataset Description

### Source files

The automated pipeline reads these files from `data/raw/`:

| File | Purpose | Important fields |
| --- | --- | --- |
| `employee_master_raw.csv` | Employee and capacity master data | `employee_id`, `employee_name`, `department`, `team`, `experience_years`, `employment_status`, `capacity_hours_monthly` |
| `timesheets_raw.csv` | Logged and billable work | `timesheet_id`, `employee_id`, `work_date`, `project_id`, `task_category`, `hours_logged`, `billable_hours`, `overtime_hours`, `timesheet_status` |
| `allocations_raw.csv` | Planned project allocation | `allocation_id`, `employee_id`, `project_id`, `allocation_start_date`, `allocation_end_date`, `allocated_hours`, `allocation_percentage`, `expected_utilization` |
| `billing_raw.csv` | Client billing and revenue data | `billing_id`, `client_id`, `project_id`, `employee_id`, `billing_date`, `billable_hours`, `billing_rate`, `billed_amount`, `currency`, `payment_status` |

All source files are CSV files. The complete source data dictionary is in
`data/raw/data_dictionary.csv`.

### Data locations and refresh

- `data/raw/` contains source data and should not be edited in place.
- `data/processed/` contains cleaned and aggregated, versioned CSV outputs.
- `data/app.db` contains the SQLite tables used by the application API and dashboard.
- The dashboard can also load one or more CSV or JSON files through the sidebar uploader.
- The GitHub Actions pipeline runs weekly on Monday at 06:00 UTC, or manually through `workflow_dispatch`.
- The workflow regenerates `data/processed/` and opens a pull request for review instead of pushing directly to `main`.
- The local refresh command loads the raw CSV files into SQLite and records the run in the `refresh_runs` table.

## Getting Started

The application uses two local processes: FastAPI for authentication, database
access, and planning actions; and Streamlit for the user interface.

### Four-step setup

1. **Clone the repository and enter the project directory**

   ```bash
   git clone https://github.com/kalviumcommunity/SW2627-Data-Product-Development-Delivery-Analytics.git
   cd SW2627-Data-Product-Development-Delivery-Analytics
   ```

2. **Create and activate a virtual environment**

   Windows PowerShell:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies and configure the environment**

   ```bash
   pip install -r requirements.txt
   ```

   Copy `.env.example` to `.env` and set a local admin email and password. For
   example, on Windows use `copy .env.example .env`; on macOS/Linux use
   `cp .env.example .env`. At minimum, update:

   ```dotenv
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=use-a-strong-local-password
   ADMIN_NAME=System Administrator
   ```

4. **Start both application processes**

   Open two terminals in the project directory with the virtual environment
   activated.

   Terminal 1, start the API:

   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```

   Terminal 2, start the dashboard:

   ```bash
   streamlit run app.py
   ```

   Open the Streamlit URL shown in the terminal, usually
   `http://localhost:8501`, and sign in with the credentials configured in
   `.env`. The API health check is available at
   `http://127.0.0.1:8000/health`.

The API creates `data/app.db` on startup and seeds the configured admin user if
that user does not already exist.

## Usage Guide

### Sign in and load data

1. Start the API before opening the dashboard.
2. Sign in with the configured admin account.
3. The dashboard initially loads the source tables from SQLite when available.
4. To use another dataset, expand the sidebar uploader and select one or more
   `.csv` or `.json` files.
5. Select the active dataset from the sidebar's dataset selector.
6. Use **Reset** to clear uploaded files and return to database-backed data.

### Navigate the dashboard

- **Overview**: Inspect row count, columns, null percentage, memory usage,
  employee counts, hours, billable hours, and utilization charts.
- **Workforce**: Search employees and filter by department, employment status,
  and team.
- **Work Planning**: Add work assignments to employees by date, start time,
  and duration. Managers and administrators can edit or delete assignments.
- **Capacity & Utilization**: Compare monthly capacity, allocated hours,
  logged hours, billable hours, capacity load, and utilization status.
- **Team Analytics**: Filter by department, team, or employee and compare
  capacity load, utilization, available hours, and project allocation.
- **Insights / Alerts**: Review critical, warning, and informational alerts.
- **Reports**: Preview and download filtered source data, capacity summaries,
  or insights and alerts as CSV, JSON, or Excel.

### Filters and date periods

Use the sidebar period selector to choose **This Week**, **This Month**,
**This Quarter**, or a custom date range. Where available, use the page-level
search and department, team, employee, or status filters to narrow the results.
The dashboard detects common date columns such as `work_date`,
`allocation_start_date`, and `billing_date`.

### Refresh application data

To manually load the four raw CSV files into SQLite, run this from the project
root while the virtual environment is active:

```bash
python scripts/refresh_data.py
```

The API also exposes these authenticated endpoints:

- `POST /refresh`: Admin-only data refresh
- `GET /refresh/status`: Refresh status for authenticated users

The API must be running for these endpoints and for work-planning actions.

### Run the automated CSV pipeline

The automated pipeline cleans the raw files, creates aggregates, and writes
processed CSV files:

```bash
python scripts/automated_pipeline.py --input data/raw --output data/processed
```

The default paths are `data/raw` and `data/processed`, so the arguments may be
omitted when using those directories.

### Run tests

Run the complete automated test suite from the project root:

```bash
pytest -q
```

## Pipeline Architecture

The project has two related data paths: the scheduled processed-data pipeline
and the application refresh path.

### Scheduled processed-data pipeline

```text
data/raw/*.csv
      |
      v
1. Ingestion
   Load employee, timesheet, allocation, and billing CSV files.
      |
      v
2. Cleaning and validation
   Drop rows missing required identifiers or measures, coerce numeric fields,
   and remove invalid non-positive hours or billed amounts.
      |
      v
3. Aggregation
   Calculate utilization by task category, billing by client, team headcount,
   and project allocation summaries.
      |
      v
4. Processed output
   Write cleaned source tables and aggregate CSV files to data/processed/.
      |
      v
5. Dashboard and analysis
   Load the processed or database-backed data, apply filters, and calculate
   capacity, utilization, KPIs, charts, and drill-down tables.
      |
      v
6. Alerts and reports
   Evaluate static workforce thresholds, display explainable alerts, and allow
   users to download filtered CSV, JSON, or Excel reports.
```

The implementation is `scripts/automated_pipeline.py`. GitHub Actions runs it
from `.github/workflows/pipeline.yml` and creates a pull request containing any
new processed outputs.

### Application refresh path

```text
Raw CSV files in data/raw/
      |
      v
Admin refresh command or POST /refresh
      |
      v
Read and load source tables into SQLite
      |
      v
Upsert employee lookup records and record refresh_runs status
      |
      v
FastAPI serves authenticated data and planning operations
      |
      v
Streamlit loads database tables, renders analytics, alerts, and exports
```

The application refresh implementation is in `src/refresh/pipeline.py`. The
dashboard can also bypass the database for an interactive CSV or JSON upload.

## Derived Features

The following fields are calculated by feature engineering, pipeline
aggregation, or dashboard analytics rather than being direct source fields.

| Column | Type | Description | Example |
| --- | --- | --- | --- |
| `utilization_rate` | float | Billable hours divided by total hours, multiplied by 100. | `72.5` |
| `allocation_variance` | float | Difference between actual and allocated hours as a percentage of allocated hours. | `15.0` |
| `efficiency_score` | float | Weighted score using utilization, allocation variance, and approval status when those inputs exist. | `78.4` |
| `revenue_per_hour` | float | Billed amount divided by billable hours; returns zero when billable hours are not positive. | `85.25` |
| `experience_segment` | string | Experience band derived from years of experience. | `Senior` |
| `flag_low_utilization` | boolean | `True` when utilization is below 60%. | `False` |
| `flag_over_allocation` | boolean | `True` when actual hours exceed allocated hours by more than 20%. | `True` |
| `flag_under_allocation` | boolean | `True` when actual hours are more than 20% below allocated hours. | `False` |
| `flag_missing_timesheet` | boolean | Flags a missing `hours_worked` value when that field is present. | `False` |
| `flag_negative_hours` | boolean | Flags a negative `hours_worked` value. | `False` |
| `total_hours` | float | Aggregate logged or billable hours, depending on the output table. | `1250.5` |
| `total_billable` | float | Total billable hours in the task-category aggregation. | `890.25` |
| `entry_count` | integer | Number of timesheet entries in a task-category group. | `125` |
| `total_billed` | float | Sum of billed amounts for a client. | `45230.75` |
| `invoice_count` | integer | Number of invoices associated with a client. | `18` |
| `headcount` | integer | Number of employees in a department and team group. | `12` |
| `total_allocated_hours` | float | Sum of allocated hours for a project. | `640.0` |
| `employee_count` | integer | Number of distinct employees allocated to a project. | `8` |
| `capacity_load_pct` | float | Allocated hours divided by monthly capacity, multiplied by 100. | `105.0` |
| `utilization_pct` | float | Billable hours divided by logged hours, multiplied by 100. | `68.3` |
| `capacity_variance_hours` | float | Monthly capacity minus allocated hours. | `-8.0` |
| `capacity_status` | string | Status derived from capacity load: `Overloaded` above 100%, `On target` from 70% through 100%, or `Available` below 70%. | `Overloaded` |
| `severity` | string | Alert priority generated by the insights engine. | `Critical` |
| `type` | string | Alert condition detected by the insights engine. | `Overloaded` |
| `subject` | string | Employee or identifier associated with an alert. | `Employee 0001` |
| `evidence` | string | Human-readable metric evidence supporting an alert. | `Allocated 168.0h against 160.0h capacity (105.0%).` |
| `recommendation` | string | Suggested action associated with an alert. | `Review allocations and move work to available capacity.` |

The feature-engineering implementation is in `src/features/derive_features.py`.
Dashboard-specific capacity features are calculated in
`src/dashboard/data_handler.py`.

## Known Limitations

- The application is not real-time. Data changes appear after a manual refresh,
  database reload, upload, or scheduled pipeline run.
- The automated pipeline expects all four source CSV files and their expected
  column names.
- Cleaning removes rows with missing required identifiers or invalid numeric
  measures, so source row counts may differ from processed row counts.
- Numeric parsing tolerates formatted values in dashboard calculations, but
  inconsistent source formats can still reduce data quality.
- Billing records may contain multiple currencies. The application does not
  perform currency conversion before comparing or aggregating amounts.
- Alert thresholds are static: capacity load above 100% is critical, utilization
  below 70% is a warning, and capacity below 50% generates an informational
  alert. There is no seasonal adjustment.
- Capacity calculations depend on matching `employee_id` values across source
  tables. Unmatched employees may have zero allocated, logged, or billable hours.
- The dashboard supports CSV and JSON uploads, but it does not validate every
  possible schema before displaying a dataset.
- Reports are currently available as CSV, JSON, or Excel downloads from the dashboard. Automated email delivery is not part of the current product scope.
- Work-planning operations require the FastAPI service to be running and a user
  with the appropriate role.
- Development credentials and secrets must not be reused in staging or
  production. Production requires `APP_ENV=production`, `APP_DEBUG=false`, a
  unique JWT secret of at least 32 characters, and a strong admin password.
- Raw files are treated as the source of truth and should not be edited in
  place. Update the raw data or pipeline code, then regenerate processed data.

## Project Structure

```text
app.py                         Streamlit entry point
src/api/                       FastAPI routes and authentication
src/dashboard/                 Dashboard pages, filters, KPIs, and alerts
src/features/                  Feature engineering functions
src/refresh/                   Raw CSV to SQLite refresh pipeline
scripts/automated_pipeline.py  Raw CSV to processed CSV pipeline
data/raw/                      Source CSV files and data dictionary
data/processed/                Cleaned and aggregated CSV outputs
tests/                         Automated tests
.github/workflows/             Validation and scheduled pipeline workflows
```

## Security

Keep local credentials in the ignored `.env` file and never commit secrets.
Review `SECURITY.md` before deploying outside a local development environment.

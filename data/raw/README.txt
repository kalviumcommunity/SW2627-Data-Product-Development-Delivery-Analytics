EMPLOYEE UTILIZATION ANALYTICS — RAW DATASET (SPRINT 1)

Purpose
-------
This package is the deliberately imperfect RAW dataset for the Employee Utilization Analytics project.
It is designed to support the project's ingestion, profiling, data-quality, cleaning, preprocessing,
EDA, KPI, SQL, visualization, Streamlit and automation work.

IMPORTANT
---------
Do NOT manually "fix" these raw files before the cleaning/profiling phase. The inconsistencies are
intentional so the project can demonstrate data-quality detection and cleaning using the relevant
Learning Units and preferred tools (primarily Python/pandas, with SQL for database-side cleaning/validation).

Source simulation
-----------------
1. employee_master_raw.csv  : employee/master/reference data
2. timesheets_raw.csv       : work/time-entry transactions
3. allocations_raw.csv      : project staffing/allocation records
4. billing_raw.csv          : client billing/invoice transactions

Approximate scale
-----------------
Employees: 850
Projects: 180
Clients: 60
Timesheet rows: 75,300
Allocation rows: 7,550
Billing rows: 18,100

Intentional data-quality issues
--------------------------------
- Missing values
- Duplicate records
- Inconsistent capitalization and whitespace
- Mixed date formats
- Numeric values stored as text
- Invalid negative hours/rates
- Allocation percentages above 100
- Orphan employee/project/client IDs
- Pending/unapproved records
- Different categorical representations

Suggested workflow
------------------
RAW → INGEST → PROFILE → QUALITY CHECKS → CLEAN → STANDARDIZE → VALIDATE JOINS
→ MERGE → FEATURE ENGINEERING → ANALYTICS DATASET → KPI/SQL/EDA → DASHBOARD

Filtering dimensions supported
------------------------------
Date, month, week, quarter, employee, department, team, designation, employment type,
experience, location, manager, skill, employment status, project, project type, project status,
priority, client, client segment, industry, country, billing type, task category, work location,
timesheet status, billable/non-billable work, staffing status, allocation percentage,
payment status, invoice status, currency and other derived KPI/risk fields.
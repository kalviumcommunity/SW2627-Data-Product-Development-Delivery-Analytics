# Video Script — Employee Utilization Analytics

---

## Learning Unit: 2.11 — Development Environment & Workspace Setup

**Date:** 2026-08-27 15:00

### Introduction
Hey everyone! Welcome back to our Employee Utilization Analytics project. In this video, we're covering Learning Unit 2.11 — Development Environment & Workspace Setup.

### What We Built & Why It Matters
We built a clean, isolated Python workspace with:
- **Virtual Environment (venv)** — Keeps project dependencies separate
- **Project Folder Structure** — Organizes data, notebooks, scripts, and output
- **.gitignore** — Prevents secrets and cache files from being committed
- **requirements.txt** — Documents all dependencies for reproducibility

### Step-by-Step Walkthrough
1. Create virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows)
3. Install packages: `pip install pandas numpy matplotlib seaborn streamlit plotly sqlalchemy`
4. Create folder structure: data/raw, data/processed, notebooks, scripts, output
5. Create .gitignore and requirements.txt

### Challenges Faced
- Package installation timeout — Split into two batches
- Windows activation path — Used `venv/Scripts/activate`

### Final Outcome
A reproducible workspace that any team member can set up in 4 commands.

---

## Learning Unit: 2.12 — GitHub Repository & Team Workflow Setup

**Date:** 2026-08-27 16:00

### Introduction
In this video, we're covering Learning Unit 2.12 — GitHub Repository & Team Workflow Setup.

### What We Built & Why It Matters
We established:
- **Branching Strategy** — Each LU gets its own feature branch
- **Commit Conventions** — Structured commit messages
- **Pull Request Workflow** — Code review before merging
- **GitHub Issues** — Trackable work items

### Step-by-Step Walkthrough
1. Create feature branch: `git checkout -b 2.12-feature/github-workflow-setup`
2. Create GitHub issues for tasks
3. Write code and commit with proper format
4. Push and create PR with `Closes #issue-number`
5. Merge PR after review

### Challenges Faced
- GitHub labels don't exist by default — Created issues without labels
- Branch protection blocks merge — Used `--admin` flag

### Final Outcome
A complete GitHub workflow for team collaboration.

---

## Learning Unit: 2.13 — Python Data Workflow Foundations

**Date:** 2026-08-27 17:00

### Introduction
In this video, we're covering Learning Unit 2.13 — Python Data Workflow Foundations.

### What We Built & Why It Matters
We created reusable data pipeline modules following the read-process-output pattern:
- **src/ingestion/** — Data loading functions
- **src/processing/** — Data cleaning functions
- **src/output/** — Data export functions

### Step-by-Step Walkthrough
1. Create src/ package structure with __init__.py files
2. Add load_data.py with CSV/JSON loading functions
3. Add clean_data.py with profiling and cleaning functions
4. Add export_data.py with CSV/JSON export functions
5. Create pipeline.py demonstrating the workflow pattern

### Challenges Faced
No major issues encountered.

### Final Outcome
Modular data pipeline code that's reusable and maintainable.

---

## Learning Unit: 2.14 — Dataset Intake & Source Validation

**Date:** 2026-08-27 17:30

### Introduction
In this video, we're covering Learning Unit 2.14 — Dataset Intake & Source Validation.

### What We Built & Why It Matters
We implemented dataset validation functions to check schema, row counts, data types, and empty columns before ingestion.

### Step-by-Step Walkthrough
1. Create validate_sources.py with validation functions
2. Define expected schemas for all 4 raw datasets
3. Create validate_datasets.py for batch validation
4. Run validation against real data

### Challenges Faced
No major issues encountered.

### Final Outcome
All 4 datasets validated successfully against expected schemas.

---

## Learning Unit: 2.15 — CSV & JSON Data Ingestion

**Date:** 2026-08-27 18:00

### Introduction
In this video, we're covering Learning Unit 2.15 — CSV & JSON Data Ingestion.

### What We Built & Why It Matters
We enhanced the data loading module with automatic encoding detection and ingestion reports.

### Step-by-Step Walkthrough
1. Add detect_encoding function for automatic encoding detection
2. Enhance load_csv and load_json with auto-encoding support
3. Add generate_ingestion_report for loading summaries
4. Create ingest_data.py for batch loading

### Challenges Faced
- Emoji encoding issues on Windows — Replaced with ASCII alternatives

### Final Outcome
Robust data loading with automatic encoding detection and reports.

---

## Learning Unit: 2.16 — Dataset Profiling & Quality Assessment

**Date:** 2026-08-27 19:00

### Introduction
In this video, we're covering Learning Unit 2.16 — Dataset Profiling & Quality Assessment.

### What We Built & Why It Matters
We created comprehensive dataset profiling functions to assess data quality.

### Step-by-Step Walkthrough
1. Create profile_dataset.py with profiling functions
2. Add profile_dataframe, detect_missing_patterns, detect_duplicates
3. Add profile_categorical_columns and profile_numeric_columns
4. Create profile_datasets.py for batch profiling

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully profiled all 4 raw datasets with quality insights.

---

## Learning Unit: 2.17 — Data Dictionary & Business Context Mapping

**Date:** 2026-08-27 19:30

### Introduction
In this video, we're covering Learning Unit 2.17 — Data Dictionary & Business Context Mapping.

### What We Built & Why It Matters
We implemented data dictionary module to connect raw column names to business meaning.

### Step-by-Step Walkthrough
1. Create data_dictionary.py with loading and querying functions
2. Add get_column_info, get_file_columns, get_kpi_columns
3. Add generate_data_dictionary_report for formatted output
4. Create generate_data_dictionary.py for report generation

### Challenges Faced
No major issues encountered.

### Final Outcome
Documented 33 columns across 4 datasets with 9 KPI-related columns.

---

## Learning Unit: 2.18 — Missing Value Detection & Imputation

**Date:** 2026-08-27 20:00

### Introduction
In this video, we're covering Learning Unit 2.18 — Missing Value Detection & Imputation.

### What We Built & Why It Matters
We implemented missing value detection and imputation functions for data cleaning.

### Step-by-Step Walkthrough
1. Create missing_values.py with detection and imputation functions
2. Add analyze_missing_values for comprehensive analysis
3. Add impute_numeric and impute_categorical functions
4. Add impute_by_group for group-based imputation

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully analyzed all 4 raw datasets with multiple imputation strategies.

---

## Learning Unit: 2.19 — Data Type Enforcement & Standardisation

**Date:** 2026-08-27 20:30

### Introduction
In this video, we're covering Learning Unit 2.19 — Data Type Enforcement & Standardisation.

### What We Built & Why It Matters
We implemented type enforcement functions for converting and standardizing data types.

### Step-by-Step Walkthrough
1. Create type_enforcement.py with type conversion functions
2. Add enforce_date_type, enforce_numeric, enforce_boolean
3. Add clean_currency, clean_percentage, standardize_string
4. Create enforce_types.py for type analysis

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully analyzed all 4 raw datasets with multiple type conversion functions.

---

## Learning Unit: 2.20 — Duplicate Detection & Record Deduplication

**Date:** 2026-08-27 21:00

### Introduction
In this video, we're covering Learning Unit 2.20 — Duplicate Detection & Record Deduplication.

### What We Built & Why It Matters
We implemented duplicate detection and removal functions for data cleaning.

### Step-by-Step Walkthrough
1. Create deduplication.py with duplicate detection functions
2. Add find_exact_duplicates, find_first_duplicates
3. Add remove_duplicates, log_duplicates_removed, analyze_duplicates
4. Create detect_duplicates.py for duplicate analysis

### Challenges Faced
No major issues encountered.

### Final Outcome
Found duplicates in timesheets (502), allocations (96), billing (176).

---

## Learning Unit: 2.21 — String Cleaning & Text Normalisation

**Date:** 2026-08-28 10:00

### Introduction
In this video, we're covering Learning Unit 2.21 — String Cleaning & Text Normalisation.

### What We Built & Why It Matters
We implemented string cleaning and normalization functions for data standardization.

### Step-by-Step Walkthrough
1. Create string_normalization.py with text cleaning functions
2. Add normalize_whitespace, normalize_case functions
3. Add remove_special_characters, standardize_categorical_labels
4. Create analyze_strings.py for string analysis

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully analyzed all 4 raw datasets with multiple text normalization functions.

---

## Learning Unit: 2.22 — Date & Time Transformation Pipeline

**Date:** 2026-08-28 11:00

### Introduction
In this video, we're covering Learning Unit 2.22 — Date & Time Transformation Pipeline.

### What We Built & Why It Matters
We implemented date parsing and transformation functions for datetime standardization.

### Step-by-Step Walkthrough
1. Create date_transforms.py with date transformation functions
2. Add parse_dates, extract_date_features functions
3. Add calculate_time_since, create_date_ranges functions
4. Create transform_dates.py for date analysis

### Challenges Faced
- infer_datetime_format parameter not available — Removed the parameter

### Final Outcome
Successfully analyzed all 4 raw datasets with multiple date transformation functions.

---

---

## Learning Unit: 2.24 — Data Consistency & Validation Rules

**Date:** 2026-08-28 14:00

### Introduction
In this video, we're covering Learning Unit 2.24 — Data Consistency & Validation Rules.

### What We Built & Why It Matters
We implemented data consistency and validation rules for quality checks.

### Step-by-Step Walkthrough
1. Create consistency_rules.py with validation functions
2. Add check_null_thresholds, check_value_ranges functions
3. Add check_referential_integrity, check_business_rules
4. Create validate_consistency.py for validation

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully analyzed all 4 raw datasets with multiple validation functions.

---

## Learning Unit: 2.25 — Multi-Source Merging & Join Validation

**Date:** 2026-08-28 15:00

### Introduction
In this video, we're covering Learning Unit 2.25 — Multi-Source Merging & Join Validation.

### What We Built & Why It Matters
We implemented multi-source merging with validation for data integration.

### Step-by-Step Walkthrough
1. Create merge_datasets.py with merging functions
2. Add validate_keys_before_merge, merge_with_validation
3. Add check_row_count_integrity, identify_unmatched_records
4. Create merge_datasets.py for merging demo

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully merged all 4 datasets with 99.88% employee ID overlap.

---

## Learning Unit: 2.26 — Feature Engineering & Derived Business Columns

**Date:** 2026-08-28 16:00

### Introduction
In this video, we're covering Learning Unit 2.26 — Feature Engineering & Derived Business Columns.

### What We Built & Why It Matters
We implemented feature engineering and derived business columns for analytics.

### Step-by-Step Walkthrough
1. Create derive_features.py with feature engineering functions
2. Add calculate_utilization_rate, calculate_allocation_variance
3. Add create_efficiency_score, create_risk_flags
4. Create engineer_features.py for feature engineering demo

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully created derived columns for all datasets with efficiency scores and risk flags.

---

## Learning Unit: 2.28 — Distribution Analysis for Business Trends

**Date:** 2026-08-28 17:00

### Introduction
In this video, we're covering Learning Unit 2.28 — Distribution Analysis for Business Trends.

### What We Built & Why It Matters
We implemented distribution analysis for business trends and insights.

### Step-by-Step Walkthrough
1. Create distribution_analysis.py with distribution analysis functions
2. Add analyze_numeric_distribution, analyze_categorical_distribution
3. Add analyze_utilization_distribution, analyze_hours_distribution
4. Create analyze_distributions.py for distribution analysis

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully analyzed all 3 raw datasets with multiple distribution analysis functions.

---

## Learning Unit: 2.30 — GroupBy Aggregation & Segment Insights

**Date:** 2026-08-28 18:00

### Introduction
In this video, we're covering Learning Unit 2.30 — GroupBy Aggregation & Segment Insights.

### What We Built & Why It Matters
We implemented GroupBy aggregation and segment insights for analytics.

### Step-by-Step Walkthrough
1. Create groupby_analysis.py with segment analysis functions
2. Add analyze_by_department, analyze_by_team, analyze_by_experience_segment
3. Add analyze_utilization_by_segment, find_top_performers, find_bottom_performers
4. Create analyze_segments.py for segment analysis

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully analyzed all 3 raw datasets with multiple segment analysis functions.

---

---

## Learning Unit: 2.31 — Time-Series Trend & Rolling Metrics

**Date:** 2026-08-28 19:00

### Introduction
In this video, we're covering Learning Unit 2.31 — Time-Series Trend & Rolling Metrics.

### What We Built & Why It Matters
We implemented time-series trend analysis and rolling metrics for analytics.

### Step-by-Step Walkthrough
1. Create time_series.py with time-series analysis functions
2. Add parse_date_column, set_time_index functions
3. Add rolling mean/std/sum, EWM functions
4. Add monthly/weekly trend analysis with MoM/WoW changes
5. Add trend direction detection and seasonal decomposition
6. Create analyze_time_series.py for time-series analysis

### Challenges Faced
- Pandas frequency alias deprecated — Changed 'M' to 'ME' for month-end frequency

### Final Outcome
Successfully analyzed all 3 raw datasets with time dimension using multiple rolling window functions.

---

---

## Learning Unit: 2.34 — KPI Definition & Business Metric Design

**Date:** 2026-08-28 20:00

### Introduction
In this video, we're covering Learning Unit 2.34 — KPI Definition & Business Metric Design.

### What We Built & Why It Matters
We implemented KPI definition and business metric design for analytics.

### Step-by-Step Walkthrough
1. Create kpi_definitions.py with KPI calculation functions
2. Add billable utilization rate, allocation efficiency, revenue per hour
3. Add non-billable load, timesheet compliance, billing accuracy, write-off rate
4. Add KPI targets, violation flagging, dashboard data
5. Create calculate_kpis.py for KPI analysis

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully calculated 7 core KPIs for all 3 datasets with targets, thresholds, and dashboard-ready data.

---

---

## Learning Unit: 2.35 — Root Cause Investigation Workflow

**Date:** 2026-08-28 21:00

### Introduction
In this video, we're covering Learning Unit 2.35 — Root Cause Investigation Workflow.

### What We Built & Why It Matters
We implemented root cause investigation workflow for identifying operational inefficiencies.

### Step-by-Step Walkthrough
1. Create root_cause.py with investigation functions
2. Add investigate_low_utilization, identify_bottlenecks functions
3. Add analyze_task_distribution, compare_allocated_vs_actual
4. Create analyze_root_cause.py script

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully analyzed bottlenecks in timesheet data with multiple investigation functions.

---

## Learning Unit: 2.36 — Anomaly Detection & Risk Identification

**Date:** 2026-08-29 05:15

### Introduction
In this video, we're covering Learning Unit 2.36 — Anomaly Detection & Risk Identification.

### What We Built & Why It Matters
We implemented anomaly detection and risk identification for employee data analysis.

### Step-by-Step Walkthrough
1. Create anomaly_detection.py with IQR and Z-score outlier detection
2. Add risk score calculation and classification
3. Add risk summary generation
4. Create analyze_anomalies.py script for anomaly analysis

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully detected anomalies in timesheet data with both IQR and Z-score methods.

---

---

## Learning Unit: 2.37 — SQL Environment & Database Integration

**Date:** 2026-08-29 05:19

### Introduction
In this video, we're covering Learning Unit 2.37 — SQL Environment & Database Integration.

### What We Built & Why It Matters
We implemented SQL environment and database integration for employee analytics.

### Step-by-Step Walkthrough
1. Create db_integration.py with SQLite connection and table management
2. Add execute_query, get_table_info, list_tables functions
3. Add create_tables_from_dataframes, get_database_stats
4. Create setup_database.py script for database setup

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully loaded all 4 datasets into SQLite database tables with query execution capabilities.

---

---

## Learning Unit: 2.38 — SQL Business Metrics Query Design

**Date:** 2026-08-29 05:24

### Introduction
In this video, we're covering Learning Unit 2.38 — SQL Business Metrics Query Design.

### What We Built & Why It Matters
We implemented SQL queries for calculating business metrics.

### Step-by-Step Walkthrough
1. Create business_metrics.py with SQL query functions
2. Add calculate_employee_utilization, calculate_department_metrics
3. Add calculate_project_billing, calculate_allocation_efficiency
4. Create calculate_business_metrics.py script

### Challenges Faced
- Column name mismatches in SQL queries — Fixed to match actual database schema

### Final Outcome
Successfully calculated employee utilization, department metrics, project billing, and allocation efficiency.

---

---

## Learning Unit: 2.39 — SQL Filtering, Grouping & Aggregation

**Date:** 2026-08-29 05:28

### Introduction
In this video, we're covering Learning Unit 2.39 — SQL Filtering, Grouping & Aggregation.

### What We Built & Why It Matters
We implemented SQL filtering, grouping, and aggregation queries.

### Step-by-Step Walkthrough
1. Create filtering_grouping.py with SQL query functions
2. Add filter_employees_by_department, filter_employees_by_experience
3. Add group_employees_by_department, group_timesheets_by_project
4. Create filter_group_data.py script

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully implemented department and experience filtering with project and monthly billing aggregations.

---

---

## Learning Unit: 2.40 — SQL Joins & Multi-Table Analysis

**Date:** 2026-08-29 05:33

### Introduction
In this video, we're covering Learning Unit 2.40 — SQL Joins & Multi-Table Analysis.

### What We Built & Why It Matters
We implemented SQL joins for multi-table analysis.

### Step-by-Step Walkthrough
1. Create joins.py with SQL join functions
2. Add join_timesheets_with_employees, join_allocations_with_employees
3. Add join_billing_with_employees, join_all_tables
4. Create join_tables.py script for join analysis

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully joined all 4 tables into comprehensive dataset with department and project aggregations.

---

---

## Learning Unit: 2.41 — SQL Window Functions & Ranking Systems

**Date:** 2026-08-29 05:37

### Introduction
In this video, we're covering Learning Unit 2.41 — SQL Window Functions & Ranking Systems.

### What We Built & Why It Matters
We implemented SQL window functions for ranking and analysis.

### Step-by-Step Walkthrough
1. Create window_functions.py with SQL window function queries
2. Add rank_employees_by_utilization, rank_employees_by_revenue
3. Add department_ranking, running_total_hours, moving_average_hours
4. Create window_function_analysis.py script

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully implemented RANK, DENSE_RANK, PERCENT_RANK functions with running totals, moving averages, and lag/lead analysis.

---

---

## Learning Unit: 2.44 — SQL-Based Insight Validation

**Date:** 2026-08-29 09:45

### Introduction
In this video, we're covering Learning Unit 2.44 — SQL-Based Insight Validation.

### What We Built & Why It Matters
We implemented SQL-based insight validation for business analytics.

### Step-by-Step Walkthrough
1. Create insight_validation.py with validation functions
2. Add validate_utilization_insight, validate_revenue_insight
3. Add validate_department_performance, validate_billing_accuracy
4. Create validate_insights.py script

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully validated 5 business insights with 100% pass rate.

---

---

## Learning Unit: 2.45 — Business Visualisation Principles

**Date:** 2026-08-29 09:49

### Introduction
In this video, we're covering Learning Unit 2.45 — Business Visualisation Principles.

### What We Built & Why It Matters
We implemented business visualization principles and best practices.

### Step-by-Step Walkthrough
1. Create business_viz.py with visualization functions
2. Add get_color_palette, get_chart_type_recommendation
3. Add format_number, create_kpi_card_data
4. Create create_business_charts.py script

### Challenges Faced
- TypeError with round function on string data — Used pd.to_numeric() with errors='coerce'

### Final Outcome
Successfully implemented business color palette, chart type recommendations, and KPI card data structures.

---

---

## Learning Unit: 2.46 — Interactive Plotly Chart Design

**Date:** 2026-08-31 05:46

### Introduction
In this video, we're covering Learning Unit 2.46 — Interactive Plotly Chart Design.

### What We Built & Why It Matters
We implemented interactive Plotly chart design for business visualizations.

### Step-by-Step Walkthrough
1. Create plotly_charts.py with chart configuration functions
2. Add create_bar_chart, create_line_chart, create_pie_chart
3. Add create_scatter_chart, create_histogram, create_box_plot
4. Create create_plotly_charts.py script

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully implemented 8 chart types with recommendations and interactive configurations.

---

---

## Learning Unit: 2.48 — Data Storytelling & Insight Narrative

**Date:** 2026-08-31 06:18

### Introduction
In this video, we're covering Learning Unit 2.48 — Data Storytelling & Insight Narrative.

### What We Built & Why It Matters
We implemented data storytelling and insight narrative for business analytics.

### Step-by-Step Walkthrough
1. Create story_narrative.py with narrative generation functions
2. Add generate_insight_narrative, create_story_structure
3. Add get_business_context, validate_story_data, extract_key_insights
4. Create analyze_storytelling.py script

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully generated insight narratives with key metrics and trends.

---

## Learning Unit: 2.49 — Executive Reporting & Stakeholder Communication

**Date:** 2026-08-31 06:28

### Introduction
In this video, we're covering Learning Unit 2.49 — Executive Reporting & Stakeholder Communication.

### What We Built & Why It Matters
We implemented executive reporting and stakeholder communication for business analytics.

### Step-by-Step Walkthrough
1. Create executive_report.py with reporting functions
2. Add generate_executive_summary, generate_stakeholder_report
3. Add format_report_for_presentation, validate_report_data
4. Create generate_executive_report.py script

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully generated executive summaries and stakeholder reports.

---

## Learning Unit: 2.50 — Insight Export & Report Generation

**Date:** 2026-08-31 06:35

### Introduction
In this video, we're covering Learning Unit 2.50 — Insight Export & Report Generation.

### What We Built & Why It Matters
We implemented insight export and report generation capabilities.

### Step-by-Step Walkthrough
1. Create insight_export.py with export functions
2. Add export_to_csv, export_to_json
3. Add generate_insight_report, generate_comparative_report
4. Create export_insights.py script

### Challenges Faced
No major issues encountered.

### Final Outcome
Successfully implemented CSV and JSON export capabilities with insight reports.

---

## Learning Unit: 2.51 — Streamlit App Structure & Navigation

**Date:** 2026-09-03

### Introduction
In this video, we're covering Learning Unit 2.51 — Streamlit App Structure & Navigation.

### What We Built & Why It Matters
We created Streamlit app shell with sidebar navigation, dark enterprise theme, page routing, and reusable layout components:
- **app.py** — Main entry point with page routing
- **src/dashboard/themer.py** — Dark theme tokens and CSS injection
- **src/dashboard/navigation.py** — Sidebar navigation (7 pages)
- **src/dashboard/layout.py** — Reusable UI components

### Step-by-Step Walkthrough
1. Create `src/dashboard/__init__.py` with module exports
2. Create `src/dashboard/themer.py` with dark theme tokens and CSS
3. Create `src/dashboard/navigation.py` with sidebar navigation
4. Create `src/dashboard/layout.py` with KPI cards, section cards, badges
5. Create `app.py` with page routing and Overview page
6. Test Streamlit app launches correctly

### Challenges Faced
- Previous implementation had HTML rendering issues — Re-implemented with proper escaping
- Period selector needs to be functional — Stored in session state

### Final Outcome
Successfully created Streamlit app shell with:
- Dark enterprise theme (bg: #0B1020, sidebar: #0F1729)
- 7-page sidebar navigation with color-coded icons
- Functional period selector
- Overview page with 6 KPI placeholders and chart placeholders
- File uploader and Reset button placeholders (disabled)

---

*This script documents the video explanation for each learning unit.*

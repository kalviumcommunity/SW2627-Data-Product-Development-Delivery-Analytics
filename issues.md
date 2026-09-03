# Issues Log — Employee Utilization Analytics

---

## Learning Unit: 2.11 — Development Environment & Workspace Setup

- **Issue:** #10
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 15:00
- **Status:** Completed

### Issues Faced

**Issue 1: Package Installation Timeout**
- **When:** 2026-08-27 15:05
- **Description:** Running `pip install` for all packages at once caused a timeout after 300 seconds.
- **Root Cause:** Combined download and installation of 11+ packages exceeded default timeout.
- **Solution:** Split installation into two batches. Verified all packages with import test.

**Issue 2: Module Not Found After Installation**
- **When:** 2026-08-27 15:10
- **Description:** `import matplotlib` failed with `ModuleNotFoundError`.
- **Root Cause:** Timeout interrupted installation before matplotlib was fully installed.
- **Solution:** Ran second `pip install` for missing packages. Verified with combined import test.

**Issue 3: Windows Activation Path**
- **When:** 2026-08-27 15:02
- **Description:** Initial attempts used `source venv/bin/activate` (Linux path).
- **Root Cause:** Windows uses different path structure for venv activation.
- **Solution:** Used `source venv/Scripts/activate` for Windows bash environments.

---

## Learning Unit: 2.12 — GitHub Repository & Team Workflow Setup

- **Issue:** #11
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 16:00
- **Status:** Completed

### Issues Faced

**Issue 1: GitHub Labels Don't Exist**
- **When:** 2026-08-27 16:15
- **Description:** `gh issue create --label "feature,data-pipeline"` failed with "label not found".
- **Root Cause:** Repository doesn't have pre-configured labels.
- **Solution:** Created issues without labels first. Labels can be added via GitHub web interface.

**Issue 2: Branch Protection Blocks Direct Merge**
- **When:** 2026-08-27 16:30
- **Description:** `gh pr merge 64 --merge` failed with "base branch policy prohibits the merge".
- **Root Cause:** Repository has branch protection rules.
- **Solution:** Used `--admin` flag to merge with administrator privileges.

**Issue 3: Local Branches Not Visible After Merge**
- **When:** 2026-08-27 16:45
- **Description:** After merging and deleting local branches, `git branch` only shows `main`.
- **Root Cause:** Deleted local branches don't appear in `git branch` but exist on GitHub.
- **Solution:** Used `git branch -a` to see all branches. Recreated branches with new commits.

---

## Learning Unit: 2.13 — Python Data Workflow Foundations

- **Issue:** #12
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 17:00
- **Status:** Completed

### Issues Faced

No major issues encountered. Module created successfully with proper structure.

---

## Learning Unit: 2.14 — Dataset Intake & Source Validation

- **Issue:** #13
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 17:30
- **Status:** Completed

### Issues Faced

No major issues encountered. Validation module created and tested.

---

## Learning Unit: 2.15 — CSV & JSON Data Ingestion

- **Issue:** #14
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 18:00
- **Status:** Completed

### Issues Faced

**Issue 1: Emoji Encoding Issues on Windows**
- **When:** 2026-08-27 18:15
- **Description:** Scripts with emoji characters failed with `UnicodeEncodeError` on Windows.
- **Root Cause:** Windows console uses cp1252 encoding which doesn't support emoji characters.
- **Solution:** Replaced emoji characters with ASCII alternatives ([PASS], [WARN], [ERROR]).

---

## Learning Unit: 2.16 — Dataset Profiling & Quality Assessment

- **Issue:** #15
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 19:00
- **Status:** Completed

### Issues Faced

No major issues encountered. Profiling module created and tested.

---

## Learning Unit: 2.17 — Data Dictionary & Business Context Mapping

- **Issue:** #16
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 19:30
- **Status:** Completed

### Issues Faced

No major issues encountered. Data dictionary module created and tested.

---

## Learning Unit: 2.18 — Missing Value Detection & Imputation

- **Issue:** #17
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 20:00
- **Status:** Completed

### Issues Faced

No major issues encountered. Missing values module created and tested.

---

## Learning Unit: 2.19 — Data Type Enforcement & Standardisation

- **Issue:** #18
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 20:30
- **Status:** Completed

### Issues Faced

No major issues encountered. Type enforcement module created and tested.

---

## Learning Unit: 2.20 — Duplicate Detection & Record Deduplication

- **Issue:** #19
- **Assignee:** arbinbiswal
- **Date:** 2026-08-27 21:00
- **Status:** Completed

### Issues Faced

No major issues encountered. Deduplication module created and tested.

---

## Learning Unit: 2.21 — String Cleaning & Text Normalisation

- **Issue:** #20
- **Assignee:** arbinbiswal
- **Date:** 2026-08-28 10:00
- **Status:** Completed

### Issues Faced

No major issues encountered. String normalization module created and tested.

---

## Learning Unit: 2.22 — Date & Time Transformation Pipeline

- **Issue:** #21
- **Assignee:** arbinbiswal
- **Date:** 2026-08-28 11:00
- **Status:** Completed

### Issues Faced

**Issue 1: infer_datetime_format parameter not available**
- **When:** 2026-08-28 11:15
- **Description:** `parse_dates()` failed with `infer_datetime_format` parameter error.
- **Root Cause:** This pandas version doesn't support the `infer_datetime_format` parameter.
- **Solution:** Removed the parameter and used default `to_datetime()` behavior.

---

---

## Learning Unit: 2.24 — Data Consistency & Validation Rules

- **Issue:** #23
- **Assignee:** prabdeep2005
- **Date:** 2026-08-28 14:00
- **Status:** Completed

### Issues Faced

No major issues encountered. Consistency rules module created and tested.

---

## Learning Unit: 2.25 — Multi-Source Merging & Join Validation

- **Issue:** #24
- **Assignee:** prabdeep2005
- **Date:** 2026-08-28 15:00
- **Status:** Completed

### Issues Faced

No major issues encountered. Merging module created and tested.

---

## Learning Unit: 2.26 — Feature Engineering & Derived Business Columns

- **Issue:** #25
- **Assignee:** prabdeep2005
- **Date:** 2026-08-28 16:00
- **Status:** Completed

### Issues Faced

No major issues encountered. Feature engineering module created and tested.

---

## Learning Unit: 2.28 — Distribution Analysis for Business Trends

- **Issue:** #26
- **Assignee:** prabdeep2005
- **Date:** 2026-08-28 17:00
- **Status:** Completed

### Issues Faced

No major issues encountered. Distribution analysis module created and tested.

---

## Learning Unit: 2.30 — GroupBy Aggregation & Segment Insights

- **Issue:** #28
- **Assignee:** prabdeep2005
- **Date:** 2026-08-28 18:00
- **Status:** Completed

### Issues Faced

No major issues encountered. GroupBy aggregation module created and tested.

---

## Learning Unit: 2.31 — Time-Series Trend & Rolling Metrics

- **Issue:** #29
- **Assignee:** prabdeep2005
- **Date:** 2026-08-28 19:00
- **Status:** Completed

### Issues Faced

**Issue 1: Pandas frequency alias deprecated**
- **When:** 2026-08-28 19:15
- **Description:** `resample('M')` failed with "Invalid frequency: M. Please use 'ME' instead."
- **Root Cause:** Newer pandas version deprecated 'M' alias for month-end frequency.
- **Solution:** Changed to 'ME' for month-end frequency.

---

---

## Learning Unit: 2.34 — KPI Definition & Business Metric Design

- **Issue:** #30
- **Assignee:** prabdeep2005
- **Date:** 2026-08-28 20:00
- **Status:** Completed

### Issues Faced

No major issues encountered. KPI definition module created and tested.

---

---

## Learning Unit: 2.35 — Root Cause Investigation Workflow

- **Issue:** #55
- **Assignee:** prabdeep2005
- **Date:** 2026-08-28 21:00
- **Status:** Completed

### Issues Faced

No major issues encountered. Root cause investigation module created and tested.

---

## Learning Unit: 2.36 — Anomaly Detection & Risk Identification

- **Issue:** #31
- **Assignee:** arbinbiswal
- **Date:** 2026-08-29 05:15
- **Status:** Completed

### Issues Faced

No major issues encountered. Anomaly detection module created and tested.

---

---

## Learning Unit: 2.37 — SQL Environment & Database Integration

- **Issue:** #32
- **Assignee:** arbinbiswal
- **Date:** 2026-08-29 05:19
- **Status:** Completed

### Issues Faced

No major issues encountered. SQL database integration module created and tested.

---

---

## Learning Unit: 2.38 — SQL Business Metrics Query Design

- **Issue:** #33
- **Assignee:** arbinbiswal
- **Date:** 2026-08-29 05:24
- **Status:** Completed

### Issues Faced

**Issue 1: Column name mismatches in SQL queries**
- **When:** 2026-08-29 05:22
- **Description:** SQL queries failed with "no such column" errors for hours_worked, hours_allocated, and amount.
- **Root Cause:** Used incorrect column names in SQL queries.
- **Solution:** Fixed column names to match actual database schema (billable_hours, allocated_hours, billed_amount).

---

---

## Learning Unit: 2.39 — SQL Filtering, Grouping & Aggregation

- **Issue:** #34
- **Assignee:** prabdeep2005
- **Date:** 2026-08-29 05:28
- **Status:** Completed

### Issues Faced

No major issues encountered. Filtering and grouping module created and tested.

---

---

## Learning Unit: 2.40 — SQL Joins & Multi-Table Analysis

- **Issue:** #35
- **Assignee:** prabdeep2005
- **Date:** 2026-08-29 05:33
- **Status:** Completed

### Issues Faced

No major issues encountered. SQL joins module created and tested.

---

---

## Learning Unit: 2.41 — SQL Window Functions & Ranking Systems

- **Issue:** #36
- **Assignee:** prabdeep2005
- **Date:** 2026-08-29 05:37
- **Status:** Completed

### Issues Faced

No major issues encountered. Window functions module created and tested.

---

---

## Learning Unit: 2.44 — SQL-Based Insight Validation

- **Issue:** #38
- **Assignee:** arbinbiswal
- **Date:** 2026-08-29 09:45
- **Status:** Completed

### Issues Faced

No major issues encountered. Insight validation module created and tested.

---

---

## Learning Unit: 2.45 — Business Visualisation Principles

- **Issue:** #39
- **Assignee:** arbinbiswal
- **Date:** 2026-08-29 09:49
- **Status:** Completed

### Issues Faced

**Issue 1: TypeError with round function on string data**
- **When:** 2026-08-29 09:47
- **Description:** `get_business_insights_from_data()` failed with "type str doesn't define __round__ method".
- **Root Cause:** Column contained string values that couldn't be rounded.
- **Solution:** Convert to numeric using `pd.to_numeric()` with `errors='coerce'` before rounding.

---

---

## Learning Unit: 2.46 — Interactive Plotly Chart Design

- **Issue:** #40
- **Assignee:** prabdeep2005
- **Date:** 2026-08-31 05:46
- **Status:** Completed

### Issues Faced

No major issues encountered. Plotly chart module created and tested.

---

## Learning Unit: 2.48 — Data Storytelling & Insight Narrative

- **Issue:** #42
- **Assignee:** prabdeep2005
- **Date:** 2026-08-31 06:18
- **Status:** Completed

### Issues Faced

No major issues encountered. Data storytelling module created and tested.

---

## Learning Unit: 2.49 — Executive Reporting & Stakeholder Communication

- **Issue:** #43
- **Assignee:** prabdeep2005
- **Date:** 2026-08-31 06:28
- **Status:** Completed

### Issues Faced

No major issues encountered. Executive reporting module created and tested.

---

## Learning Unit: 2.50 — Insight Export & Report Generation

- **Issue:** #44
- **Assignee:** prabdeep2005
- **Date:** 2026-08-31 06:35
- **Status:** Completed

### Issues Faced

No major issues encountered. Insight export module created and tested.

---

## Learning Unit: 2.51 — Streamlit App Structure & Navigation (REVERTED)

- **Issue:** #45
- **Assignee:** arbinbiswal
- **Date:** 2026-09-01 17:00
- **Status:** Reverted (PR #100)

### Issues Faced

**Issue 1: HTML rendering issues in navigation.py**
- **When:** 2026-09-01
- **Description:** Escaped quote characters in HTML strings caused broken rendering in sidebar navigation.
- **Root Cause:** Improper HTML string escaping in navigation.py.
- **Solution:** Reverted and re-implemented with properly escaped HTML strings.

---

## Learning Unit: 2.51 — Streamlit App Structure & Navigation (Re-implemented)

- **Issue:** #45
- **Assignee:** arbinbiswal
- **Date:** 2026-09-03
- **Status:** Completed (PR #101 pending)

### Issues Faced

No major issues encountered. Fresh implementation with proper HTML escaping.

### What was implemented
- Streamlit app shell with sidebar navigation, dark enterprise theme, page routing
- Reusable layout components: KPI cards, section cards, status badges
- Functional period selector (stored in session state)
- Overview page with 6 KPI placeholders and chart placeholders

### Key files created
- `app.py` — Main entry point with page routing
- `src/dashboard/__init__.py` — Module exports
- `src/dashboard/themer.py` — Dark theme tokens and CSS injection
- `src/dashboard/navigation.py` — Sidebar navigation (7 pages)
- `src/dashboard/layout.py` — Reusable UI components

---

*This log tracks all issues encountered during development. Update after each LU completion.*

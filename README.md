# Employee Utilization Analytics

Data product for identifying operational inefficiencies that reduce billable utilization.

## Setup

```bash
# Clone the repository
git clone https://github.com/kalviumcommunity/SW2627-Data-Product-Development-Delivery-Analytics.git
cd SW2627-Data-Product-Development-Delivery-Analytics

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Run the application

The dashboard and API run as separate local processes:

```bash
# Terminal 1
uvicorn src.api.main:app --reload --port 8000

# Terminal 2
streamlit run app.py
```

The API health check is available at `http://127.0.0.1:8000/health`.

The application database is created at `data/app.db` on API startup. It can be
opened with DB Browser for SQLite after stopping the local application.

## Data refresh

Run a refresh manually with:

```bash
python scripts/refresh_data.py
```

The refresh loads `data/raw/employee_master_raw.csv`, `timesheets_raw.csv`,
`allocations_raw.csv`, and `billing_raw.csv`. It preserves application users
and work assignments, upserts employee lookup records, and records each run in
the `refresh_runs` table.

For the agreed local schedule, create a Windows Task Scheduler task that runs
daily at 02:00 using `venv\Scripts\python.exe scripts\refresh_data.py` from
the project directory. The API also exposes Admin-only `POST /refresh` and
authenticated `GET /refresh/status` endpoints.

Run the automated checks from the project root with:

```bash
pytest -q
```

---

*Detailed documentation will be added upon project completion.*

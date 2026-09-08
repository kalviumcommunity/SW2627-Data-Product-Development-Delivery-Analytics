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

---

*Detailed documentation will be added upon project completion.*

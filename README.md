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

## Running the Streamlit App
```bash
# From the project root
venv\Scripts\activate
streamlit run app.py
```

The app opens at `http://localhost:8501` with a dark enterprise interface featuring:
- Sidebar navigation (Overview, Workforce, Work Planning, Capacity & Utilization, Team Analytics, Insights/Alerts, Reports)
- Top header with period selector and user profile
- File upload functionality (CSV/JSON)
- KPI cards and workforce analytics dashboards

---

*Detailed documentation will be added upon project completion.*
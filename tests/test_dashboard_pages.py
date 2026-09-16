import ast
from pathlib import Path

import pytest


APP_PATH = Path(__file__).parents[1] / "app.py"


def _app_source():
    return APP_PATH.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "page_key",
    ["overview", "workforce", "work_planning", "capacity", "team_analytics", "insights", "reports"],
)
def test_every_dashboard_page_has_a_renderer_and_is_registered(page_key):
    tree = ast.parse(_app_source())
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

    assert f"render_{page_key}" in functions
    assert f'"{page_key}":' in _app_source()


def test_dashboard_contains_empty_states_and_report_download():
    source = _app_source()

    assert "render_placeholder" in source
    assert "st.download_button" in source
    assert "Upload datasets to generate reports" in source


def test_login_form_supports_enter_submission():
    auth_source = (APP_PATH.parent / "src" / "dashboard" / "auth.py").read_text(encoding="utf-8")

    assert 'st.form("login_form", enter_to_submit=True)' in auth_source


def test_dashboard_theme_uses_streamlit_theme_and_chart_template():
    app_source = _app_source()
    themer_source = (APP_PATH.parent / "src" / "dashboard" / "themer.py").read_text(encoding="utf-8")
    theme_config = (APP_PATH.parent / ".streamlit" / "config.toml").read_text(encoding="utf-8")

    assert "get_plotly_template" in app_source
    assert '"bg_app": "transparent"' in themer_source
    assert 'currentColor' in themer_source
    assert 'st.get_option("theme.base")' in themer_source
    assert 'data-testid="stWidgetLabel"' in themer_source
    assert 'data-testid="stMetricValue"' in themer_source
    assert 'section[data-testid="stSidebar"] [role="radiogroup"] label *' in themer_source
    assert 'data-testid="stMainBlockContainer"' in themer_source
    assert '.stMarkdown li' in themer_source
    assert '[theme.dark]' in theme_config
    assert 'backgroundColor = "#000000"' in theme_config
    assert 'textColor = "#FFFFFF"' in theme_config

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

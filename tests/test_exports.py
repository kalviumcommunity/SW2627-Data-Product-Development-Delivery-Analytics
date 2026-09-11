import json

import pandas as pd

from src.export.insight_export import export_to_csv, export_to_json
from src.output.export_data import export_csv, export_json


def test_csv_exports_preserve_columns_without_index(tmp_path):
    frame = pd.DataFrame({"employee_id": ["E1"], "hours": [8.5]})

    csv_path = export_csv(frame, str(tmp_path / "output.csv"))
    insight_path = export_to_csv(frame, str(tmp_path / "insight.csv"))

    assert pd.read_csv(csv_path).to_dict("records") == frame.to_dict("records")
    assert pd.read_csv(insight_path["file_path"]).columns.tolist() == ["employee_id", "hours"]


def test_json_exports_support_records_and_metadata(tmp_path):
    frame = pd.DataFrame({"employee_id": ["E1"], "hours": [8.5]})

    json_path = export_json(frame, str(tmp_path / "output.json"))
    insight_path = export_to_json(frame, str(tmp_path / "insight.json"))

    assert json.loads((tmp_path / "output.json").read_text()) == [{"employee_id": "E1", "hours": 8.5}]
    assert json.loads((tmp_path / "insight.json").read_text()) == [{"employee_id": "E1", "hours": 8.5}]
    assert json_path.endswith("output.json")
    assert insight_path["rows_exported"] == 1

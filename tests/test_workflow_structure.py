from pathlib import Path


WORKFLOW_PATH = Path(__file__).parents[1] / ".github" / "workflows" / "pipeline.yml"


def test_pipeline_workflow_uses_pr_publishing_and_failure_permissions():
    source = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "contents: write" in source
    assert "pull-requests: write" in source
    assert "issues: write" in source
    assert "peter-evans/create-pull-request@v7" in source
    assert "branch: pipeline-autorefresh" in source
    assert "base: main" in source
    assert "labels: ['pipeline-failure']" in source
    assert "git push" not in source


def test_failure_notification_is_failure_only():
    source = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "needs: run-pipeline" in source
    assert "if: failure()" in source
    assert "issues.create" in source

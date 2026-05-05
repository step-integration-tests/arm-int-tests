import os
import pytest
from analyze_agent_metrics import analyze_metrics

def test_analyze_agent_metrics():
    metrics_file = ".github/scripts/agent_pidstat.log"

    assert os.path.exists(metrics_file), "metrics file should exist"

    report = analyze_metrics(metrics_file)

    assert report['Peak CPU %'] > 1.0, f"Expected peak CPU > 1, got {report['Peak CPU %']}"
    assert report['Average Memory MB'] > 1.0, f"Expected average memory > 1 MB, got {report['Average Memory MB']}"
    assert report['Average Disk Read KB/s'] >= 0, f"Expected average disk read >= 0, got {report['Average Disk Read KB/s']}"
    assert report['Average Disk Write KB/s'] >= 0, f"Expected average disk write >= 0, got {report['Average Disk Write KB/s']}"
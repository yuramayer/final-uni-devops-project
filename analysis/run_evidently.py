import json
from pathlib import Path

import pandas as pd

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric

LOG_FILE = Path("data/logs/predictions.jsonl")
OUTPUT = Path("analysis/report.html")


def load():
    rows = []
    for line in LOG_FILE.open():
        rows.append(json.loads(line))
    df = pd.DataFrame(rows)
    f = df["features"].apply(pd.Series)
    df = pd.concat([df.drop(columns=["features"]), f], axis=1)
    return df


def main():
    df = load()

    if len(df) < 50:
        print("not enough data")
        return

    ref = df.head(200)
    cur = df.tail(200)

    column_mapping = ColumnMapping(
        numerical_features=["feature_1", "feature_2"],
        prediction="probability",
    )

    report = Report(
        metrics=[
            DatasetDriftMetric()
        ]
    )

    report.run(
        reference_data=ref,
        current_data=cur,
        column_mapping=column_mapping
    )

    report.save_html("report.html")

    print("Saved:", OUTPUT)


if __name__ == "__main__":
    main()
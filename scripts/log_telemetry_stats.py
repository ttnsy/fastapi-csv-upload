from pathlib import Path

import pandas as pd


def aggregate_perf_logs(log_dir="logs"):
    files = list(Path(log_dir).glob("*.jsonl"))
    if not files:
        raise FileNotFoundError(f"No JSONL log files found in {log_dir}")

    df = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
    df = df[df.logger == "telemetry"]
    df["date"] = pd.to_datetime(df.timestamp).dt.date
    summary = (
        df.groupby(["date", "path"])["duration_ms"]
        .agg(count="count", avg_duration_ms="mean")
        .reset_index()
        .rename(columns={"path": "endpoint"})
    )

    return summary


if __name__ == "__main__":
    df_summary = aggregate_perf_logs()
    print(df_summary)

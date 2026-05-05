import os
import pandas as pd
import traceback

def analyze_metrics(metrics_file: str) -> dict:
    if not os.path.exists(metrics_file) or os.path.getsize(metrics_file) == 0:
        raise ValueError("No metrics captured. Skipping analysis.")

    # Debug: Print first 20 lines
    with open(metrics_file, 'r') as f:
        print("\n--- First 20 lines of the metrics file ---")
        for i, line in enumerate(f):
            print(line.rstrip())
            if i >= 100:
                break
        print("--- End of first 20 lines ---\n")

    # 🛠 NEW: Pre-clean the file
    lines = []
    with open(metrics_file, 'r') as f:
        for line in f:
            if not line.startswith("#") and not line.startswith("Linux") and line.strip():
                lines.append(line)

    from io import StringIO
    if not lines:
        raise ValueError("No valid data rows after cleaning.")

    df = pd.read_csv(
        StringIO(''.join(lines)),
        sep=r'\s+',
        engine='python',
        header=None,
        names=['Time', 'UID', 'PID', '%usr', '%system', '%guest', '%wait', '%CPU', 'CPU',
               'minflt/s', 'majflt/s', 'VSZ', 'RSS', '%MEM', 'kB_rd/s', 'kB_wr/s', 'kB_ccwr/s', 'iodelay', 'Command']
    )

    expected_cols = ['%usr', '%system', '%guest', '%CPU', 'RSS', 'kB_rd/s', 'kB_wr/s']
    if not all(col in df.columns for col in expected_cols):
        raise ValueError(f"Expected columns not found. Found columns: {df.columns.tolist()}")

    for col in expected_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['%CPU', 'RSS', 'kB_rd/s', 'kB_wr/s'])

    df['kB_rd/s'] = df['kB_rd/s'].apply(lambda x: max(x, 0))
    df['kB_wr/s'] = df['kB_wr/s'].apply(lambda x: max(x, 0))

    if df.empty:
        raise ValueError("No valid metrics data after cleaning.")

    report = {
        'Average CPU %': df['%CPU'].mean(),
        'Peak CPU %': df['%CPU'].max(),
        'Average Memory MB': df['RSS'].mean() / 1024,
        'Peak Memory MB': df['RSS'].max() / 1024,
        'Average Disk Read KB/s': df['kB_rd/s'].mean(),
        'Peak Disk Read KB/s': df['kB_rd/s'].max(),
        'Average Disk Write KB/s': df['kB_wr/s'].mean(),
        'Peak Disk Write KB/s': df['kB_wr/s'].max(),
    }
    return report

if __name__ == "__main__":
    try:
        report = analyze_metrics('metrics/agent_pidstat.log')
        os.makedirs('metrics', exist_ok=True)
        with open('metrics/agent_resource_report.txt', 'w') as f:
            for key, value in report.items():
                f.write(f"{key}: {value:.2f}\n")
    except Exception as e:
        print(f"Analysis failed to analyze agent metrics: {e}")
        traceback.print_exc()
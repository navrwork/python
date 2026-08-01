import pandas as pd
import numpy as np
import glob
import os
from collections import defaultdict

def analyze_etf(df, etf_name):
    df = df.sort_values("DATE")

    # --- Annualized Volatility ---
    df["Return"] = df["CLOSE"].pct_change()
    daily_vol = df["Return"].std()
    annual_vol = daily_vol * np.sqrt(252)

    # --- Rolling Returns ---
    rolling_return_1y = np.nan
    rolling_return_6m = np.nan

    if len(df) >= 252:
        rolling_return_1y = (df["CLOSE"].iloc[-1] / df["CLOSE"].iloc[-252] - 1)
    if len(df) >= 126:
        rolling_return_6m = (df["CLOSE"].iloc[-1] / df["CLOSE"].iloc[-126] - 1)

    # --- 52W Low & High ---
    low_val = df["52W L"].min()
    low_date = df.loc[df["52W L"].idxmin(), "DATE"]

    high_val = df["52W H"].max()
    high_date = df.loc[df["52W H"].idxmax(), "DATE"]

    # --- Bounce-back Strength ---
    bounce_days = (high_date - low_date).days
    if bounce_days <= 90:
        bounce_strength = "Strong bounce"
    elif bounce_days <= 180:
        bounce_strength = "Decent bounce"
    else:
        bounce_strength = "Poor bounce"

    # --- Risk-adjusted Score (using 6M return fallback) ---
    risk_score = None
    if not np.isnan(rolling_return_6m) and annual_vol > 0:
        risk_score = rolling_return_6m / annual_vol

    return {
        "ETF name": etf_name,
        "52w high date": high_date.date(),
        "52w high price": round(high_val, 2),
        "52w low date": low_date.date(),
        "52w low price": round(low_val, 2),
        "bounce days": bounce_days,
        "Bounce-back Strength": bounce_strength,
        "Annualized Volatility (%)": round(annual_vol * 100, 2),
        "1-Year Rolling Return (%)": round(rolling_return_1y * 100, 2) if not np.isnan(rolling_return_1y) else None,
        "6-Month Rolling Return (%)": round(rolling_return_6m * 100, 2) if not np.isnan(rolling_return_6m) else None,
        "Risk-adjusted Score": round(risk_score, 2) if risk_score is not None else None
    }

def analyze_folder(folder_path, output_file="etf-summary.csv"):
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    etf_groups = defaultdict(list)

    # Group files by ETF name (strip date ranges from filename)
    for file in csv_files:
        base = os.path.basename(file).replace(".csv", "")
        # Example: "Quote-Equity-ALPHA-EQ-01-08-2025-01-08-2026"
        etf_name = "-".join(base.split("-")[2:4])  # Extract ALPHA-EQ, BANKBEES-EQ, etc.
        etf_groups[etf_name].append(file)

    results = []
    for etf_name, files in etf_groups.items():
        # Merge all files for this ETF
        dfs = [pd.read_csv(f, parse_dates=["DATE"]) for f in files]
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset="DATE")  # avoid overlap
        results.append(analyze_etf(combined_df, etf_name))

    summary_df = pd.DataFrame(results)
    summary_df.to_csv(output_file, index=False)
    print(f"Summary saved to {output_file}")
    print(summary_df)

# Example usage: replace with your folder path
analyze_folder("C:\\Users\\rnava\\Documents\\nr\\etf\\hist-data\\past-1yr-data-aug2026")

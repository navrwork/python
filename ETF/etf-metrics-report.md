# ETF Metrics Report

This script combines ETF historical-price CSV files, calculates performance and
risk metrics, and writes one summary row per ETF.

## Requirements

Use Python 3. Install the required packages in the active environment:

```powershell
python -m pip install pandas numpy
```

## Prepare the input files

You can get a copy of source data from [exchange-traded-funds-etf](https://www.nseindia.com/market-data/exchange-traded-funds-etf) page.

Put the historical CSV files in one folder. Each file must contain at the least these columns:


```text
DATE,CLOSE,52W L,52W H
```

`DATE` must contain dates that pandas can parse. The filename should follow the
same pattern as the source files, for example:

```text
Quote-Equity-BANKBEES-EQ-01-08-2025-01-08-2026.csv
```

The script identifies the ETF from the third and fourth hyphen-separated parts
of the filename (Sample file name taken from nseindia.com: `Quote-Equity-NIFTYBEES-EQ-01-08-2025-01-08-2026.csv`).

Note: 
* The position or order of the columns doesn't matter. 
* The file downloaded from the nseindia website can be used as is. 

## Run the script

The input folder is currently set at the bottom of
`etf-metrics-report.py`:

```python
analyze_folder(
	r"C:\path\to\your\historical-data-folder"
)
```

Change that path to the folder containing your CSV files, then run:

```powershell
python etf_metrics_report.py
```

The script creates `etf-summary.csv` in the current working directory and also
prints the summary table to the terminal. To use a different output filename,
change the call to:

```python
analyze_folder(
	r"C:\path\to\your\historical-data-folder",
	output_file="etf-summary-past-1yr-aug2026.csv"
)
```

## Output columns

The generated summary includes:

- ETF name
- 52-week high and low dates and prices
- Number of days between the low and high
- Bounce-back Strength (`Strong bounce`, `Decent bounce`, or `Poor bounce`)
- Annualized volatility
- 1-year and 6-month rolling returns
- Risk-adjusted score

Rolling metrics are blank when the input does not contain enough trading days.

# COMPLETE GUIDE TO USING THE PYTHON ANALYZER

## QUICK START (30 seconds)

### Option 1: Copy-Paste (Fastest)
1. Copy code from `gold_etf_minimal.py`
2. Paste into Python IDE or Jupyter notebook
3. Change filename if needed
4. Run!

### Option 2: Run Directly (Very Easy)
bash
python gold_etf_analyzer_standalone.py

### Option 3: Import as Module (Most Professional)
```python
from gold_etf_analyzer import GoldETFAnalyzer

analyzer = GoldETFAnalyzer('SBIG-ETF-Stock-Price-History.csv')
analyzer.calculate_moving_averages()
analyzer.analyze_all_years()
analyzer.print_summary_table()
analyzer.export_to_csv('results.csv')
```

## FILE DESCRIPTIONS

### 1. gold_etf_analyzer.py (Class-Based)
**Type:** Production-grade code
**Size:** ~400 lines
**Style:** Object-Oriented Programming (OOP)
**Best For:** Large projects, reusable components

**Key Components:**
- `GoldETFAnalyzer` class
- 8 public methods
- Full documentation
- Professional structure

**When to Use:**
- Building a larger application
- Need reusability
- Want clean, maintainable code
- Planning future enhancements

### 2. gold_etf_analyzer_standalone.py (Function-Based)
**Type:** Learning/scripting code
**Size:** ~250 lines
**Style:** Procedural (Functions only)
**Best For:** Learning, quick scripts, copy-paste

**Key Components:**
- Pure functions
- Clear flow
- Easy to understand
- Good for beginners

**When to Use:**
- Learning Python
- One-off analysis
- Quick prototyping
- Teaching others

### 3. gold_etf_minimal.py (Minimal)
**Type:** Quick analysis
**Size:** ~50 lines
**Style:** Inline code
**Best For:** Quick analysis, snippets, examples

**Key Components:**
- All code in main()
- No functions/classes
- Straightforward logic
- Fastest to understand

**When to Use:**
- Need instant results
- Copy-paste into notebook
- Teaching data science basics
- Rapid prototyping

## INSTALLATION

Step 1: Install Python (if not already installed)
- Download from python.org
- Version 3.7 or higher recommended

Step 2: Install required packages
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install pandas numpy
```

## HOW TO USE

### Method 1: Command Line (Easiest)
```bash
cd /path/to/scripts
python gold_etf_analyzer_standalone.py
```

### Method 2: Jupyter Notebook
1. Open Jupyter: `jupyter notebook`
2. Create new Python 3 notebook
3. Paste code from `gold_etf_minimal.py`
4. Run cell (Shift + Enter)

### Method 3: Python IDE (PyCharm, VS Code)
1. Open your IDE
2. Create new Python file
3. Paste code
4. Run (F5 or Run button)

### Method 4: Python Interactive Shell
```python
>>> import pandas as pd
>>> exec(open('gold_etf_analyzer_standalone.py').read())
```

## WHAT EACH SCRIPT OUTPUTS

### Console Output
- Year-by-year analysis
- Summary table with percentages
- Key statistics
- Price information

### CSV File Output
- All metrics in spreadsheet format
- Easy to import to Excel
- Good for further analysis

### Dataframe (OOP Version)
- Access results as Python dataframe
- Further programmatic processing

## CUSTOMIZATION GUIDE

### Change Input File
```python
# Original
df = pd.read_csv('SBIG-ETF-Stock-Price-History.csv')

# Your file
df = pd.read_csv('your_gold_etf_data.csv')
```

### Change Output Filename
```python
# Original
results_df.to_csv('analysis_results.csv', index=False)

# Your name
results_df.to_csv('my_custom_results.csv', index=False)
```

### Add Additional Moving Averages
```python
# Add 20-DMA
df['SMA_20'] = df['Price'].rolling(20).mean()

# Add 30-DMA
df['SMA_30'] = df['Price'].rolling(30).mean()

# Then analyze like the others
```

### Filter by Year Range
```python
# Analyze only 2020-2025
start_year = 2020
results = []
for year in sorted(df['Year'].unique()):
    if year >= start_year:
        result = analyze_year(df, year)
        results.append(result)
```

## UNDERSTANDING THE OUTPUT

### What is "Percent Below 50-DMA"?
- Percentage of trading days price was below 50-DMA
- Higher % = More volatility
- Lower % = Stronger trend

### What is "Avg Fall"?
- Average percentage price falls below moving average
- When price crosses below MA, how far down on average?
- Larger = Bigger corrections

### What is "Max Fall"?
- Maximum percentage price ever fell below MA in that year
- Worst-case scenario
- Good for risk assessment

## EXAMPLE INTERPRETATION

```
Year 2024:
  50-DMA: 33.87%     ← Price below 50-DMA about 1/3 of trading days
  100-DMA: 12.50%    ← Price below 100-DMA about 1/8 of trading days
  200-DMA: 0.00%     ← Price NEVER below 200-DMA = Strong uptrend

Year 2021:
  50-DMA: 55.65%     ← Very volatile, below half the time
  100-DMA: 55.65%    ← Same volatility at both levels
  200-DMA: 77.02%    ← Major market stress, mostly below long-term MA
```

## TROUBLESHOOTING

### Error: "FileNotFoundError"
- Check CSV file is in same directory as script
- Or provide full path: '/Users/myname/data/SBIG-ETF-Stock-Price-History.csv'

### Error: "KeyError: 'Price'"
- Check column names in CSV
- Should be: Date, Price, Open, High, Low, Vol., Change %

### Error: "ModuleNotFoundError: No module named 'pandas'"
- Install pandas: pip install pandas

### Script runs but no output
- Check if file is in same directory
- Check CSV file format
- Add print statements to debug

## ADVANCED TIPS

### Calculate CAGR
```python
start_price = df['Price'].iloc[0]
end_price = df['Price'].iloc[-1]
years = (df['Date'].max() - df['Date'].min()).days / 365.25
cagr = ((end_price / start_price) ** (1 / years) - 1) * 100
print(f"CAGR: {cagr:.2f}%")
```

### Find Worst Day Below MA
```python
year_200 = year_data.dropna(subset=['SMA_200'])
below_200 = year_200[year_200['Price'] < year_200['SMA_200']].copy()
below_200['Fall'] = ((below_200['SMA_200'] - below_200['Price']) / below_200['SMA_200']) * 100
worst_day = below_200.loc[below_200['Fall'].idxmax()]
```

### Export to Excel with Formatting
```python
with pd.ExcelWriter('results.xlsx', engine='openpyxl') as writer:
    results_df.to_excel(writer, sheet_name='Analysis')
```

## PERFORMANCE NOTES

- Analysis of 2,500 trading days: < 1 second
- CSV export: < 1 second
- Total runtime: ~2 seconds

## FILE ORGANIZATION

Recommended folder structure:
```
gold_etf_analysis/
├── gold_etf_analyzer.py
├── gold_etf_analyzer_standalone.py
├── gold_etf_minimal.py
├── example_usage.py
├── SBIG-ETF-Stock-Price-History.csv
├── requirements.txt
├── README.md
├── results.csv (generated)
└── analysis_results.csv (generated)
```

## NEXT STEPS

1. **Try Minimal Version First**
   - Understand the output
   - Get comfortable with data

2. **Try Standalone Version**
   - Learn how functions work
   - Customize calculations

3. **Use OOP Version**
   - Integrate into larger project
   - Build on the foundation

## SUPPORT & HELP

If code doesn't work:
1. Check Python version: `python --version`
2. Check pandas installed: `python -c "import pandas"`
3. Check CSV file format
4. Check file path is correct
5. Read error message carefully

## LICENSE

All code is free to use, modify, and distribute.
No attribution required (but appreciated!).

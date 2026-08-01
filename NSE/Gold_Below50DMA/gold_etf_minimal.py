#!/usr/bin/env python3
"""
MINIMAL VERSION - Gold ETF Moving Average Analysis in ~50 lines
Copy and paste this if you just need a quick analysis!
"""

import pandas as pd

# ===== LOAD AND PREPARE =====
df = pd.read_csv('SBIG-ETF-Stock-Price-History.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Price'] = pd.to_numeric(df['Price'])
df = df.sort_values('Date').reset_index(drop=True)
df['Year'] = df['Date'].dt.year

# ===== CALCULATE MOVING AVERAGES =====
df['SMA_50'] = df['Price'].rolling(50).mean()
df['SMA_100'] = df['Price'].rolling(100).mean()
df['SMA_200'] = df['Price'].rolling(200).mean()

# ===== ANALYZE BY YEAR =====
results = []

for year in sorted(df['Year'].unique()):
    year_data = df[df['Year'] == year]

    # 50-DMA
    d50 = year_data.dropna(subset=['SMA_50'])
    below_50 = (d50['Price'] < d50['SMA_50']).sum() if len(d50) > 0 else 0
    pct_50 = (below_50 / len(d50)) * 100 if len(d50) > 0 else 0

    # 100-DMA
    d100 = year_data.dropna(subset=['SMA_100'])
    below_100 = (d100['Price'] < d100['SMA_100']).sum() if len(d100) > 0 else 0
    pct_100 = (below_100 / len(d100)) * 100 if len(d100) > 0 else 0

    # 200-DMA
    d200 = year_data.dropna(subset=['SMA_200'])
    below_200 = (d200['Price'] < d200['SMA_200']).sum() if len(d200) > 0 else 0
    pct_200 = (below_200 / len(d200)) * 100 if len(d200) > 0 else 0

    results.append({
        'Year': year,
        'Days': len(year_data),
        '50-DMA%': round(pct_50, 2),
        '100-DMA%': round(pct_100, 2),
        '200-DMA%': round(pct_200, 2),
        'Price_Min': round(year_data['Price'].min(), 2),
        'Price_Max': round(year_data['Price'].max(), 2)
    })

# ===== DISPLAY RESULTS =====
results_df = pd.DataFrame(results)
print("\n" + "="*100)
print("GOLD ETF MOVING AVERAGE ANALYSIS")
print("="*100)
print(results_df.to_string(index=False))
print("="*100)

# ===== EXPORT =====
results_df.to_csv('quick_analysis.csv', index=False)
print("\n✓ Results saved to: quick_analysis.csv")

# ===== STATISTICS =====
print("\nKEY METRICS:")
print(f"  50-DMA Avg: {results_df['50-DMA%'].mean():.2f}%")
print(f"  100-DMA Avg: {results_df['100-DMA%'].mean():.2f}%")
print(f"  200-DMA Avg: {results_df['200-DMA%'].mean():.2f}%")

start = df['Price'].iloc[0]
end = df['Price'].iloc[-1]
ret = ((end - start) / start) * 100
print(f"  Total Return: {ret:.2f}%")

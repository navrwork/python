#!/usr/bin/env python3
"""
Standalone Gold ETF Moving Average Analyzer
No classes - just pure functions for maximum simplicity
"""

import pandas as pd
import numpy as np

def load_data(csv_file):
    """Load and prepare data from CSV file"""
    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.sort_values('Date').reset_index(drop=True)
    df['Year'] = df['Date'].dt.year
    return df

def calculate_moving_averages(df):
    """Calculate 50-DMA, 100-DMA, and 200-DMA"""
    df['SMA_50'] = df['Price'].rolling(window=50).mean()
    df['SMA_100'] = df['Price'].rolling(window=100).mean()
    df['SMA_200'] = df['Price'].rolling(window=200).mean()
    return df

def get_fall_percentage(price, ma_value):
    """Calculate percentage fall from moving average"""
    if pd.isna(ma_value) or ma_value == 0:
        return 0
    return ((ma_value - price) / ma_value) * 100

def analyze_year(df, year):
    """Analyze a specific year"""
    year_data = df[df['Year'] == year].copy()

    result = {'Year': year}

    # General metrics
    result['Trading_Days'] = len(year_data)
    result['Price_Min'] = year_data['Price'].min()
    result['Price_Max'] = year_data['Price'].max()

    # 50-DMA Analysis
    year_50 = year_data.dropna(subset=['SMA_50'])
    if len(year_50) > 0:
        days_below_50 = (year_50['Price'] < year_50['SMA_50']).sum()
        result['50DMA_Days_Below'] = days_below_50
        result['50DMA_Percent_Below'] = (days_below_50 / len(year_50)) * 100

        below_50 = year_50[year_50['Price'] < year_50['SMA_50']].copy()
        if len(below_50) > 0:
            below_50['Fall_Pct'] = below_50.apply(
                lambda row: get_fall_percentage(row['Price'], row['SMA_50']), 
                axis=1
            )
            result['50DMA_Avg_Fall_%'] = below_50['Fall_Pct'].mean()
            result['50DMA_Max_Fall_%'] = below_50['Fall_Pct'].max()
        else:
            result['50DMA_Avg_Fall_%'] = 0
            result['50DMA_Max_Fall_%'] = 0
    else:
        result['50DMA_Days_Below'] = 0
        result['50DMA_Percent_Below'] = 0
        result['50DMA_Avg_Fall_%'] = 0
        result['50DMA_Max_Fall_%'] = 0

    # 100-DMA Analysis
    year_100 = year_data.dropna(subset=['SMA_100'])
    if len(year_100) > 0:
        days_below_100 = (year_100['Price'] < year_100['SMA_100']).sum()
        result['100DMA_Days_Below'] = days_below_100
        result['100DMA_Percent_Below'] = (days_below_100 / len(year_100)) * 100

        below_100 = year_100[year_100['Price'] < year_100['SMA_100']].copy()
        if len(below_100) > 0:
            below_100['Fall_Pct'] = below_100.apply(
                lambda row: get_fall_percentage(row['Price'], row['SMA_100']), 
                axis=1
            )
            result['100DMA_Avg_Fall_%'] = below_100['Fall_Pct'].mean()
            result['100DMA_Max_Fall_%'] = below_100['Fall_Pct'].max()
        else:
            result['100DMA_Avg_Fall_%'] = 0
            result['100DMA_Max_Fall_%'] = 0
    else:
        result['100DMA_Days_Below'] = 0
        result['100DMA_Percent_Below'] = 0
        result['100DMA_Avg_Fall_%'] = 0
        result['100DMA_Max_Fall_%'] = 0

    # 200-DMA Analysis
    year_200 = year_data.dropna(subset=['SMA_200'])
    if len(year_200) > 0:
        days_below_200 = (year_200['Price'] < year_200['SMA_200']).sum()
        result['200DMA_Days_Below'] = days_below_200
        result['200DMA_Percent_Below'] = (days_below_200 / len(year_200)) * 100

        below_200 = year_200[year_200['Price'] < year_200['SMA_200']].copy()
        if len(below_200) > 0:
            below_200['Fall_Pct'] = below_200.apply(
                lambda row: get_fall_percentage(row['Price'], row['SMA_200']), 
                axis=1
            )
            result['200DMA_Avg_Fall_%'] = below_200['Fall_Pct'].mean()
            result['200DMA_Max_Fall_%'] = below_200['Fall_Pct'].max()
        else:
            result['200DMA_Avg_Fall_%'] = 0
            result['200DMA_Max_Fall_%'] = 0
    else:
        result['200DMA_Days_Below'] = 0
        result['200DMA_Percent_Below'] = 0
        result['200DMA_Avg_Fall_%'] = 0
        result['200DMA_Max_Fall_%'] = 0

    return result

def main():
    """Main execution"""
    print("\n" + "="*100)
    print("GOLD ETF MOVING AVERAGE ANALYZER - STANDALONE VERSION")
    print("="*100)

    # Step 1: Load data
    print("\n[1] Loading data...")
    df = load_data('SBIG-ETF-Stock-Price-History.csv')
    print(f"    ✓ Loaded {len(df)} trading days")
    print(f"    ✓ Date range: {df['Date'].min()} to {df['Date'].max()}")

    # Step 2: Calculate moving averages
    print("\n[2] Calculating moving averages...")
    df = calculate_moving_averages(df)
    print(f"    ✓ 50-DMA from: {df[df['SMA_50'].notna()]['Date'].min()}")
    print(f"    ✓ 100-DMA from: {df[df['SMA_100'].notna()]['Date'].min()}")
    print(f"    ✓ 200-DMA from: {df[df['SMA_200'].notna()]['Date'].min()}")

    # Step 3: Analyze each year
    print("\n[3] Analyzing each year...")
    all_results = []
    for year in sorted(df['Year'].unique()):
        result = analyze_year(df, year)
        all_results.append(result)
        pct_50 = result['50DMA_Percent_Below']
        pct_100 = result['100DMA_Percent_Below']
        pct_200 = result['200DMA_Percent_Below']
        print(f"    Year {year}: 50-DMA={pct_50:.1f}% | 100-DMA={pct_100:.1f}% | 200-DMA={pct_200:.1f}%")

    # Step 4: Create results dataframe
    print("\n[4] Creating results dataframe...")
    results_df = pd.DataFrame(all_results)

    # Step 5: Display summary
    print("\n" + "="*100)
    print("SUMMARY - PERCENT BELOW MOVING AVERAGES")
    print("="*100)
    summary = results_df[['Year', '50DMA_Percent_Below', '100DMA_Percent_Below', '200DMA_Percent_Below']].copy()
    summary.columns = ['Year', '50-DMA %', '100-DMA %', '200-DMA %']
    for col in ['50-DMA %', '100-DMA %', '200-DMA %']:
        summary[col] = summary[col].apply(lambda x: f"{x:.2f}%")
    print(summary.to_string(index=False))

    # Step 6: Export to CSV
    print("\n[5] Exporting results...")
    results_df.to_csv('analysis_results.csv', index=False)
    print("    ✓ Results saved to: analysis_results.csv")

    # Step 7: Show key statistics
    print("\n" + "="*100)
    print("KEY STATISTICS")
    print("="*100)
    print(f"\n50-DMA: Avg Below = {results_df['50DMA_Percent_Below'].mean():.2f}%")
    print(f"100-DMA: Avg Below = {results_df[results_df['100DMA_Percent_Below']>0]['100DMA_Percent_Below'].mean():.2f}%")
    print(f"200-DMA: Avg Below = {results_df[results_df['200DMA_Percent_Below']>0]['200DMA_Percent_Below'].mean():.2f}%")

    start_price = df['Price'].iloc[0]
    end_price = df['Price'].iloc[-1]
    total_return = ((end_price - start_price) / start_price) * 100
    years = (df['Date'].max() - df['Date'].min()).days / 365.25
    cagr = ((end_price / start_price) ** (1 / years) - 1) * 100

    print(f"\nPrice: ₹{start_price:.2f} → ₹{end_price:.2f}")
    print(f"Total Return: {total_return:.2f}% over {years:.1f} years")
    print(f"CAGR: {cagr:.2f}%")
    print("="*100)

    return results_df

if __name__ == "__main__":
    results = main()

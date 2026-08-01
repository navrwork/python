#!/usr/bin/env python3
"""
SBI Gold ETF (SBIG) - Moving Average Analysis
Calculate and analyze 50-DMA, 100-DMA, and 200-DMA for historical data
Author: Generated for SBIG Analysis
Date: 2025-11-02
"""

import pandas as pd
import numpy as np
from datetime import datetime

class GoldETFAnalyzer:
    """Analyze Gold ETF data with multiple moving averages"""

    def __init__(self, csv_file):
        """
        Initialize the analyzer with CSV file

        Args:
            csv_file (str): Path to the CSV file with columns: Date, Price, Open, High, Low, Vol., Change %
        """
        self.df = pd.read_csv(csv_file)
        self.prepare_data()

    def prepare_data(self):
        """Prepare and clean the data"""
        # Convert Date to datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'])

        # Convert Price to float
        self.df['Price'] = pd.to_numeric(self.df['Price'], errors='coerce')

        # Sort by date (ascending)
        self.df = self.df.sort_values('Date').reset_index(drop=True)

        # Add year column
        self.df['Year'] = self.df['Date'].dt.year

        print(f"✓ Data loaded: {len(self.df)} trading days")
        print(f"  Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")

    def calculate_moving_averages(self):
        """Calculate 50-DMA, 100-DMA, and 200-DMA"""
        self.df['SMA_50'] = self.df['Price'].rolling(window=50).mean()
        self.df['SMA_100'] = self.df['Price'].rolling(window=100).mean()
        self.df['SMA_200'] = self.df['Price'].rolling(window=200).mean()

        print(f"✓ Moving averages calculated")
        print(f"  50-DMA available from: {self.df[self.df['SMA_50'].notna()]['Date'].min()}")
        print(f"  100-DMA available from: {self.df[self.df['SMA_100'].notna()]['Date'].min()}")
        print(f"  200-DMA available from: {self.df[self.df['SMA_200'].notna()]['Date'].min()}")

    def calculate_fall_percentage(self, price, ma_value):
        """Calculate percentage fall from moving average"""
        if pd.isna(ma_value) or ma_value == 0:
            return 0
        return ((ma_value - price) / ma_value) * 100

    def analyze_year(self, year):
        """
        Analyze a specific year's data

        Args:
            year (int): The year to analyze

        Returns:
            dict: Analysis results for the year
        """
        year_data = self.df[self.df['Year'] == year].copy()

        # Results dictionary
        results = {
            'Year': year,
            'Total_Trading_Days': len(year_data),
            'Price_Min': year_data['Price'].min(),
            'Price_Max': year_data['Price'].max(),
        }

        # ===== 50-DMA Analysis =====
        year_data_50 = year_data.dropna(subset=['SMA_50'])
        if len(year_data_50) > 0:
            days_below_50 = (year_data_50['Price'] < year_data_50['SMA_50']).sum()
            results['Days_Below_50DMA'] = days_below_50
            results['Total_Days_50DMA'] = len(year_data_50)
            results['Percent_Below_50DMA'] = (days_below_50 / len(year_data_50)) * 100

            # Calculate falls from 50-DMA
            below_50_data = year_data_50[year_data_50['Price'] < year_data_50['SMA_50']].copy()
            if len(below_50_data) > 0:
                below_50_data['Fall_Pct'] = below_50_data.apply(
                    lambda row: self.calculate_fall_percentage(row['Price'], row['SMA_50']), 
                    axis=1
                )
                results['Avg_Fall_50DMA_%'] = below_50_data['Fall_Pct'].mean()
                results['Max_Fall_50DMA_%'] = below_50_data['Fall_Pct'].max()
            else:
                results['Avg_Fall_50DMA_%'] = 0
                results['Max_Fall_50DMA_%'] = 0
        else:
            results['Days_Below_50DMA'] = 0
            results['Total_Days_50DMA'] = 0
            results['Percent_Below_50DMA'] = 0
            results['Avg_Fall_50DMA_%'] = 0
            results['Max_Fall_50DMA_%'] = 0

        # ===== 100-DMA Analysis =====
        year_data_100 = year_data.dropna(subset=['SMA_100'])
        if len(year_data_100) > 0:
            days_below_100 = (year_data_100['Price'] < year_data_100['SMA_100']).sum()
            results['Days_Below_100DMA'] = days_below_100
            results['Total_Days_100DMA'] = len(year_data_100)
            results['Percent_Below_100DMA'] = (days_below_100 / len(year_data_100)) * 100

            # Calculate falls from 100-DMA
            below_100_data = year_data_100[year_data_100['Price'] < year_data_100['SMA_100']].copy()
            if len(below_100_data) > 0:
                below_100_data['Fall_Pct'] = below_100_data.apply(
                    lambda row: self.calculate_fall_percentage(row['Price'], row['SMA_100']), 
                    axis=1
                )
                results['Avg_Fall_100DMA_%'] = below_100_data['Fall_Pct'].mean()
                results['Max_Fall_100DMA_%'] = below_100_data['Fall_Pct'].max()
            else:
                results['Avg_Fall_100DMA_%'] = 0
                results['Max_Fall_100DMA_%'] = 0
        else:
            results['Days_Below_100DMA'] = 0
            results['Total_Days_100DMA'] = 0
            results['Percent_Below_100DMA'] = 0
            results['Avg_Fall_100DMA_%'] = 0
            results['Max_Fall_100DMA_%'] = 0

        # ===== 200-DMA Analysis =====
        year_data_200 = year_data.dropna(subset=['SMA_200'])
        if len(year_data_200) > 0:
            days_below_200 = (year_data_200['Price'] < year_data_200['SMA_200']).sum()
            results['Days_Below_200DMA'] = days_below_200
            results['Total_Days_200DMA'] = len(year_data_200)
            results['Percent_Below_200DMA'] = (days_below_200 / len(year_data_200)) * 100

            # Calculate falls from 200-DMA
            below_200_data = year_data_200[year_data_200['Price'] < year_data_200['SMA_200']].copy()
            if len(below_200_data) > 0:
                below_200_data['Fall_Pct'] = below_200_data.apply(
                    lambda row: self.calculate_fall_percentage(row['Price'], row['SMA_200']), 
                    axis=1
                )
                results['Avg_Fall_200DMA_%'] = below_200_data['Fall_Pct'].mean()
                results['Max_Fall_200DMA_%'] = below_200_data['Fall_Pct'].max()
            else:
                results['Avg_Fall_200DMA_%'] = 0
                results['Max_Fall_200DMA_%'] = 0
        else:
            results['Days_Below_200DMA'] = 0
            results['Total_Days_200DMA'] = 0
            results['Percent_Below_200DMA'] = 0
            results['Avg_Fall_200DMA_%'] = 0
            results['Max_Fall_200DMA_%'] = 0

        return results

    def analyze_all_years(self):
        """Analyze all years in the dataset"""
        all_results = []

        for year in sorted(self.df['Year'].unique()):
            results = self.analyze_year(year)
            all_results.append(results)
            print(f"✓ {year}: {results['Total_Trading_Days']} days | "
                  f"50-DMA: {results['Percent_Below_50DMA']:.2f}% | "
                  f"100-DMA: {results['Percent_Below_100DMA']:.2f}% | "
                  f"200-DMA: {results['Percent_Below_200DMA']:.2f}%")

        self.results_df = pd.DataFrame(all_results)
        return self.results_df

    def print_summary_table(self):
        """Print a formatted summary table"""
        print("\n" + "="*200)
        print("SUMMARY TABLE - MOVING AVERAGE ANALYSIS")
        print("="*200)

        summary = self.results_df[[
            'Year', 'Total_Trading_Days',
            'Days_Below_50DMA', 'Percent_Below_50DMA',
            'Days_Below_100DMA', 'Percent_Below_100DMA',
            'Days_Below_200DMA', 'Percent_Below_200DMA',
            'Price_Min', 'Price_Max'
        ]].copy()

        # Format percentage columns
        for col in ['Percent_Below_50DMA', 'Percent_Below_100DMA', 'Percent_Below_200DMA']:
            summary[col] = summary[col].apply(lambda x: f"{x:.2f}%")

        for col in ['Price_Min', 'Price_Max']:
            summary[col] = summary[col].apply(lambda x: f"₹{x:.2f}")

        print(summary.to_string(index=False))
        print("="*200)

    def export_to_csv(self, filename):
        """Export results to CSV"""
        export_df = self.results_df.copy()

        # Format columns for export
        export_df['Percent_Below_50DMA'] = export_df['Percent_Below_50DMA'].apply(lambda x: f"{x:.2f}%")
        export_df['Percent_Below_100DMA'] = export_df['Percent_Below_100DMA'].apply(lambda x: f"{x:.2f}%")
        export_df['Percent_Below_200DMA'] = export_df['Percent_Below_200DMA'].apply(lambda x: f"{x:.2f}%")
        export_df['Avg_Fall_50DMA_%'] = export_df['Avg_Fall_50DMA_%'].apply(lambda x: f"{x:.2f}%")
        export_df['Avg_Fall_100DMA_%'] = export_df['Avg_Fall_100DMA_%'].apply(lambda x: f"{x:.2f}%")
        export_df['Avg_Fall_200DMA_%'] = export_df['Avg_Fall_200DMA_%'].apply(lambda x: f"{x:.2f}%")
        export_df['Max_Fall_50DMA_%'] = export_df['Max_Fall_50DMA_%'].apply(lambda x: f"{x:.2f}%")
        export_df['Max_Fall_100DMA_%'] = export_df['Max_Fall_100DMA_%'].apply(lambda x: f"{x:.2f}%")
        export_df['Max_Fall_200DMA_%'] = export_df['Max_Fall_200DMA_%'].apply(lambda x: f"{x:.2f}%")

        export_df.to_csv(filename, index=False)
        print(f"✓ Results exported to: {filename}")

    def print_statistics(self):
        """Print key statistics"""
        print("\n" + "="*120)
        print("KEY STATISTICS")
        print("="*120)

        print("\n50-DMA ANALYSIS:")
        print(f"  Highest % Below: {self.results_df['Percent_Below_50DMA'].max():.2f}%")
        print(f"  Lowest % Below: {self.results_df['Percent_Below_50DMA'].min():.2f}%")
        print(f"  Average % Below: {self.results_df['Percent_Below_50DMA'].mean():.2f}%")

        print("\n100-DMA ANALYSIS:")
        valid_100 = self.results_df[self.results_df['Percent_Below_100DMA'] > 0]
        print(f"  Highest % Below: {valid_100['Percent_Below_100DMA'].max():.2f}%")
        print(f"  Lowest % Below: {valid_100['Percent_Below_100DMA'].min():.2f}%")
        print(f"  Average % Below: {valid_100['Percent_Below_100DMA'].mean():.2f}%")

        print("\n200-DMA ANALYSIS:")
        valid_200 = self.results_df[self.results_df['Percent_Below_200DMA'] > 0]
        print(f"  Highest % Below: {valid_200['Percent_Below_200DMA'].max():.2f}%")
        print(f"  Lowest % Below: {valid_200['Percent_Below_200DMA'].min():.2f}%")
        print(f"  Average % Below: {valid_200['Percent_Below_200DMA'].mean():.2f}%")

        print("\nPRICE APPRECIATION:")
        start_price = self.df['Price'].iloc[0]
        end_price = self.df['Price'].iloc[-1]
        total_return = ((end_price - start_price) / start_price) * 100
        years = (self.df['Date'].max() - self.df['Date'].min()).days / 365.25
        cagr = ((end_price / start_price) ** (1 / years) - 1) * 100
        print(f"  Starting Price: ₹{start_price:.2f}")
        print(f"  Ending Price: ₹{end_price:.2f}")
        print(f"  Total Return: {total_return:.2f}%")
        print(f"  CAGR: {cagr:.2f}%")
        print(f"  Period: {years:.1f} years")
        print("="*120)


def main():
    """Main execution function"""

    # ===== STEP 1: Initialize Analyzer =====
    print("\n" + "="*120)
    print("SBI GOLD ETF (SBIG) - MOVING AVERAGE ANALYZER")
    print("="*120)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Load data
    analyzer = GoldETFAnalyzer('SBIG-ETF-Stock-Price-History.csv')

    # ===== STEP 2: Calculate Moving Averages =====
    analyzer.calculate_moving_averages()

    # ===== STEP 3: Analyze All Years =====
    print("\n" + "="*120)
    print("ANALYZING EACH YEAR")
    print("="*120)
    analyzer.analyze_all_years()

    # ===== STEP 4: Print Results =====
    analyzer.print_summary_table()
    analyzer.print_statistics()

    # ===== STEP 5: Export to CSV =====
    analyzer.export_to_csv('SBIG_MA_Analysis_Results.csv')

    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*120)

    return analyzer


if __name__ == "__main__":
    analyzer = main()

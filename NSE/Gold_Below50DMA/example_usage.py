#!/usr/bin/env python3
"""
SIMPLE USAGE EXAMPLE
"""

from gold_etf_analyzer import GoldETFAnalyzer

# Create analyzer instance
analyzer = GoldETFAnalyzer('SBIG-ETF-Stock-Price-History.csv')

# Calculate moving averages
analyzer.calculate_moving_averages()

# Analyze all years
results = analyzer.analyze_all_years()

# Print summary
analyzer.print_summary_table()

# Print statistics
analyzer.print_statistics()

# Export results
analyzer.export_to_csv('results.csv')

# Or analyze a specific year
year_2024_analysis = analyzer.analyze_year(2024)
print(year_2024_analysis)

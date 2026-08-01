# Calculate for all years including 2020, 2021, and 2022
print("=" * 100)
print("GOLDIETF - COMPREHENSIVE 50-DMA ANALYSIS (2020-2025)")
print("=" * 100)

all_years_analysis = []

for year in sorted(df_5yrs['Year'].unique()):
    year_data = df_5yrs[df_5yrs['Year'] == year].copy()
    year_data_valid = year_data.dropna(subset=['SMA_50'])
    
    if len(year_data_valid) == 0:
        print(f"\n{year}: Insufficient data (less than 50 trading days available)")
        all_years_analysis.append({
            'Year': year,
            'Status': 'Insufficient Data',
            'Total_Trading_Days': len(year_data),
            'Days_Below_50DMA': 'N/A',
            'Percentage_Below': 'N/A',
            'Avg_Fall_Pct': 'N/A',
            'Max_Fall_Pct': 'N/A',
            'Price_Range': 'N/A'
        })
        continue
    
    days_below = (year_data_valid['Price'] < year_data_valid['SMA_50']).sum()
    total_trading_days = len(year_data_valid)
    pct_below = (days_below / total_trading_days) * 100
    
    below_data = year_data_valid[year_data_valid['Price'] < year_data_valid['SMA_50']].copy()
    if len(below_data) > 0:
        below_data['Fall_Pct'] = ((below_data['SMA_50'] - below_data['Price']) / below_data['SMA_50']) * 100
        avg_fall = below_data['Fall_Pct'].mean()
        max_fall = below_data['Fall_Pct'].max()
    else:
        avg_fall = 0
        max_fall = 0
    
    price_min = year_data_valid['Price'].min()
    price_max = year_data_valid['Price'].max()
    
    all_years_analysis.append({
        'Year': year,
        'Status': 'Full Year',
        'Total_Trading_Days': total_trading_days,
        'Days_Below_50DMA': int(days_below),
        'Percentage_Below': round(pct_below, 2),
        'Avg_Fall_Pct': round(avg_fall, 2),
        'Max_Fall_Pct': round(max_fall, 2),
        'Price_Range': f"₹{price_min:.2f} - ₹{price_max:.2f}"
    })
    
    print(f"\n{year}:")
    print(f"  Status: Full Year Data")
    print(f"  Trading Days Analyzed: {total_trading_days}")
    print(f"  Days Below 50-DMA: {days_below}")
    print(f"  Percentage of Days Below 50-DMA: {pct_below:.2f}%")
    print(f"  Average Fall from 50-DMA: {avg_fall:.2f}%")
    print(f"  Maximum Fall from 50-DMA: {max_fall:.2f}%")
    print(f"  Price Range: ₹{price_min:.2f} - ₹{price_max:.2f}")

print("\n" + "=" * 100)
print("SPECIAL NOTE FOR 2020:")
print("=" * 100)
year_2020 = df[df['Year'] == 2020]
print(f"Data for 2020 starts from: {year_2020['Date'].min().strftime('%B %d, %Y')}")
print(f"Data available for 2020: {len(year_2020)} days")
print(f"Since less than 50 trading days are available, 50-DMA cannot be calculated.")
print("=" * 100)
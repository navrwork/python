#!/usr/bin/env python3
"""
GOLD ETF BUY SIGNAL CHECKER
====================================
Purpose: Check if Gold ETF meets buying criteria
Criteria: Price < 20-DMA AND RSI < 40 (oversold)

Usage:
1. Download 60 days of historical prices from your brokerage
2. Update the PRICES list below with your data (oldest to newest)
3. Update CURRENT_PRICE with today's closing price
4. Run: python gold_etf_signal_checker.py
5. Check the output for BUY SIGNALS

Author: Your Investment Tracking System
Date: November 2025
"""

import numpy as np
from datetime import datetime

# ============================================================================
# CONFIGURATION - UPDATE THESE VALUES DAILY
# ============================================================================

ETF_TICKER = "103.60"                    # Change to your ETF: GOLDBEES, GOLDIETF, SETFGOLD
ETF_NAME = "GOLDIETF"    # Display name
CURRENT_PRICE = 105.41                     # Today's closing price - UPDATE DAILY

# Historical closing prices (oldest to newest) - Minimum 34 days required
# Download from your brokerage platform (Angel One, 5Paisa, Zerodha, etc.)
PRICES = [
    # Paste your 60 days of closing prices here (oldest first, newest last)
    # Example format:
    # 95.50, 95.75, 96.00, 96.25, 96.50, 96.75, 97.00, 97.25, 97.50, 97.75,
    # ... continue with your actual data ...
    # 104.50, 104.65, 104.80
    
    # Sample data for demonstration:
    105.41, 107.29, 109, 106.21, 106.85, 105.17, 103.23, 103.35, 102.89, 103.18, 
    103.34, 102.76, 103.09, 100.14, 103.34, 103.72, 104.76, 109.17, 108.23, 111.83, 
    108.82, 108.9, 108.61, 106.11, 104.02, 104.69, 105.25, 103.11, 102.46, 99.88, 
    101.33, 99.57, 99.66, 97.38, 97.59, 97.81, 98.36, 96.35, 94.29, 94.5, 
    94.41, 95.62, 93.97, 94.29, 93.63, 93.91, 94.52, 93.05, 91.68, 91.04, 
    90.96, 89.59, 89.73, 88.17, 87.22, 86.59, 86.27, 85.38, 85.38, 84.77
]

# ============================================================================
# DO NOT MODIFY BELOW THIS LINE
# ============================================================================

def calculate_rsi(prices, period=14):
    """Calculate RSI (Relative Strength Index) - standard 14-period"""
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)
    
    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        upval = delta if delta > 0 else 0.0
        downval = -delta if delta < 0 else 0.0
        
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)
    
    return rsi


def check_buy_signal():
    """Main function to check buy signal"""
    
    # Validate data
    if len(PRICES) < 34:
        print(f"ERROR: Need minimum 34 prices, got {len(PRICES)}")
        print("Please download 60 days of historical data from your brokerage")
        return None
    
    prices = np.array(PRICES, dtype=float)
    
    # Calculate indicators
    dma_20 = np.mean(prices[-20:])  # 20-day moving average
    rsi = calculate_rsi(prices, period=14)[-1]  # Latest RSI
    
    # Check conditions
    price_below_dma = CURRENT_PRICE < dma_20
    rsi_oversold = rsi < 40
    buy_signal = price_below_dma and rsi_oversold
    
    # Calculate additional metrics
    distance_from_dma = CURRENT_PRICE - dma_20
    distance_pct = (distance_from_dma / dma_20 * 100) if dma_20 != 0 else 0
    
    # Print results
    print("\n" + "="*80)
    print("GOLD ETF BUY SIGNAL CHECKER")
    print("="*80)
    print(f"\nETF: {ETF_NAME} ({ETF_TICKER})")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print(f"Criteria: Price < 20-DMA AND RSI < 40\n")
    
    print("📊 CURRENT VALUES:")
    print(f"   Current Price:        ₹{CURRENT_PRICE:.2f}")
    print(f"   20-Day Moving Average: ₹{dma_20:.2f}")
    print(f"   Distance from 20-DMA: ₹{distance_from_dma:.2f} ({distance_pct:+.2f}%)")
    print(f"   RSI (14):             {rsi:.2f}")
    
    print("\n📈 SIGNAL ANALYSIS:")
    dma_status = "✅ YES" if price_below_dma else "❌ NO"
    rsi_status = "✅ YES" if rsi_oversold else "❌ NO"
    print(f"   {dma_status} - Price < 20-DMA?")
    print(f"   {rsi_status} - RSI < 40?")
    
    print("\n" + "="*80)
    if buy_signal:
        print("✅ STRONG BUY SIGNAL")
        print("   ACTION: Invest 2 tranches of your budget")
        recommendation = "STRONG BUY"
    elif price_below_dma or rsi_oversold:
        print("⚠️  WEAK BUY SIGNAL (1 condition met)")
        print("   ACTION: Invest 1 tranche (optional)")
        recommendation = "WEAK BUY"
    else:
        print("❌ NO BUY SIGNAL")
        print("   ACTION: Hold cash, wait for next opportunity")
        recommendation = "HOLD"
    print("="*80)
    
    # Additional context
    print("\n📉 CONTEXT:")
    recent_20 = prices[-20:]
    print(f"   20-Day High:          ₹{recent_20.max():.2f}")
    print(f"   20-Day Low:           ₹{recent_20.min():.2f}")
    print(f"   20-Day Range:         ₹{recent_20.max() - recent_20.min():.2f}")
    if len(prices) > 1:
        change_pct = ((prices[-1] - prices[-2]) / prices[-2] * 100)
        print(f"   1-Day Change:         {change_pct:+.2f}%")
    
    print("\n" + "="*80)
    
    return {
        'ticker': ETF_TICKER,
        'name': ETF_NAME,
        'current_price': CURRENT_PRICE,
        'dma_20': dma_20,
        'rsi': rsi,
        'buy_signal': buy_signal,
        'recommendation': recommendation
    }


def save_signal_log(result):
    """Save signal to log file for tracking"""
    if result is None:
        return
    
    log_line = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | {result['ticker']} | Price: {result['current_price']:.2f} | 20-DMA: {result['dma_20']:.2f} | RSI: {result['rsi']:.2f} | Signal: {result['recommendation']}\n"
    
    with open('gold_etf_signals.log', 'a') as f:
        f.write(log_line)
    
    print("✓ Signal logged to: gold_etf_signals.log")


if __name__ == "__main__":
    result = check_buy_signal()
    
    if result:
        save_signal_log(result)
        
        print("\n" + "="*80)
        print("INSTRUCTIONS FOR DAILY USE:")
        print("="*80)
        print("""
1. At market close (3:30 PM IST), download today's historical prices
2. Update PRICES list in this script (paste all closing prices)
3. Update CURRENT_PRICE with today's close
4. Run: python gold_etf_signal_checker.py
5. Check recommendation at top

AUTOMATED DAILY RUN (Linux/Mac):
   Add to crontab: 0 16 * * 1-5 python /path/to/gold_etf_signal_checker.py
   (Runs at 4 PM IST on weekdays)

AUTOMATED DAILY RUN (Windows):
   Use Task Scheduler to run: python gold_etf_signal_checker.py
   Set time: 4:00 PM daily
        """)

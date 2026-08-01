import pandas as pd
import yfinance as yf
from twilio.rest import Client
import schedule
import time

# Config: Replace these with your own info
ETF_TICKER = 'GOLDIETF.NS'  # or GOLDBEES.NS, as per your broker!
ACCOUNT_SID = '...'
AUTH_TOKEN = '...'
TWILIO_WHATSAPP = 'whatsapp:...'  # Twilio sandbox sender
YOUR_WHATSAPP = 'whatsapp:...'   # Your phone

def check_gold_dma_and_notify():
    data = yf.download(ETF_TICKER, period='90d')
    data['50DMA'] = data['Close'].rolling(50).mean()
    current_price = data['Close'][-1]
    dma_50 = data['50DMA'][-1]
    if current_price < dma_50:
        # Initialize Twilio client
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message_body = f"{ETF_TICKER} price is {current_price:.2f}, below 50 DMA ({dma_50:.2f})!"
        message = client.messages.create(
            from_=TWILIO_WHATSAPP,
            body=message_body,
            to=YOUR_WHATSAPP
        )
        print("Alert sent:", message_body)
    else:
        print("No alert: Price is above 50 DMA.")

# check now
check_gold_dma_and_notify


# Scheduler to run daily
#schedule.every().day.at("09:00").do(check_gold_dma_and_notify)

#while True:
#    schedule.run_pending()
#    time.sleep(60)

import requests
from bs4 import BeautifulSoup
import time
import smtplib

# Amazon product URL
url = 'https://www.amazon.in/s?k=digital+camera&crid=WD83YZPOLJXU&sprefix=Digital+camer%2Caps%2C267&ref=nb_sb_ss_ts-doa-p_2_13'

# Your desired price
target_price = 500.00

# Email settings
sender_email = '**************.com'
receiver_email = '***********.com'
email_password = '********'

def get_amazon_price(url):
    headers = {
        'User-Agent': 'Your User Agent String',
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the price element on the Amazon page and extract the price
    price_element = soup.find('span', {'id': 'priceblock_ourprice'})
    if price_element:
        price_str = price_element.get_text(strip=True)
        price = float(price_str.replace('$', '').replace(',', ''))
        return price
    else:
        print("Price not found")
        return None

def send_email(message):
    subject = 'Amazon Price Alert'
    body = f'Subject: {subject}\n\n{message}'

    # Establish a connection with the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, email_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, body)

def track_amazon_price(url, target_price):
    while True:
        current_price = get_amazon_price(url)

        if current_price and current_price <= target_price:
            message = f'The price is now {current_price}. Buy it now!'
            send_email(message)
            break

        print(f'Current Price: {current_price}. Waiting...')
        time.sleep(3600)  # Check the price every hour

if __name__ == '__main__':
    track_amazon_price(url, target_price)


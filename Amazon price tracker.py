
import requests
from bs4 import BeautifulSoup
import smtplib
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



PRODUCT_URL = "https://www.amazon.in/gp/aw/d/B0D7HW3JNY?pd_rd_plhdr=t&hsa_cr_id=0&qid=1789492724&sr=1-2-941ebe59-d25b-49d0-b214-12cc5b66c90f&i=aps&aref=HLTjRuVI7Y&_encoding=UTF8&ref_=sbx_s_sparkle_sbtcd_asin_1_title&pd_rd_w=UAOfH&content-id=amzn1.sym.7b6188a8-103f-4f88-b43a-19aba06e30c1%3Aamzn1.sym.7b6188a8-103f-4f88-b43a-19aba06e30c1&pf_rd_p=7b6188a8-103f-4f88-b43a-19aba06e30c1&pf_rd_r=RMR0ZZ6CJ7GFY2G0V2GM&pd_rd_wg=HgbZZ&pd_rd_r=7869c51f-2a8e-45ba-b88e-34001dc879e2&th=1"


TARGET_PRICE = 500.00


SENDER_EMAIL = "YOURGMAILgmail.com"

# Email address that will RECEIVE the alert
RECEIVER_EMAIL = "YOURGMAIL@gmail.com"

# Gmail APP PASSWORD
# Do NOT put your normal Gmail password here.
GMAIL_APP_PASSWORD = "************"

# Check every 1 hour
CHECK_INTERVAL = 3600



def get_amazon_price(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,image/webp,"
            "image/apng,*/*;q=0.8"
        ),
        "Connection": "keep-alive"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("HTTP Status:", response.status_code)

        if response.status_code != 200:
            print("Amazon did not return a normal page.")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

       

        price_selectors = [
            "#corePriceDisplay_desktop_feature_div .a-price .a-offscreen",
            "#corePrice_feature_div .a-price .a-offscreen",
            "#apex_desktop .a-price .a-offscreen",
            "span.a-price span.a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            "#priceblock_saleprice"
        ]

        for selector in price_selectors:

            price_element = soup.select_one(selector)

            if price_element:

                price_text = price_element.get_text(
                    strip=True
                )

                print("Price text found:", price_text)

                # Remove currency symbols and commas
                cleaned_price = re.sub(
                    r"[^\d.]",
                    "",
                    price_text
                )

                if cleaned_price:

                    price = float(cleaned_price)

                    return price

        print("Price element was not found.")

        # Check if Amazon returned a bot-check page
        page_text = soup.get_text(" ", strip=True).lower()

        if "captcha" in page_text:
            print("Amazon returned a CAPTCHA page.")

        if "robot" in page_text:
            print("Amazon thinks this request may be automated.")

        return None

    except requests.exceptions.RequestException as e:

        print("Network error:", e)

        return None

    except Exception as e:

        print("Error while extracting price:", e)

        return None




def send_email(current_price):

    subject = "Amazon Price Alert"

    message = f"""
Amazon Price Alert!

The product price has reached your target.

Current Price: ₹{current_price:.2f}
Target Price: ₹{TARGET_PRICE:.2f}

Buy it here:

{PRODUCT_URL}
"""

    try:

        email = MIMEMultipart()

        email["From"] = SENDER_EMAIL
        email["To"] = RECEIVER_EMAIL
        email["Subject"] = subject

        email.attach(
            MIMEText(message, "plain")
        )

        print("Connecting to Gmail...")

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                SENDER_EMAIL,
                GMAIL_APP_PASSWORD
            )

            server.sendmail(
                SENDER_EMAIL,
                RECEIVER_EMAIL,
                email.as_string()
            )

        print("Email alert sent successfully!")

    except Exception as e:

        print("Could not send email.")
        print("Email error:", e)


def track_amazon_price():

    print("=" * 60)
    print("AMAZON PRICE TRACKER")
    print("=" * 60)

    print("Product URL:")
    print(PRODUCT_URL)

    print()
    print("Target Price: ₹", TARGET_PRICE)
    print("Check interval:", CHECK_INTERVAL, "seconds")
    print("=" * 60)

    while True:

        print()
        print("Checking Amazon price...")

        current_price = get_amazon_price(
            PRODUCT_URL
        )

        if current_price is None:

            print(
                "Could not determine the current price."
            )

        else:

            print(
                f"Current Price: ₹{current_price:.2f}"
            )

            if current_price <= TARGET_PRICE:

                print()
                print(
                    "TARGET PRICE REACHED!"
                )

                send_email(
                    current_price
                )

                print(
                    "Price alert sent."
                )

                # Stop after sending the alert
                break

            else:

                difference = (
                    current_price - TARGET_PRICE
                )

                print(
                    f"₹{difference:.2f} above target price."
                )

                print(
                    "Waiting before checking again..."
                )

        print()
        print(
            f"Next check in "
            f"{CHECK_INTERVAL // 60} minutes."
        )

        time.sleep(
            CHECK_INTERVAL
        )


=

if __name__ == "__main__":

    track_amazon_price()


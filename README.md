# Amazon-price-Tracker

The Amazon Price Tracker script automates the process of monitoring the price of a specified product on Amazon. It periodically fetches the latest price from the product page using ScraperAPI to bypass Amazon’s anti-scraping mechanisms. The script extracts the price using BeautifulSoup and compares it with a predefined target price. If the price drops below the target, an automated email alert is sent to the user using SMTP. To enhance security, email credentials are stored as environment variables instead of being hardcoded. The script runs continuously, checking the price at regular intervals (e.g., every hour), ensuring users never miss a price drop on their desired product

+--------------------+
|       Start       |
+--------------------+
         |
         v
+----------------------+
| Fetch Amazon Page   |
| (Using ScraperAPI)  |
+----------------------+
         |
         v
+----------------------+
| Extract Product Price|
| (Using BeautifulSoup)|
+----------------------+
         |
         v
+----------------------+
| Compare with Target |
| Price              |
+----------------------+
     |         |
     | No      | Yes
     |         v
     |   +----------------------+
     |   | Send Email Alert     |
     |   +----------------------+
     |         |
     |         v
     |   +----------------------+
     |   | Stop Tracking        |
     |   +----------------------+
     |
     v
+----------------------+
| Wait for Time Interval|
| (e.g., 1 Hour)      |
+----------------------+
         |
         v
+----------------------+
| Repeat Process       |
+----------------------+

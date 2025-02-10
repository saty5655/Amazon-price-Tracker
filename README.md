# Amazon-price-Tracker

The Amazon Price Tracker script automates the process of monitoring the price of a specified product on Amazon. It periodically fetches the latest price from the product page using ScraperAPI to bypass Amazon’s anti-scraping mechanisms. The script extracts the price using BeautifulSoup and compares it with a predefined target price. If the price drops below the target, an automated email alert is sent to the user using SMTP. To enhance security, email credentials are stored as environment variables instead of being hardcoded. The script runs continuously, checking the price at regular intervals (e.g., every hour), ensuring users never miss a price drop on their desired product


The process follows these steps:

Start->
Fetch Amazon Product Page (Using ScraperAPI to bypass restrictions)->
Extract the Price (Using BeautifulSoup)->
Check if Price is Below Target->
Yes → Send Email Notification or
No → Wait and Retry After an Interval->
Repeat Until Price Drop is Dete

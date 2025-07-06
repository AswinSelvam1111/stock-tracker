# StockTracker

**StockTracker** is a Python-based application that retrieves real-time stock data from multiple sites. It also possesses the ability to store such data in a database file, which can be exported as a CSV file for future use or represented graphically as a line graph. This is meant to be a beginner project that lets me delve into the introductory world of webscraping and database management. Eventually, there would be changes to the code to make it more user-friendly and hopefully, more time-efficient. If you stumbled across this and are interested in helping me out, please feel free to do so!

## Features:

- Fetches real-time stock data using web scraping (Selenium)
- Stores data in a local database, supporting multiple tables (sqlite3)
- Exports data to CSV format with timestamps
- Data handling (pandas) and visualization (plotly)

## Installation:

Take note that this project was developed and tested on **Python 3.13.3**.

To install all the necessary libraries:

```bash
pip install undetected-chromedriver
pip install selenium
pip install pandas
pip install plotly
```

The later versions of this code do not require you to download any chromedrivers as webscraping is done headless (without manually opening the web browser.)

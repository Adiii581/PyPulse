# PyPulse - Polite PyPI Data Aggregator

**PyPulse** is a robust, "white-hat" data aggregation tool built in Python. It uses an automated browser to scrape the Python Package Index (PyPI) for any search term, navigate through all result pages, and compile package data into a clean CSV file.

This project is an advanced demonstration of browser automation, designed to navigate the real-world challenges of a modern web application, including bot detection, dynamic content, and JavaScript-based elements.

**Note**: This tool is an educational project built to demonstrate advanced automation skills. It is intentionally a **"polite" scraper** that includes randomized delays to mimic human behavior and respect server load.

Demo: https://youtu.be/JqIU3oK4b74
🔗 **Target Website (Data source for PyPulse): [https://pypi.org](https://pypi.org)**

-----

## ✨ Key Features

  - **Bypasses Bot Detection**: Utilizes `selenium-stealth` to configure the browser driver, successfully evading JavaScript-based bot detection and CAPTCHA walls.
  - **Ethical & Polite Scraping**: Includes a randomized 2-5 second "human" delay on every page load, ensuring the script is a good citizen and does not hammer the server.
  - **Automated Pagination Loop**: Programmatically scrapes all available pages (from 1 to 500+), finds the "Next" button using a robust XPath selector, and automatically stops when the last page is reached.
  - **Dynamic Content Handling**: Intelligently handles dynamic page elements, including programmatically accepting the cookie consent banner on the first load (which otherwise blocks pagination).
  - **Resilient Interaction**: Explicitly scrolls to the bottom of the page to ensure the "Next" button is in the browser viewport before executing a click, solving a common automation bug.
  - **Clean Data Export**: Parses all package titles, descriptions, and URLs and saves them to a structured `pypi_packages.csv` file.

-----

## 🏛️ Architectural Overview

PyPulse is a Python script that automates a Google Chrome browser instance to perform tasks as a human user would.

  - **Stealth Automation Core**: The script initializes a `selenium-stealth` patched driver, which hides the default automation flags that allow sites like PyPI to detect and block scrapers.
  - **Dynamic Navigation**: The tool navigates directly to a programmatically built search URL. It immediately handles dynamic JavaScript elements like the cookie consent banner, using a short wait to find the button by its ID and click it.
  - **Pagination & Scrape Loop**: The script enters a `while True` loop. In each loop, it:
    1.  Waits for the package "snippet" cards to load.
    2.  Scrapes all 20 packages on the page.
    3.  Pauses for a random 2-5 seconds (the "politeness" delay).
    4.  Programmatically scrolls to the bottom of the page.
    5.  Waits 10 seconds for the "Next" button to become clickable.
    6.  Clicks "Next" and uses an `EC.staleness_of` check to wait for the old content to disappear before starting the next loop.
  - **Graceful Exit**: If the "Next" button is not found (throwing a `TimeoutException`), the script assumes it has reached the final page, breaks the loop, and proceeds to save the data.

-----

## 🚀 Getting Started

Follow these steps to set up and run the project locally. Ensure you have **Python 3** and **Google Chrome** installed.

### 1\. Clone or Download

Clone this repository or download the `pypi_scraper.py` file.

### 2\. Install Dependencies

This project requires three main libraries. Open your terminal and run:

```bash
pip install selenium
pip install webdriver-manager
pip install selenium-stealth
```

### 3\. Run the Scraper

Run the script from your terminal. It's fully automated and will begin scraping immediately.

```bash
python pypi_scraper.py
```

The script will print its progress to the console and create a `pypi_packages.csv` file in the same directory when finished.

-----

## 🛠️ Technology Stack

| **Area** | **Technologies Used** |
| :--- | :--- |
| **Automation Core** | Python, Selenium, Selenium-Stealth, webdriver-manager |
| **Libraries** | `csv`, `time`, `random`, `urllib.parse` |
| **Core Skills** | Web Scraping, Browser Automation, HTML Parsing, DOM Navigation, CSS Selectors, XPath |

-----

## 📚 Why PyPulse Stands Out

  - **Resilience**: This isn't a "happy path" script. It is built to solve real-world problems: it successfully navigates CAPTCHA walls, cookie banners, dynamic content, and off-screen elements.
  - **Ethical Design**: Demonstrates responsible scraping by including politeness delays, proving it's possible to collect data without negatively impacting the target service.
  - **No API, No Problem**: This project proves the ability to gather public data when a public-facing API for the desired task (keyword search) is not available.
  - **Advanced Logic**: Uses a combination of explicit waits (`element_to_be_clickable`), smart waits (`staleness_of`), and JavaScript execution (`scrollTo`) to create a stable, reliable automation process.

-----

## 📬 Contact

For questions or feedback, please connect with me on [LinkedIn](https://linkedin.com/in/aditya-chhabria123).

-----

*Built with 💻 by Aditya Chhabria*

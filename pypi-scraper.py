import csv
import time     # For our politeness delay
import random   # For our politeness delay
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote_plus  # For building the URL

# --- Settings ---
SEARCH_TERM = "api"
# -----------------

print(f"Starting PyPI Package Scraper for search term: '{SEARCH_TERM}'")

# --- Step 2: Automatically gets the right ChromeDriver ---
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# --- NEW STEALTH CODE ---
stealth(driver,
      languages=["en-US", "en"],
      vendor="Google Inc.",
      platform="Win32",
      webgl_vendor="Intel Inc.",
      renderer="Intel Iris OpenGL Engine",
      fix_hairline=True,
      )
# ------------------------

# This is the "wait" helper. It will wait up to 10 seconds.
wait = WebDriverWait(driver, 10)

# --- Step 4: Search for Packages ---
try:
    print(f"Navigating directly to PyPI search...")
    
    # This is the new URL for PyPI
    search_url = f"https://pypi.org/search/?q={quote_plus(SEARCH_TERM)}"
    
    driver.get(search_url)

    print("Search page loaded. Scraping results...")

    # --- NEW: ACCEPT COOKIE BANNER ---
    try:
        cookie_wait = WebDriverWait(driver, 5)
        cookie_button = cookie_wait.until(
            EC.element_to_be_clickable((By.ID, "accept-cookies"))
        )
        cookie_button.click()
        print("Cookie banner accepted.")
    except Exception as e:
        print("Cookie banner not found or already accepted.")
        pass # If the banner isn't there, just continue
    # ---------------------------------

except Exception as e:
    print(f"Error navigating to search page: {e}")
    driver.quit()
    exit()

# --- Step 5: Starts the Multi-Page Scraping Loop ---
packages_list = [] # This master list holds all packages
page_number = 1

# These are the new working selectors for PyPI
PACKAGE_CARD_SELECTOR = "a.package-snippet" # The whole card is the link
PACKAGE_TITLE_SELECTOR = "span.package-snippet__name"
PACKAGE_DESC_SELECTOR = "p.package-snippet__description"

# This is the new loop
while True:
    print(f"--- Scraping Page {page_number} ---")

    # --- Step 5a: Scrape Current Page ---
    try:
        # Waits for the first package card to be visible
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, PACKAGE_CARD_SELECTOR)))

        # Now that they're loaded, get all of them
        package_postings = driver.find_elements(By.CSS_SELECTOR, PACKAGE_CARD_SELECTOR)

        if not package_postings:
            print("No packages found on this page. Ending scrape.")
            break
            
        print(f"Found {len(package_postings)} packages on this page.")

        for package in package_postings:
            try:
                # Finds elements using the new selectors
                title = package.find_element(By.CSS_SELECTOR, PACKAGE_TITLE_SELECTOR).text.strip()
                description = package.find_element(By.CSS_SELECTOR, PACKAGE_DESC_SELECTOR).text.strip()
                
                # The whole "card" (the variable 'package') is the <a> tag, so href is retrieved
                url = package.get_attribute("href")
                
                packages_list.append([title, description, url])
                print(f"Successfully scraped: {title}")

            except Exception as e:
                # Skips any "empty" <li> elements or promoted listings
                print(f"DEBUG: Failed to scrape one card. Error: {e}")

    except Exception as e:
        print(f"Error scraping page {page_number}: {e}")
        break # Exits the loop if the page fails to load
    
    # --- Step 5b: Go to Next Page ---
    try:
        # --- POLITENESS DELAY ---
        sleep_time = random.randint(2, 5)
        print(f"Reading page... pausing for {sleep_time} seconds.")
        time.sleep(sleep_time)
        # ------------------------
        
        # --- SCROLL TO BOTTOM ---
        print("Scrolling to bottom of page...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5) # Gives the scroll a half-second to finish
        # ---------------------------

        # Gets a reference to the job cards scraped
        current_cards = driver.find_elements(By.CSS_SELECTOR, PACKAGE_CARD_SELECTOR)
        
        # Find the element (any tag: *) that contains the text "Next"
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
            "//*[contains(text(), 'Next') and contains(@class, 'button') and contains(@class, 'button-group__button')]"
        )))
        
        # Clicks it with Selenium's normal click
        next_button.click()
        # ---------------------------------
        
        page_number += 1
        
        # Waits for the old cards to go stale
        print("Going to next page... waiting for new packages to load...")
        wait.until(EC.staleness_of(current_cards[0]))

    except Exception as e:
        print(f"\n--- PAGINATION FAILED (THIS IS THE ERROR) --- \n{e}\n-------------------\n")
        break # Exits the while loop

# --- Step 6: Saves to CSV ---
print(f"\nScraping complete. Total packages found: {len(packages_list)}")

if packages_list:
    print(f"Saving {len(packages_list)} packages to pypi_packages.csv...")
    with open('pypi_packages.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Updates headers
        writer.writerow(["Package Name", "Description", "URL"]) # Header
        writer.writerows(packages_list)
    print("Done! Check pypi_packages.csv.")
else:
    print("No packages found to save.")

# --- Step 7: Finish! ---
driver.quit()

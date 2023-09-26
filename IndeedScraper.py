#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Latest version
# This code is written to let the user make a search on the job site indeed.com (swedish
# version) and will scrape the description and location for every job that appears for
# that search. The description and location will be saved in a list.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
import unicodedata 
import numpy as np

# Initialize lists to hold data
search_words = input("What do you want to search for: ")
job_data = []


# Use this if you have a PC
#driver = webdriver.Chrome()

url = "https://se.indeed.com/"

driver = webdriver.Chrome() # Use this if you have a macbook
# maximizing window size
driver.maximize_window()
driver.get(url) 

# Wait for cookie agreement form to pop up
time.sleep(2)

# Click agree on cookies
agree_button_xp = '//*[@id="onetrust-accept-btn-handler"]'
WebDriverWait(driver, 3)                                               # wait 3 sec 
element = driver.find_element(By.XPATH, agree_button_xp) # find the location of the bottom
element.click()

# Search for data by sending keys to text box
search_box_xp = '//*[@id="text-input-what"]'
text_search = driver.find_element(By.XPATH, search_box_xp)
text_search.send_keys(search_words)
time.sleep(2)

# Simulate pressing the Enter key
text_search.send_keys(Keys.RETURN)

time.sleep(2)
# Set initial zoom level
initial_zoom_level = 1
driver.execute_script(f"document.body.style.zoom = '{initial_zoom_level}'")

time.sleep(1)  # Wait for the page to load and dynamic content to update

nav_count = 0
last_page = False

while True:  # Keep this loop running until no "Next" button is found (i.e., reached the last page)
        
    # Close potential popup window
    try:
        popup_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mosaic-desktopserpjapopup"]/div[1]/button'))
        )
        popup_button.click()
        print("Popup closed.")
    except Exception as e:
        # No popup appeared
        print(f"No popup found: {e}")
            
    # Wait for the job listings to load and find them on the page
    to_click = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2 > a"))
    )
    
    location_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.companyLocation"))
    )
        
    for index, button in enumerate(to_click):
        try:
            # Get location for this job listing
            job_location = location_elements[index].text

            # Wait and then click the button
            time.sleep(2)
            ActionChains(driver).move_to_element(button).click().perform()

            # Continue with the rest of your existing code to scrape the job description
            time.sleep(1)
            soup = bs(driver.page_source, "lxml")
            key = "div.jobsearch-JobComponent-description"
            #containers.append(soup.select(key))
            description = " ".join([tag.text for tag in soup.select(key)]) if soup.select(key) else "Not provided"
            job_data.append({"description": description, "location": job_location})
        except Exception as e:
            print(f"Error scraping listing {index}: {e}")

        
    if last_page:
        break

        
    # Try to find navigation buttons
    try:
        # Find all navigation buttons
        nav_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "nav div a"))
        )
        if len(nav_buttons) < nav_count:
            last_page = True
        else:
            nav_count = len(nav_buttons)

        # Click the last button, which should be the "Next" button
        if nav_buttons:
            ActionChains(driver).move_to_element(nav_buttons[-1]).click().perform()
        else:
            print("No navigation buttons found.")
            break
    except Exception as e:
        # If there's an error (likely meaning that we're on the last page and there's no "Next" button)
        print(f"Reached the end of the pages or encountered an error: {e}")
        break
driver.quit()
print("Program ended.")


# In[5]:





# In[ ]:





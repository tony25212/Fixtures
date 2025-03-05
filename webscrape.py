import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
import csv
import os
import streamlit as st

# Define driver, options and service
URL = 'https://www.rfyl.org.uk/core/clubs.aspx'
edge_driver_path = "Web_driver/msedgedriver.exe"

# Set execute permission for msedgedriver.exe
os.chmod(edge_driver_path, 0o755)

# Set up the Edge service
service = Service(edge_driver_path)

# Set up Edge options
options = Options()
options.add_argument("--headless")  # Ensure GUI is off
options.add_argument("--disable-gpu")

# Launch Edge with the specified options
driver = webdriver.Edge(service=service, options=options)

# Load website
driver.get(URL)

"""
Logging in to a site

# Locate the needed fields
username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))
button_field = driver.find_element(By.ID, 'login')  # to prevent ads being clicked

# Fill in the data and action
username_field.send_keys('the user name')
password_field.send_keys('the PW')
driver.execute_script("arguments[0].click();", button_field)
"""

def scrape_data():
    # Locate and update the competition field
    competition_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'ddlCompetitions')))
    Select(competition_field).select_by_visible_text('Under 12 9v9 Division 10')

    # Wait for the second field to be refreshed
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//option[text()='CONSETT WARRIORS']")))

    # Locate and update the club field
    club_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'ddlClubs')))
    Select(club_field).select_by_visible_text('CONSETT WARRIORS')

    # Pause for page refresh
    time.sleep(1)

    # Wait for the table to be refreshed the first time
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='gvClubFixtures']/tbody/tr")))
    
    # Get the page source
    page_source = driver.page_source
    
    # Close the WebDriver
    driver.quit()
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Locate the table
    table = soup.find('table', {'id': 'gvClubFixtures'})
    
    # Read the rows of the table
    rows = table.find_all('tr')
    
    # Loop through the rows and print the data
    filename = "output.csv"

    # Open the CSV file once, outside the loop
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the header row if needed
        csvwriter.writerow(["Date", "Weekday", "Competition", "Home", "Away"])

        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 2:  # Ensure there are at least 3 cells in the row
                date_object = datetime.strptime(cells[0].text, '%d/%m/%y %H:%M')
                # Get the weekday (0=Monday, 6=Sunday)
                weekday = date_object.weekday()
                # Convert the weekday number to a name
                weekday_name = date_object.strftime('%A')
                fixtures = [cells[0].text, weekday_name, cells[1].text, cells[2].text, cells[4].text]
                csvwriter.writerow(fixtures)
    return True

if __name__ == '__main__':
    get_data = scrape_data()
    print(get_data)

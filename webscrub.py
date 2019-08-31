from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import os
import pandas

LINKEDIN_URL = "https://www.linkedin.com/search/results/people/"
COMPANY = input("Please enter company name: ")

# Get credentials
creds = open('credentials.txt', 'r').read().split("\n")
username = creds[0][9:].strip()
password = creds[1][9:].strip()

# Point driver to the current working directory
driver = webdriver.Chrome(executable_path="%s/chromedriver" % os.getcwd())

try:
    # Go to login page
    driver.get(LINKEDIN_URL)
    frame = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(frame)
    signInLink = driver.find_elements_by_class_name("sign-in-link")[0]
    signInLink.click()

    username_text_box = driver.find_element_by_id("username")
    username_text_box.send_keys(username)
    password_text_box = driver.find_element_by_id("password")
    password_text_box.send_keys(password + "\n")

    # Enter the company name into the filter
    time.sleep(3)
    current_companies_filter = driver.find_element_by_xpath("//*[contains(@class,'currentCompany')]")
    current_companies_filter.click()
    current_companies_filter_text = driver.find_element_by_xpath("//*[@placeholder='Add a current company']")
    current_companies_filter_text.send_keys(COMPANY)
    current_companies_filter_text.click()
    time.sleep(1)
    actions = ActionChains(driver)
    actions.send_keys(Keys.DOWN)
    actions.send_keys(Keys.RETURN)
    actions.perform()

    # Apply the filter
    apply_filter_buttons = driver.find_elements_by_xpath("//*[contains(@data-control-name, 'filter_pill_apply')]")
    apply_filter_buttons[2].click()

    # Determine number of pages to iterate through
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    page_numbers = driver.find_element_by_xpath("//*[contains(@class,'artdeco-pagination')]")
    numberHTML = page_numbers.get_attribute("outerHTML")
    numberSoup = BeautifulSoup(numberHTML, 'html.parser')
    numbersOnly = list(filter(lambda element : re.match("[1-9][0-9]*",
                              element.get_text()), numberSoup.find_all("span")))
    numbers = list(map(lambda number : int(number.get_text()), numbersOnly))
    total_pages = max(numbers)

    # Collect all employee information
    employeeList = []
    for i in range(total_pages):
        time.sleep(1)
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            results = driver.find_elements_by_xpath("//*[contains(@class, 'search-result__wrapper')]")
            for result in results:
                html = result.get_attribute("outerHTML")
                soup = BeautifulSoup(html, 'html.parser')

                # Find all informational fields in the html
                soups = list(filter(lambda s: re.match(".*ltr.*|.*actor-name.*", str(s)), soup.find_all("span")))
                info = list(map(lambda s : s.get_text(), soups))

                # Add employee info to a list
                employeeList.append({"name" : info[len(info) - 3].strip(),
                                     "role" : info[len(info) - 2].strip(),
                                     "location": info[len(info) - 1].strip()})

            # Move to next page
            next_page_link = driver.find_element_by_xpath("//button[@aria-label='Next']")
            next_page_link.click()
        except Exception as e:
            print(e)

    # Export data to excel
    employeeData = pandas.DataFrame(employeeList)
    employeeData.to_excel("output.xlsx")

    driver.quit()
except Exception as e:
    print(e)
    driver.quit()

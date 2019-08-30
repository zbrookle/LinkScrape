from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import inspect
import os
import pandas

LINKEDIN_URL = "https://www.linkedin.com/search/results/people/"
COMPANY = "Disney Streaming Services"

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

    # Get the resulting employees
    employeeList = []
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    results = driver.find_elements_by_xpath("//*[contains(@class, 'search-result__wrapper')]")
    results = results[:1]
    for result in results:
        html = result.get_attribute("outerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find("span", class_ = "name actor-name").get_text()
        info = list(map(lambda x : x.get_text(), soup.find_all("span")))

        # Add employee info to a list
        employeeList.append({"name" : name, "role" : info[7], "location": info[8]})

    employeeData = pandas.DataFrame(employeeList)
    print(employeeData)
    driver.quit()
except Exception as e:
    print(e)
    driver.quit()



# <button data-control-name="filter_pill_apply" id="ember166" class="facet-collection-list__apply-button ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view" type="button"><!---->
# <span class="artdeco-button__text">
#     Apply
# </span></button>

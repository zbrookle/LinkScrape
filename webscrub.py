from selenium import webdriver
# from selenium.webdriver.common.keys import keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import inspect
import os

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

    time.sleep(2)
    current_companies_filter = driver.find_element_by_xpath("//*[contains(@class,'currentCompany')]")
    current_companies_filter.click()
    current_companies_filter_text = driver.find_element_by_xpath("//*[@placeholder='Add a current company']")
    current_companies_filter_text.send_keys(COMPANY)
    actions = ActionChains(driver)
    actions.send_keys(COMPANY)
    actions.perform()
    # driver.quit()
except Exception as e:
    print(e)
    driver.quit()

# # print(signInLink)
# <button aria-label="Current companies filter. Clicking this button displays all Current companies filter options." aria-expanded="false" aria-controls="current-companies-facet-values" id="ember158" class="search-s-facet__button artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--2 artdeco-button--secondary ember-view" type="button">  <li-icon aria-hidden="true" type="caret-filled-down-icon" class="artdeco-button__icon" size="small"><svg viewBox="0 0 24 24" width="24px" height="24px" x="0" y="0" preserveAspectRatio="xMinYMin meet" class="artdeco-icon" focusable="false"><path d="M8.8,10.66L14,5.12A0.07,0.07,0,0,0,13.93,5H2.07A0.07,0.07,0,0,0,2,5.12L7.2,10.66A1.1,1.1,0,0,0,8.8,10.66Z" class="small-icon" style="fill-opacity: 1"></path></svg></li-icon>
#
# <span class="artdeco-button__text">
#     Current companies
# </span></button>
#
# <input placeholder="Add a current company" role="combobox" aria-autocomplete="list" aria-activedescendant="" aria-expanded="false" aria-owns="" aria-label="Add a current company" type="text">


# <input class="cell-body-textinput" autocomplete="off"
# data-type-ahead="true"
# data-email-domains="gmail.com,yahoo.com,hotmail.com,aol.com,comcast.net,sbcglobal.net,msn.com,verizon.net,cox.net"
# type="email" autocapitalize="off"
# aria-required="true" id="join-email"
# name="emailAddress" placeholder="Email" value="">

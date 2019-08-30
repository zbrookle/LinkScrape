from selenium import webdriver
# from selenium.webdriver.common.keys import keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import inspect
import os

LINKEDIN_URL = "https://www.linkedin.com/search/results/people/"
COMPANY = ""

# Point driver to the current working directory
driver = webdriver.Chrome(executable_path="%s/chromedriver" % os.getcwd())

# Set URL to search for people
driver.get(LINKEDIN_URL)

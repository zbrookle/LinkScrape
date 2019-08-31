# Intro

Sometimes when applying for jobs it can be really hard to find the recruiting manager to address your cover letter to. Using conventional search engine techniques it can be nearly impossible! To solve this issue for myself and others during job searches, I created this webscrubbing code to help people find the employees that they need to connect with by webscrubbing the company's listed employees on LinkedIn.

# Non Native Packages Required

* selenium
* bs4
* pandas
* openpyxl

# Set up

1. Make sure that you have google chrome installed and ensure that the chromedriver
version is the same as your chrome installation. To ensure this go to this website:
https://chromedriver.storage.googleapis.com/index.html?path=76.0.3809.126/
and download the appropriate version. You can find your chrome version in Settings - About Google Chrome.

2. Next, add your LinkedIn username and password to the credentials file so that
the application can login. The application will not make any posts or transfer any data.

3. Be sure that you have all of the above python packages installed.

# Warnings

1. LinkedIn limits the number of searches you can do per month so be sure not to go too crazy with this tool.

2. If the tool isn't working, it may be due to your computer or internet speed. If this happens increase the timer variable until the application functions properly.

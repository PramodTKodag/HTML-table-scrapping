from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
import pandas as pd

chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)
url = "https://www.w3schools.com/html/html_tables.asp"
r = driver.get(url)

tbl = driver.find_element_by_xpath("""//*[@id="customers"]""").get_attribute('outerHTML')

df  = pd.read_html(tbl)

print(df)
import os
import ast
import ConfigParser

from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

config = ConfigParser.ConfigParser()

#Load Website
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.reservecalifornia.com/CaliforniaWebHome/')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'txtSearchparkautocomplete')))

#Go through first screen
driver.find_element_by_id("txtSearchparkautocomplete").send_keys("Angel Island SP", Keys.ARROW_DOWN, Keys.RETURN)
driver.find_element_by_id("mainContent_txtArrivalDate").click()
driver.find_element_by_id("mainContent_txtArrivalDate").send_keys(Keys.RETURN)
Select(driver.find_element_by_id("ddlHomeNights")).select_by_value("1")
driver.find_element_by_class_name("home_btn_go").click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn_green")))

#Go to angel island
driver.find_elements_by_class_name("btn_green")[0].click()

#Manuever through each area and find opening
for area in ["406", "408", "409"]:#Areas corresponding to campgrounds
	Select(driver.find_element_by_id("ddlFacility")).select_by_value(area)
	first_day = datetime.today() + timedelta(days = 2)
	saturday = first_day + timedelta(days = 6 if first_day.weekday() == 6 else 5 - first_day.weekday())
	saturday = saturday.strftime('%m/%d/%Y')

	driver.find_element_by_id("mainContent_txtDateRange").clear()
	driver.find_element_by_id("mainContent_txtDateRange").send_keys(saturday, Keys.RETURN)
	driver.find_element_by_class_name("ui-datepicker-trigger").click()
	driver.implicitly_wait(2)
	driver.find_element_by_class_name("ui-state-active").click()



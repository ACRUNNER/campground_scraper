import os
import ast
#import ConfigParser
import time
from random import random

from datetime import datetime, timedelta, date

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

#config = ConfigParser.ConfigParser()

# def check_errors(id):
# 	total_retries = 5
# 	num_retries = 0
# 	site_ready = false
# 	while site_ready == False:
# 		error = driver.find_element_by_id()
# 		if error != None:
# 			if num_retries < total_retries:
# 				print('Error: ' + error.text)
# 				num_retries += 1
# 				driver.refresh()
# 			else:
# 				print 'Failed'
# 				return False
# 		else:
# 			site_ready = true
# 	return True
class Checker:
	def __init__(self):
		self.driver = None

	def initiate_webdriver(self):
		options = webdriver.ChromeOptions()
		options.add_argument("window-size=1920,1080");
		options.add_argument('headless')
		options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
		options.binary_location = GOOGLE_CHROME_PATH
		self.driver = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH, chrome_options = options)


	def go_to_angel_island(self):
		#Go to website
		self.driver.get('https://www.reservecalifornia.com/CaliforniaWebHome/')
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'txtSearchparkautocomplete')))

		#Go through first screen
		self.driver.find_element_by_id("txtSearchparkautocomplete").send_keys("Angel Island SP", Keys.ARROW_DOWN, Keys.RETURN)
		self.driver.find_element_by_id("mainContent_txtArrivalDate").click()
		self.driver.find_element_by_id("mainContent_txtArrivalDate").send_keys(Keys.RETURN)
		Select(self.driver.find_element_by_id("ddlHomeNights")).select_by_value("1")
		self.driver.find_element_by_class_name("home_btn_go").click()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn_green")))

		#Go to angel island
		self.driver.find_elements_by_class_name("btn_green")[0].click()

	def check_saturdays(self):	

		#Manuever through each area and find opening
		areas = {
			'406': 'East Bay (sites 1-3)',
			'408': 'Ridge (sites 4-6',
			'409': 'Sunrise (sites 7-9)',
		}
		for area in ["406", "408", "409"]:#Areas corresponding to campgrounds
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ddlFacility")))
			Select(self.driver.find_element_by_id("ddlFacility")).select_by_value(area)
			first_day = datetime.today().date() + timedelta(days = 2)
			saturday = first_day + timedelta(days = 6 if first_day.weekday() == 6 else 5 - first_day.weekday())
			last_saturday = saturday - timedelta(days=7)
			saturday_str = saturday.strftime('%m/%d/%Y')

			self.driver.find_element_by_id("mainContent_txtDateRange").clear()
			self.driver.find_element_by_id("mainContent_txtDateRange").send_keys(saturday_str, Keys.RETURN)
			self.driver.find_element_by_class_name("ui-datepicker-trigger").click()
			self.driver.find_element_by_class_name("ui-state-active").click()

			while(last_saturday + timedelta(days=7) == saturday):
				time.sleep(1 + random() * 1)
				ids = [
					"ctl00_ctl05",
					"ctl00_ctl26",
					"ctl00_ctl47"
				]
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, ids[0])))
				for id in ids:
					if not "red_brd_box" in self.driver.find_element_by_id(id).get_attribute("class"):
						return [saturday_str, areas[area]]
				self.driver.find_element_by_id("NextDays").click()

				last_saturday = saturday
				saturday_str = self.driver.find_element_by_id("mainContent_txtDateRange").get_attribute('value')
				saturday = datetime.strptime(saturday_str, "%m/%d/%Y").date()
		return 	None

	def check_campsites(self):
		self.initiate_webdriver()
		self.go_to_angel_island()
		result = self.check_saturdays()
		self.driver.quit()
		return result

	










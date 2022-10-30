from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import configparser
import csv

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

driver = webdriver.Firefox()

#log into allpro website and waiting for page to load
driver.get("https://warehouse.allprocorp.com/midwest/customer/account/login/")

driver.find_element_by_xpath("//*[@id='email']").send_keys(config['DEFAULT']['username'])
driver.find_element_by_xpath("//*[@id='pass']").send_keys(config['DEFAULT']['password'])

driver.find_element_by_xpath("//*[@id='send2']").submit()

WebDriverWait(driver, 10).until(lambda x: "Midwest Homepage" in driver.title)
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

#navigating to order page and waiting for page to load
driver.get("https://warehouse.allprocorp.com/midwest/quickorder")

WebDriverWait(driver, 10).until(lambda x: "Quick order" in driver.title)
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

#setting up cart for the amount of items needed
#this needed to be in it's own open block or else it would hang after adding rows
with open('order.csv', newline='') as csvfile:
    row_count = csv.reader(csvfile, delimiter=',', quotechar='|')
    rows = sum(1 for line in row_count)
    if rows > 4:
        for x in range(0,(rows-4)):
            driver.find_element_by_xpath("//*[@id='search-table']/tbody/tr[" + str(5+x) + "]/td/label[1]").click()

#steps through order csv for SKUs and quantites
with open('order.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    i = 1
    for row in spamreader:
        #add sku to text box
        driver.find_element_by_xpath("//*[@id='pcode" + str(i) + "']").send_keys(str(row[0]))

        #waiting for sku popup, will not post unless popup is selected and clicked
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='product_" + str(i) + "']/td[2]/div/div[1]"))
        )
        element.click()

        #clears auto-fill from quantity box and adds quantity from text box
        qty = driver.find_element_by_xpath("//*[@id='qty" + str(i) + "']")
        qty.clear()
        qty.send_keys(str(row[1]))

        i+=1

#clicking add all to cart button
driver.find_element_by_class_name("add-all").click()
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By  # allow searching for things using specific parameters
from selenium.webdriver.support.ui import WebDriverWait  # allow wait for a page to load
from selenium.webdriver.support import expected_conditions as EC


class FlightSearch:

    def set_up_oneway(self, url):
        option = webdriver.ChromeOptions()
        option.add_argument(" - incognito")
        driver = webdriver.Chrome(executable_path='/Users/SHAWN/PycharmProjects/chromedriver', chrome_options=option)
        driver.get(url)

        # try to click on the language selection popup, choose English.
        BUTTON_XPATH = '//*[@id="enCAEdition"]'
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, BUTTON_XPATH)))
        element = driver.find_element_by_xpath(BUTTON_XPATH)
        element.click()

        # then choose to select one way.
        one_way_xpath = '//*[@id="oneWay"]'
        # wait2 = WebDriverWait(driver,20)
        # element = wait2.until(EC.element_to_be_clickable((By.XPATH, one_way_xpath)))
        element = driver.find_element_by_xpath(one_way_xpath)
        element.click()


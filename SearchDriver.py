import time
import datetime
from selenium import webdriver
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By  # allow searching for things using specific parameters
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # allow wait for a page to load


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

        return driver

        # Note that the following definition has to have airport names in acronyms as strings.

    def oneway_search(self, driver, depart, dest, day, month, year):
        depart_xpath = '//*[@id="origin_O_0"]'
        dest_xpath = '//*[@id="destination_O_0"]'
        date_xpath = '//*[@id="returnDateLabel"]/div[1]/div'
        empty_xpath = '//*[@id="bookingMagnetForm"]/fieldset/div[2]/div[1]'
        search_xpath = '//*[@id="magnet-fields-wrapper"]/div[3]/div[3]/input'

        # To edit the date
        date_field = driver.find_element_by_xpath(date_xpath)
        date_field.click()

        # find the correct table (month + year)
        month_now = datetime.datetime.now().month
        year_now = datetime.datetime.now().year
        click_num = (year - year_now) * 12 + (month - month_now)
        print(click_num)
        for i in range(0, click_num):
            time.sleep(0.5)
            next_field = driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/a[2]')
            next_field.click()

        # select the correct date
        date_button_xpath = (
            '//td[@data-handler="selectDay"][@data-date="{0}"][@data-month="{1}"][@data-year="{2}"]/span[1]'
        ).format(str(day), str(month - 1), str(year))
        general_button = '//*[@id="ui-datepicker-div"]/a[2]/span'
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, general_button)))
        button = driver.find_element_by_xpath(date_button_xpath)
        action_chains.ActionChains(driver).move_to_element(button).click().perform()
        button.click()

        # to edit depart, dest fields
        empty_field = driver.find_element_by_xpath(empty_xpath)
        depart_field = driver.find_element_by_xpath(depart_xpath)
        depart_field.send_keys(depart)
        time.sleep(1)
        depart_field.send_keys(keys.Keys.ENTER)

        dest_field = driver.find_element_by_xpath(dest_xpath)
        dest_field.send_keys(dest)
        time.sleep(1)
        dest_field.send_keys(keys.Keys.ENTER)

        # Press search
        search_field = driver.find_element_by_xpath(search_xpath)
        search_field.click()

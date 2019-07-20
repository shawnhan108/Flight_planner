import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, TimeoutException
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By  # allow searching for things using specific parameters
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # allow wait for a page to load


class SearchDriver:

    def set_up(self, url):
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

        return driver

        # Note that the following definition has to have airport names in acronyms as strings.

    def oneway_search(self, driver, depart, dest, day, month, year):
        # choose to select one way.
        one_way_xpath = '//*[@id="oneWay"]'
        element = driver.find_element_by_xpath(one_way_xpath)
        element.click()

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
        for i in range(0, click_num):
            BUTTON_XPATH = '//*[@id="ui-datepicker-div"]/a[2]'
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, BUTTON_XPATH)))
            element = driver.find_element_by_xpath(BUTTON_XPATH)
            element.click()

        # select the correct date
        if (day < 10):
            day = '0' + str(day)

        time.sleep(1.5)
        date_button_xpath = (
            '//td[@data-handler="selectDay"][@data-date="{0}"][@data-month="{1}"][@data-year="{2}"]/span[1]'
        ).format(day, str(month - 1), str(year))
        general_button = '//*[@id="ui-datepicker-div"]/a[2]/span'
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, general_button)))
        button = driver.find_element_by_xpath(date_button_xpath)
        action_chains.ActionChains(driver).move_to_element(button).click().perform()

        # to edit depart, dest fields
        empty_field = driver.find_element_by_xpath(empty_xpath)
        depart_field = driver.find_element_by_xpath(depart_xpath)
        for i in range(0, 10):
            depart_field.send_keys(keys.Keys.BACKSPACE)
        depart_field.send_keys(depart)
        time.sleep(1)
        depart_field.send_keys(keys.Keys.ENTER)

        dest_field = driver.find_element_by_xpath(dest_xpath)
        for i in range(0, 10):
            dest_field.send_keys(keys.Keys.BACKSPACE)
        dest_field.send_keys(dest)
        time.sleep(1)
        dest_field.send_keys(keys.Keys.ENTER)

        # Press search
        search_field = driver.find_element_by_xpath(search_xpath)
        search_field.click()

        return driver

    def round_trip_search(self, driver, depart, dest, day_from, month_from, year_from, day_back, month_back, year_back):
        depart_xpath = '//*[@id="origin_R_0"]'
        dest_xpath = '//*[@id="destination_R_0"]'
        date_xpath = '//*[@id="returnDateLabel"]/span[1]'
        empty_xpath = '//*[@id="bookingMagnetForm"]/fieldset/div[2]'
        search_xpath = '//*[@id="magnet-fields-wrapper"]/div[3]/div[3]/input'

        # To edit the date
        date_field = driver.find_element_by_xpath(date_xpath)
        date_field.click()

        # find the correct table (month + year)
        month_now = datetime.datetime.now().month
        year_now = datetime.datetime.now().year
        click_num = (year_from - year_now) * 12 + (month_from - month_now)
        for i in range(0, click_num):
            BUTTON_XPATH = '//*[@id="ui-datepicker-div"]/a[2]'
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, BUTTON_XPATH)))
            element = driver.find_element_by_xpath(BUTTON_XPATH)
            element.click()

        # select the correct date
        if (day_from < 10):
            day_from = '0' + str(day_from)

        time.sleep(1.5)
        date_button_xpath = (
            '//td[@data-handler="selectDay"][@data-date="{0}"][@data-month="{1}"][@data-year="{2}"]/span[1]'
        ).format(str(day_from), str(month_from - 1), str(year_from))
        general_button = '//*[@id="ui-datepicker-div"]/a[2]/span'
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, date_button_xpath)))
        # button2 = driver.find_element_by_xpath(date_button_xpath)
        # action_chains.ActionChains(driver).move_to_element(button).click().perform()
        # button2.click()
        element = driver.find_element_by_xpath(date_button_xpath)
        webdriver.ActionChains(driver).move_to_element(element).click(element).perform()

        # find the correct table for return (month + year)
        click_more = (year_back - year_from) * 12 + (month_back - month_from)
        for i in range(0, click_more):
            BUTTON_XPATH = '//*[@id="ui-datepicker-div"]/a[2]'
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, BUTTON_XPATH)))
            element = driver.find_element_by_xpath(BUTTON_XPATH)
            element.click()

        # select the correct date
        if (day_back < 10):
            day_back = '0' + str(day_back)

        time.sleep(1.5)
        date_button_xpath = (
            '//td[@data-handler="selectDay"][@data-date="{0}"][@data-month="{1}"][@data-year="{2}"]/span[1]'
        ).format(str(day_back), str(month_back - 1), str(year_back))
        general_button = '//*[@id="ui-datepicker-div"]/a[2]/span'
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, date_button_xpath)))
        # button2 = driver.find_element_by_xpath(date_button_xpath)
        # action_chains.ActionChains(driver).move_to_element(button).click().perform()
        # button2.click()
        element = driver.find_element_by_xpath(date_button_xpath)
        webdriver.ActionChains(driver).move_to_element(element).click(element).perform()

        # Confirm the date by clicking the red "select" button
        date_select_xpath = '//*[@id="calendarSelectActionBtn"]'
        date_select_field = driver.find_element_by_xpath(date_select_xpath)
        time.sleep(1.5)
        date_select_field.click()

        # to edit depart, dest fields
        empty_field = driver.find_element_by_xpath(empty_xpath)
        depart_field = driver.find_element_by_xpath(depart_xpath)
        time.sleep(1)
        for i in range(0, 10):
            depart_field.send_keys(keys.Keys.BACKSPACE)
        depart_field.send_keys(depart)
        depart_field.send_keys(keys.Keys.ENTER)

        dest_field = driver.find_element_by_xpath(dest_xpath)
        dest_field.send_keys(dest)
        time.sleep(1)
        for i in range(0, 10):
            dest_field.send_keys(keys.Keys.BACKSPACE)
        dest_field.send_keys(keys.Keys.ENTER)

        # Press search
        search_field = driver.find_element_by_xpath(search_xpath)
        search_field.click()

        return driver

    def extract_info_oneway(self, driver):
        time.sleep(5)
        # extract flight price
        all_prices = driver.find_elements_by_class_name('fare-details-section')
        price_list = []
        for price in all_prices:
            price_list.append(price.text)

        # extract flight time
        all_itinerary_time = driver.find_elements_by_class_name('flight-row-head')
        itinerary_time_list = []
        for itinerary in all_itinerary_time:
            temp = str(itinerary.text)
            depart_time = temp[0:temp.find("\n")]

            if temp[temp.find("arriving"):] != "":
                duration = temp[6:-6]
                dest_time = temp[-5:]
            elif temp[temp.find("\n") + 1:temp.find("m") + 1] == "":
                duration = temp[6:-6]
                dest_time = temp[-5:]
            else:
                duration = temp[temp.find("\n") + 1:temp.find("m") + 1]
                dest_time = temp[temp.find("m") + 3:]

            itinerary_time_list.append([depart_time, duration, dest_time])

        # extract flight locations
        all_itinerary_location = driver.find_elements_by_class_name('top-section')
        itinerary_locations_list = []
        for itinerary in all_itinerary_location:
            temp = str(itinerary.text)
            depart = temp[0:temp.find("\n")]
            dest = temp[temp.find("\n") + 1:]
            if dest != dest[dest.find("\n") + 1:]:
                connection = dest[dest.find("\n") + 1:]
                dest = dest[0:dest.find("\n")]
                itinerary_locations_list.append([depart, dest, connection])
            else:
                itinerary_locations_list.append([depart, dest])

        # organize all information together.
        flights = []
        updated_price_list = []
        for items in price_list:
            if items[0] == "E":
                if len(updated_price_list) == 0 or len(updated_price_list[-1]) == 2:
                    substring = [items[items.find("$") + 1:items.find("\n.")]]
                    updated_price_list.append(substring)
                else:
                    updated_price_list[-1].append('NULL')
                    substring = [items[items.find("$") + 1:items.find("\n.")]]
                    updated_price_list.append(substring)
            elif len(updated_price_list[-1]) == 1:
                substring = items[items.find("$") + 1:items.find("\n.")]
                updated_price_list[-1].append(substring)
            else:
                substring = ['NULL', items[items.find("$") + 1:items.find("\n.")]]
                updated_price_list.append(substring)

        for i in range(0, len(all_itinerary_location)):
            temp = [itinerary_locations_list[i], itinerary_time_list[i], updated_price_list[i]]
            flights.append(temp)

        return flights

    def extract_info_roundtrip(self, driver):

        one_way_flights = SearchDriver.extract_info_oneway(self, driver)
        time.sleep(5)

        next_xpath = '//*[@id="cabinBtnECO00"]'
        turn_page_xpath = \
            '//*[@id="main-fare-element-container"]/div/div/div[1]/fare-family-element/div[3]/div[1]/button'
        second_turn_page_xpath = \
            '//*[@id="main-fare-element-container"]/div/div/div[2]/fare-family-element/div[3]/div[1]/button'
        STAR_XPATH = '//*[@id="fareSubContent_0"]/ul/li[3]/span[1]'
        element = driver.find_element_by_xpath(next_xpath)
        element.click()

        # go to the next page
        try:
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, STAR_XPATH)))
            element = driver.find_element_by_xpath(turn_page_xpath)
            element.click()

            try:
                accept_xpath = '//*[@id="ulccLightBoxBody"]/div[2]/div[2]/div[1]/button'
                wait = WebDriverWait(driver, 20)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, accept_xpath)))
                element = driver.find_element_by_xpath(accept_xpath)
                element.click()
            except ElementNotVisibleException as e:
                pass

        except NoSuchElementException as es:
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, STAR_XPATH)))
            element = driver.find_element_by_xpath(second_turn_page_xpath)
            element.click()

            try:
                accept_xpath = '//*[@id="ulccLightBoxBody"]/div[2]/div[2]/div[1]/button'
                wait = WebDriverWait(driver, 20)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, accept_xpath)))
                element = driver.find_element_by_xpath(accept_xpath)
                element.click()
            except ElementNotVisibleException as e:
                pass
            except TimeoutException as ex:
                pass

        # now extract the return flight info.
        time.sleep(5)
        return_flights = SearchDriver.extract_info_oneway(self, driver)

        return_list = [one_way_flights, return_flights]
        return return_list

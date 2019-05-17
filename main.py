import time

import SearchDriver

p = SearchDriver.FlightSearch()
driver = p.set_up_oneway("https://www.aircanada.com/ca/en/aco/home.html")
p.oneway_search(driver, 'YYZ', 'YOW', 26, 7, 2019)

time.sleep(10)
driver.quit()

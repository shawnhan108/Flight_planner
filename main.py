import SearchDriver

p = SearchDriver.FlightSearch()
driver = p.set_up("https://www.aircanada.com/ca/en/aco/home.html")
# p.oneway_search(driver, 'YYZ', 'YOW', 29, 7, 2019)
p.round_trip_search(driver, 'YYZ', 'YOW', 6, 7, 2019, 8, 8, 2019)

# quit
driver.quit()

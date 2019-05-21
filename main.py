import SearchDriver


# depart and dest are strings, rest are integers. year = 4 digits, day/month 1 or 2 digits
def retrieve_oneway(depart, dest, day, month, year):
    p = SearchDriver.FlightSearch()
    driver = p.set_up("https://www.aircanada.com/ca/en/aco/home.html")
    driver = p.oneway_search(driver, depart, dest, day, month, year)
    result = p.extract_info_oneway(driver)
    driver.quit()
    return result


def retrieve_roundtrip(depart, dest, depart_day, depart_month, depart_year, dest_day, dest_month, dest_year):
    p = SearchDriver.FlightSearch()
    driver = p.set_up("https://www.aircanada.com/ca/en/aco/home.html")
    driver = p.round_trip_search(driver, depart, dest, depart_day, depart_month, depart_year, dest_day, dest_month,
                                 dest_year)
    result = p.extract_info_roundtrip(driver)
    driver.quit()
    return result

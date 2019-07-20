import datetime

import mysql.connector

from load_app import App
from search_driver import SearchDriver


class FlightSearch(App):
    def retrieve_oneway(self, flight_id: int):
        """
        retrieves info in a flight_info list for one-way flights
        """
        flight = self.flights_db.flights_dict[flight_id]
        month = flight.depart_date.split('/')[0]
        day = flight.depart_date.split('/')[1]
        year = flight.depart_date.split('/')[2]

        p = SearchDriver()
        driver = p.set_up("https://www.aircanada.com/ca/en/aco/home.html")
        driver = p.oneway_search(driver, flight.depart, flight.dest, day, month, year)
        result = p.extract_info_oneway(driver)
        driver.quit()
        return result

    def retrieve_roundtrip(self, flight_id: int):
        """
        retrieves info in a flight_info list for round_trip flights
        """
        flight = self.flights_db.flights_dict[flight_id]
        depart_month = flight.depart_date.split('/')[0]
        depart_day = flight.depart_date.split('/')[1]
        depart_year = flight.depart_date.split('/')[2]
        dest_month = flight.return_date.split('/')[0]
        dest_day = flight.return_date.split('/')[1]
        dest_year = flight.return_date.split('/')[2]

        p = SearchDriver()
        driver = p.set_up("https://www.aircanada.com/ca/en/aco/home.html")
        driver = p.round_trip_search(driver, flight.depart, flight.dest, depart_day, depart_month, depart_year,
                                     dest_day, dest_month, dest_year)
        result = p.extract_info_roundtrip(driver)
        driver.quit()
        return result

    def apply_filters(self, flight_info, flight_id: int):
        """
        Applies filters in filters field to flight_info list.
        :param flight_info: a list of flight information extracted by selenium web scraper
        :param flight_id:
        :return: a list of flight info that satisfies the criteria described in the filters.
        """
        flight = self.flights_db.flights_dict[flight_id]

        if flight.filters.day_filter_switch():
            day, month, year = (int(x) for x in flight.depart_date.split('/'))
            flight_day = str(datetime.date(year, month, day))
            for days in flight.filters.day_filter.split(';'):
                if flight_day == days:
                    flight_info = []
                    return flight_info

        if flight_info & flight.filters.depart_time_filter_switch():
            start = datetime.datetime.strptime(flight.filters.depart_time_filter.split(';')[0], '%H:%M').time()
            end = datetime.datetime.strptime(flight.filters.depart_time_filter.split(';')[1], '%H:%M').time()
            if start < end:
                flight_info = list(filter(
                    lambda x: (datetime.datetime.strptime(x[1][0], '%H:%M').time() > start) and (
                            datetime.datetime.strptime(x[1][0], '%H:%M').time() < end), flight_info))
            else:
                flight_info = list(filter(lambda x: (datetime.datetime.strptime(x[1][0], '%H:%M').time() > start) or (
                        datetime.datetime.strptime(x[1][0], '%H:%M').time() < end), flight_info))

        if flight_info & flight.filters.max_duration_filter_switch():
            time_limit = datetime.datetime.strptime(flight.filters.max_duration_filter, '%H:%M').time()

            flight_info = list(filter(
                lambda x: (datetime.datetime.strptime(
                    x[1][1][x[1][1].find("- ") + 2:][0:1] + ':' + x[1][1][x[1][1].find("- ") + 2:][3:5],
                    '%H:%M').time() < time_limit), flight_info))

        if flight_info & flight.filters.price_amount_filter_switch():
            if flight.filters.price_amount_filter.split(';')[0] == 'Economy':
                flight_info = list(
                    filter(
                        lambda x: x[2][1] != 'NULL' and int(x[2][0]) <= int(
                            flight.filters.price_amount_filter.split(';')[1]),
                        flight_info))
            else:
                flight_info = list(
                    filter(
                        lambda x: x[2][1] != 'NULL' and int(x[2][1]) <= int(
                            flight.filters.price_amount_filter.split(';')[1]),
                        flight_info))

        return flight_info

    def store_info(self, flight_id: int):

        def find_min(flight_info_list, class_type):
            if class_type == 'economy':
                min_price = int(flight_info_list[0][2][0])
                for item in flight_info_list:
                    if item[2][0] != 'NULL' and int(item[2][0]) < min_price:
                        min_price = int(item[2][0])
                    else:
                        continue
            else:
                min_price = int(flight_info_list[0][2][1])
                for item in flight_info_list:
                    if item[2][1] != 'NULL' and int(item[2][1]) < min_price:
                        min_price = int(item[2][1])
                    else:
                        continue
            return min_price

        def find_max(flight_info_list, class_type):
            if class_type == 'economy':
                max_price = int(flight_info_list[0][2][0])
                for item in flight_info_list:
                    if item[2][0] != 'NULL' and int(item[2][0]) > max_price:
                        max_price = int(item[2][0])
                    else:
                        continue
            else:
                max_price = int(flight_info_list[0][2][1])
                for item in flight_info_list:
                    if item[2][1] != 'NULL' and int(item[2][1]) > max_price:
                        max_price = int(item[2][1])
                    else:
                        continue
            return max_price

        def find_avg(flight_info_list, class_type):
            if class_type == 'economy':
                sum = 0
                for item in flight_info_list:
                    if item[2][0] != 'NULL':
                        sum += int(item[2][0])
            else:
                sum = 0
                for item in flight_info_list:
                    if item[2][1] != 'NULL':
                        sum += int(item[2][1])
            return sum

        flight = self.flights_db.flights_dict[flight_id]
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        # search the flight information from web.
        if flight.return_date:
            flight_info = self.retrieve_roundtrip(flight_id)
        else:
            flight_info = self.retrieve_oneway(flight_id)

        # apply filters to the flight_info.
        flight_info = self.apply_filters(flight_info, flight_id)

        # TODO: notify user if there are flights that satisfy their requirements, using price analysis

        # store flight_info into db.
        # table_name columns: Depart, Dest, Date, min_econ, min_bus, avg_econ, avg_bus, track_date
        username = self.flights_db.flights_dict[flight_id][0]
        self.users_flights_dict[username].flights_dict[flight_id].commit_flight_db(find_min(flight_info, 'economy'),
                                                                                   find_min(flight_info, 'business'),
                                                                                   find_avg(flight_info, 'economy'),
                                                                                   find_avg(flight_info, 'business'))
        del flight_info
        mycursor.close()

import datetime
from datetime import datetime

import mysql.connector

from SearchDriver import retrieve_oneway


class Flight_oneway:
    flight_type = 'oneway'
    track_counter = 0

    # Initializer with attributes
    # all fields are strings, depart_date in the form of DD/MM/YYYY
    def __init__(self, username, depart, dest, depart_date):
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='flightplanner',
            database='FP_database'
        )
        my_cursor = mydb.cursor()
        self.username = username
        self.track_id = 1 + my_cursor.execute('SELECT MAX(track_id) FROM User_info')
        self.table_name = 'tb_' + str(self.track_id)
        self.depart = depart
        self.dest = dest
        self.depart_date = depart_date
        self.filters = Filters()
        self.notifications = Notification()

    # store an object information in table User_info
    def push_info(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='flightplanner',
            database='FP_database'
        )
        my_cursor = mydb.cursor()

        # User_info columns: Username, track_id, table_name, trip_type, depart, dest
        push_command = 'INSERT INTO User_info VALUES ({0}, {1}, {2}, {3},{4},{5},{6}, {7}, {8}, {9}, {10}, {11}, {12});' \
            .format(self.username, self.track_id, self.table_name, self.flight_type, self.depart, self.dest,
                    self.filters.day_filter, self.filters.depart_time_filter, self.filters.max_duration_filter,
                    self.filters.price_amount_filter, self.notifications.amount, self.notifications.diff,
                    self.notifications.trend
                    )
        my_cursor.execute(push_command)

        # setup a unique table for the flight, using table_name
        # table_name columns: Depart, Dest, Date, min_econ, min_bus, avg_econ, avg_bus, track_date
        set_up_command = 'CREATE TABLE {0} (Depart varchar(255), Dest varchar(255), Date varchar(255), ' \
                         'min_econ int, min_bus int, avg_econ int, avg_bus int, track_date varchar(255);'.format \
            (self.table_name)
        my_cursor.execute(set_up_command)

    def apply_filters(self, flight_info):
        if self.filters.day_filter_switch():
            day, month, year = (int(x) for x in self.depart_date.split('/'))
            flight_day = str(datetime.date(year, month, day))
            for days in self.filters.day_filter.split(';'):
                if flight_day == days:
                    flight_info = []
                    return flight_info

        if flight_info & self.filters.depart_time_filter_switch():
            start = datetime.strptime(self.filters.depart_time_filter.split(';')[0], '%H:%M').time()
            end = datetime.strptime(self.filters.depart_time_filter.split(';')[1], '%H:%M').time()
            if start < end:
                flight_info = list(filter(
                    lambda x: (datetime.strptime(x[1][0], '%H:%M').time() > start) and (
                            datetime.strptime(x[1][0], '%H:%M').time() < end), flight_info))
            else:
                flight_info = list(filter(lambda x: (datetime.strptime(x[1][0], '%H:%M').time() > start) or (
                        datetime.strptime(x[1][0], '%H:%M').time() < end), flight_info))

        if flight_info & self.filters.max_duration_filter_switch():
            time_limit = datetime.strptime(self.filters.max_duration_filter, '%H:%M').time()

            flight_info = list(filter(
                lambda x: (datetime.strptime(
                    x[1][1][x[1][1].find("- ") + 2:][0:1] + ':' + x[1][1][x[1][1].find("- ") + 2:][3:5],
                    '%H:%M').time() < time_limit), flight_info))

        if flight_info & self.filters.price_amount_filter_switch():
            if self.filters.price_amount_filter.split(';')[0] == 'Economy':
                flight_info = list(
                    filter(
                        lambda x: x[2][1] != 'NULL' and int(x[2][0]) <= int(
                            self.filters.price_amount_filter.split(';')[1]),
                        flight_info))
            else:
                flight_info = list(
                    filter(
                        lambda x: x[2][1] != 'NULL' and int(x[2][1]) <= int(
                            self.filters.price_amount_filter.split(';')[1]),
                        flight_info))

        return flight_info

    def check_notify(self, flight_info):
        if self.notifications.amount_notify():
            if self.notifications.amount.split(';')[0] == 'Economy':
                filtered_lst = list(
                    filter(lambda x: x[2][0] != 'NULL' and (
                        int(x[2][0]) <= int(self.notifications.amount.split(';')[1]), flight_info)))
                if filtered_lst:
                    self.notifications.notify_display(filtered_lst)
            else:
                filtered_lst = list(
                    filter(lambda x: x[2][1] != 'NULL' and (
                    int(x[2][1]) <= int(self.notifications.amount.split(';')[1]), flight_info)))
                if filtered_lst:
                    self.notifications.notify_display(filtered_lst)

    def store_info(self):
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

        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='flightplanner',
            database='FP_database'
        )
        my_cursor = mydb.cursor()

        # search the flight information from web.
        flight_info = retrieve_oneway(self.depart, self.dest, int(self.depart_date[:2]), int(self.depart_date[3:5]),
                                      int(self.depart_date[6:]))

        # apply filters to the flight_info.
        flight_info = self.apply_filters(flight_info)

        # notify user if there are flights that satisfy their requirements.

        # store flight_info into db.
        # table_name columns: Depart, Dest, Date, min_econ, min_bus, avg_econ, avg_bus, track_date
        record = 'INSERT INTO {0} VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8});'.format(
            self.table_name, self.depart, self.dest, self.depart_date, find_min(flight_info, 'economy'),
            find_min(flight_info, 'business'), find_avg(flight_info, 'economy'), find_avg(flight_info, 'business'),
            str(datetime.datetime.now().strftime("%x")))

        my_cursor.execute(record)
        del flight_info


class Filters:

    def __init__(self):
        self.day_filter = ''
        self.depart_time_filter = ''
        self.max_duration_filter = ''
        self.price_amount_filter = ''

    def day_filter_switch(self):
        if not self.day_filter:
            return False
        else:
            return True

    def depart_time_filter_switch(self):
        if not self.depart_time_filter:
            return False
        else:
            return True

    def max_duration_filter_switch(self):
        if not self.max_duration_filter:
            return False
        else:
            return True

    def price_amount_filter_switch(self):
        if not self.price_amount_filter:
            return False
        else:
            return True

    # excluded_days is in the form of a string e.g. 'Monday;Wednesday;Thursday'
    def insert_day_filter(self, excluded_days):
        self.day_filter = excluded_days

    # time_range in the form of military time, e.g. '11:30;14:30'
    def insert_depart_time_filter(self, time_range):
        self.depart_time_filter = time_range

    # time_range in the form of military time, e.g. '2:30'
    def insert_max_duration_filter(self, time_range):
        self.max_duration_filter = time_range

    # class_type is either 'Economy' or 'Business'. Amount must be an integer.
    def insert_price_amount_filter(self, class_type, amount):
        self.price_amount_filter = str(class_type) + ';' + str(amount)


class Notification:

    def __init__(self):
        self.amount = ''
        self.diff = 10000000
        self.trend = 10000000

    def amount_notify(self):
        if not self.amount:
            return False
        else:
            return True

    def diff_notify(self):
        if self.diff == 10000000:
            return False
        else:
            return True

    def trend_notify(self):
        if self.trend == 10000000:
            return False
        else:
            return True

    # limit must be a positive integer; class_type (string) is either 'Economy' or 'Business'
    # e.g. 'Economy;500'
    def insert_amount(self, class_type, limit):
        self.amount = str(class_type) + ';' + str(limit)

    # direction must be either 'inc' or 'dec'
    def insert_diff(self, class_type, limit, direction):
        self.diff = str(class_type) + ';' + str(limit) + ';' + str(direction)

    def insert_trend(self, class_type, limit, direction):
        self.trend = str(class_type) + ';' + str(limit) + ';' + str(direction)

    # display_lst contains flight info that satisfies user's request, now display to UI.
    def notify_display(self, display_lst):
        pass
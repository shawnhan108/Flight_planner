import datetime

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
        self.table_name = 'tb' + str(self.track_id)
        self.depart = depart
        self.dest = dest
        self.depart_date = depart_date
        self.filters = Filters()
        self.notifications = Notification()
        self.notify = False

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
        push_command = 'INSERT INTO User_info VALUES ({0}, {1}, {2}, {3},{4},{5});'.format(
            self.username, self.track_id, self.table_name, self.flight_type, self.depart, self.dest
        )
        my_cursor.execute(push_command)

        # setup a unique table for the flight, using table_name
        # table_name columns: Depart, Dest, Date, Depart_time, Arrive_time, Eco_price, Bus_price
        set_up_command = 'CREATE TABLE {0} (Depart varchar(255), Dest varchar(255), Date varchar(255), ' \
                         'Depart_time varchar(255), Arrive_time varchar(255), Eco_price int, Bus_price int);'.format(
            self.table_name)
        my_cursor.execute(set_up_command)

    def apply_filters(self, flight_info):
        if self.filters.day_filter_switch():
            day, month, year = (int(x) for x in self.depart_date.split('/'))
            flight_day = str(datetime.date(year, month, day))
            for days in self.filters.day_filter:
                if flight_day == days:
                    flight_info = []
                    break

        if self.filters.depart_time_filter_switch():
            pass
            # mylist = [1, 1, 2, 3, 4, 5, 6, 6, 8, 9]
            # mynewlist = list(filter(lambda x: x % 2 == 0, mylist))

        return flight_info



    def store_info(self):
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


class Filters:

    def __init__(self):
        self.day_filter = []
        self.depart_time_filter = []
        self.arrive_time_filter = []
        self.price_amount_filter = []

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

    def arrive_time_filter_switch(self):
        if not self.arrive_time_filter:
            return False
        else:
            return True

    def price_amount_filter_switch(self):
        if not self.price_amount_filter:
            return False
        else:
            return True

    # excluded_days is in the form of a list of string, e.g. ['Saturday', 'Sunday']
    def insert_day_filter(self, excluded_days):
        self.day_filter = excluded_days

    # time_range in the form of military time, e.g. [15:00, 21:00]
    def insert_depart_time_filter(self, time_range):
        self.depart_time_filter = time_range

    # time_range in the form of military time, e.g. [15:00, 21:00]
    def insert_arrive_time_filter(self, time_range):
        self.arrive_time_filter = time_range

    # class_type is either 'Economy' or 'Business'. Amount must be an integer.
    def insert_price_amount_filter(self, class_type, amount):
        self.price_amount_filter = [class_type, amount]


class Notification:

    def __init__(self):
        self.amount = -1
        self.diff = 10000000
        self.trend = 10000000

    def amount_notify(self):
        if self.amount == -1:
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

    # limit must be a positive integer
    def insert_amount(self, limit):
        self.amount = limit

    def insert_diff(self, limit):
        self.diff = limit

    def insert_trend(self, limit):
        self.trend = limit

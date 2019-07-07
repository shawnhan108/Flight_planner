import datetime
from datetime import datetime
from typing import Optional

import mysql.connector
from SearchDriver import retrieve_oneway


class Flight:

    def __init__(self):
        """
        return a new, empty flight object.
        """
        # Connect to SQL DB
        self.username = None
        self.flight_id = 0
        self.table_name = 'tb_' + str(self.flight_id)
        self.info_dict = dict()
        self.flight_type = None
        self.depart = None
        self.dest = None
        self.depart_date = None
        self.return_date = None
        self.filters = None
        self.notifications = None

    # store an object information in table general_info
    def __new_flight__(self, flight_id: int, username: str, depart: str, dest: str, depart_date: str, flight_type: str,
                       return_date: Optional[str] = None):
        """
        Creates a basic flight instance, its table, and its dict.
        :param flight_id:
        :param username:
        :param depart:
        :param dest:
        :param depart_date:
        :param flight_type:
        :param return_date:
        :return:
        COMMENT: need to increment flight_id by 1 in load_app
        """
        self.username = username
        self.flight_id = flight_id
        self.table_name = 'tb_' + str(flight_id)
        self.flight_type = flight_type
        self.depart = depart
        self.dest = dest
        self.depart_date = depart_date
        self.return_date = return_date

        # Create table and dicts
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        set_up_command = 'CREATE TABLE {0} (Flight_id int, Date varchar(255), Min_eco int, Min_bus int, Avg_econ int,' \
                         ' Avg_bus int, Track_date varchar(255));'.format(self.table_name)
        mycursor.execute(set_up_command)
        mydb.commit()
        mycursor.close()

        self.info_dict = dict()

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

    #  TODO: Notification Algos

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
        record = 'INSERT INTO {0} VALUES ("{1}", "{2}", "{3}", {4}, {5}, {6}, {7}, "{8}");'.format(
            self.table_name, self.depart, self.dest, self.depart_date, find_min(flight_info, 'economy'),
            find_min(flight_info, 'business'), find_avg(flight_info, 'economy'), find_avg(flight_info, 'business'),
            str(datetime.datetime.now().strftime("%x")))
        my_cursor.execute(record)
        mydb.commit()

        del flight_info
        my_cursor.close()


def reconstruct(flight_id):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='flightplanner',
        database='FP_database'
    )
    my_cursor = mydb.cursor()

    find_flight_instance = 'SELECT * FROM general_info WHERE flight_id="{0}"'.format(flight_id)
    my_cursor.execute(find_flight_instance)
    flight_record = my_cursor.fetchone()
    my_cursor.close()

    new_notification = Notification()
    new_notification.amount = flight_record[16]
    new_notification.diff = flight_record[17]
    new_notification.trend = flight_record[18]

    new_filters = Filters()
    new_filters.day_filter = flight_record[12]
    new_filters.depart_time_filter = flight_record[13]
    new_filters.max_duration_filter = flight_record[14]
    new_filters.price_amount_filter = flight_record[15]

    flight_obj = Flight_oneway(flight_record[0], flight_record[4], flight_record[5],
                               str(flight_record[6]) + '/' + str(flight_record[7]) + '/' + str(flight_record[8]))
    flight_obj.flight_id = flight_record[1]
    flight_obj.table_name = flight_record[2]
    flight_obj.filters = new_filters
    flight_obj.notifications = new_notification

    return flight_obj


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
        self.amount = []
        self.diff = []
        self.trend = []

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
    def insert_amount(self, class_type: str, limit_min: int, limit_max: int):
        self.amount = [class_type, limit_min, limit_max]

    def insert_diff(self, class_type: str, diff: int):
        """
        :param class_type: economy or business
        :param diff: positive or negative
        :return:
        """
        self.diff = [class_type, diff]
        #  TODO: add class attribute class_type and get rid of the params in functions.

    def insert_trend(self, class_type: str, days_since_reset: int, inc_num: int, direction: int):
        """

        :param class_type:
        :param days_since_reset: total number of days since trend started being recorded
        :param inc_num: number of price increase over days.
        :param direction: +1 / -1
        :return:
        """
        #  TODO: trend implementation.

    # display_lst contains flight info that satisfies user's request, now display to UI.
    def notify_display(self, display_lst):
        pass

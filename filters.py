class Filters:

    def __init__(self):
        """
        a new filter object with empty fields. All switches are set to False.
        """
        self.day_filter = ''
        self.depart_time_filter = ''
        self.max_duration_filter = ''
        self.price_amount_filter = 1000000000

    def day_filter_switch(self):
        """
        :return: if user sets a day filter
        """
        if not self.day_filter:
            return False
        else:
            return True

    def depart_time_filter_switch(self):
        """
        :return: if user sets a depart time filter
        """
        if not self.depart_time_filter:
            return False
        else:
            return True

    def max_duration_filter_switch(self):
        """
        :return: if user sets a max flight duration filter
        """
        if not self.max_duration_filter:
            return False
        else:
            return True

    def price_amount_filter_switch(self):
        """
        :return: if user sets a price filter.
        """
        if self.price_amount_filter != 1000000000:
            return True
        else:
            return False

    def insert_day_filter(self, excluded_days):
        """
        :param excluded_days: in the form of a string e.g. 'Monday;Wednesday;Thursday'
        :return: a filter object with day_filter turned on.
        """
        if excluded_days != "NULL":
            self.day_filter = excluded_days

    def insert_depart_time_filter(self, time_range):
        """
        :param time_range: in the form of military time, e.g. '11:30;14:30'
        :return: a filter object with depart_time_filter turned on
        """
        if time_range != "NULL":
            self.depart_time_filter = time_range

    def insert_max_duration_filter(self, time_range):
        """
        :param time_range: in the form of military time, e.g. '2:30'
        :return: a filter object with max duration filter turned on.
        """
        if time_range != "NULL":
            self.max_duration_filter = time_range

    def insert_price_amount_filter(self, amount):
        """
        :param class_type: is either 'Economy' or 'Business'
        :param amount: must be an integer. e.g. 'Economy;120'
        :return: a filter object with price_amount filter turned on.
        """
        if amount != "NULL":
            self.price_amount_filter = amount

    def display_filters(self, display_lst):
        """
        :param display_lst: contains flight info that satisfies user's request
        :return: Display qualified flights to UI
        """
        pass

    def require_filters(self):
        """
        :return: requires user filter settings from frontend, and inserts into the filters object.
                 will be implemented once frontend is set up.
        """
        pass

class Notification:

    def __init__(self):
        self.amount = []
        self.diff = 100000000
        self.trend = []

    def amount_notify(self):
        """
        :return: if user sets an amount filter
        """
        if self.amount:
            return True
        else:
            return False

    def diff_notify(self):
        """
        :return: if user sets a price diff filter
        """
        if self.diff == 100000000:
            return False
        else:
            return True

    def trend_notify(self):
        """
        :return: if user sets a trend filter
        """
        if self.trend:
            return True
        else:
            return False

    def insert_amount(self, limit_min: int, limit_max: int):
        """
        :param limit_min: a positive integer
        :param limit_max: a positive integer
        :return: a notification object with amount turned on.
        """
        self.amount = [limit_min, limit_max]

    def insert_diff(self, diff: int):
        """
        :param diff: positive or negative
        :return: a notification object with diff turned on.
        """
        self.diff = diff

    def insert_trend(self, days_since_reset: int, inc_num: int, direction: int):
        """
        :param days_since_reset: total number of days since trend started being recorded
        :param inc_num: number of price increase over days.
        :param direction: +1 / -1
        :return: a notification object with trend turned on.
        """
        self.trend = [days_since_reset, inc_num, direction]

    def notify_display(self, display_lst):
        """
        :param display_lst: contains flight info that satisfies user's request
        :return: Display qualified flights to UI
        """
        pass

    def require_notifications(self):
        """
        :return: requires user notification settings from frontend, and inserts into the notifications object.
                 will be implemented once frontend is set up.
        """
        pass

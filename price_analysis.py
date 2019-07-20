from notifications import Notification


class NotificationAnalysis(Notification):
    def check_notify(self, flight_info):
        """
        Takes a list of freshly scraped flights and check if the user should be notified.
        If yes, return a list of important data that needs to be displayed to the user.
        If no, then pass, or record down data for later use.
        :param flight_info: a list of flights obtained from AirCanada.
        :return:
        """
        if self.amount_notify():
            # insert code here
            pass

        if self.diff_notify():
            # insert code here
            pass

        if self.trend_notify():
            # insert code here
            pass

    #  TODO: price algos. --> limits, differences, trends

    """
    [[['Ottawa', 'Vancouver'], ['07:00', 'Non-stop - 5hr40m', '09:40'], ['366', '1112']],
    [['Ottawa', 'Vancouver'], ['17:35', 'Non-stop - 5hr40m', '20:15'], ['366', '1112']],
    [['Ottawa', 'Vancouver', 'YUL'], ['05:45', '1 Stop - 7hr15m', '10:00'], ['366', '893']],
    [['Ottawa', 'Vancouver', 'YWG'], ['07:05', '1 Stop - 7hr32m', '11:37'], ['NULL', '1468']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['05:25', '1 Stop - 7hr37m', '10:02'], ['446', '1112']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['17:30', '1 Stop - 7hr38m', '22:08'], ['371', '897']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['16:00', '1 Stop - 8hr02m', '21:02'], ['NULL', '1473']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['17:00', '1 Stop - 8hr08m', '22:08'], ['371', '897']],
    [['Ottawa', 'Vancouver', 'YYC'], ['07:25', '1 Stop - 8hr15m', '12:40'], ['NULL', '1473']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['06:00', '1 Stop - 8hr17m', '11:17'], ['371', '897']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['07:00', '1 Stop - 8hr17m', '12:17'], ['NULL', '1473']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['14:00', '1 Stop - 8hr17m', '19:17'], ['371', '897']],
    [['Ottawa', 'Vancouver', 'YUL'], ['15:35', '1 Stop - 8hr31m', '21:06'], ['NULL', '1473']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['19:00', '1 Stop - 8hr47m - arriving next day', '00:47'], ['366', '1112']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['05:25', '1 Stop - 8hr52m', '11:17'], ['408', '2291']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['15:00', '1 Stop - 9hr02m', '21:02'], ['371', '2291']],
    [['Ottawa', 'Vancouver', 'YUL'], ['10:00', '1 Stop - 9hr08m', '16:08'], ['371', '2291']],
    [['Ottawa', 'Vancouver', 'YUL'], ['14:55', '1 Stop - 9hr11m', '21:06'], ['366', '893']],
    [['Ottawa', 'Vancouver', 'YYC'], ['07:25', '1 Stop - 9hr15m', '13:40'], ['NULL', '1468']],
    [['Ottawa', 'Vancouver', 'YYZ'], ['06:00', '1 Stop - 9hr17m', '12:17'], ['371', '2291']]]
    
    Above is a list structure (that param called flight_info), which is a list of flights that is scraped from AirCanada
    Each flight is a sublist that contains 3 sub-sublists: a list of depart/dest, a list of depart_time and arrive_time,
    and a list of economy price and business price.
    So ya bro this is the data structure you will handle...
    
    Also, here is a brief explanation of the notification class from notifications.py that you will use:
    
    amount_notify, diff_notify, and trend_notify are predicate functions that tell you if user has setup a notification 
      of price/diff/trend or not.
    insert price/diff/trend are functions that set up the notifications.
    
    I don't think you will use these functions extensively, but you may want to access the notifications. Access them
    like this:
    """

    def example(self):
        amount_notification = self.amount
        differences_notification = self.diff
        trend_notification = self.trend

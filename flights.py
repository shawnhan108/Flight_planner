import datetime
from datetime import datetime
from typing import Optional

import mysql.connector

from filters import Filters
from notifications import Notification


class Flight:

    def __init__(self):
        """
        return a new, empty flight object.
        """
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

        self.filters = Filters()
        self.filters.require_filters()

        self.notifications = Notification()
        self.notifications.require_notifications()

    def __load_flight_dict__(self):
        """
        loads the flight's dictionary from flight table. Track_date as key in dict.
        :return: a flight object with loaded dict.
        """
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        temp_dict = dict()
        mycursor.execute("SELECT * FROM {0};".format(self.table_name))
        data_list = mycursor.fetchall()

        for record in data_list:
            temp_dict[record[6]] = record[:6]

        self.info_dict = temp_dict
        mycursor.close()

    def commit_flight_db(self, min_eco: int, min_bus: int, avg_econ: int, avg_bus: int):
        """
        Updates both flight table and flight dict using newly extracted info from web.
        :param min_eco:
        :param min_bus:
        :param avg_econ:
        :param avg_bus:
        :return:
        """
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()
        record_command = "INSERT INTO {0} (Flight_id, Date, Min_eco, Min_bus, Avg_econ, Avg_bus, Track_date) VALUES" \
                         " ({1}, {2}, {3}, {4}, {5}, {6}, {7})".format(self.table_name, self.flight_id,
                                                                       self.depart_date, min_eco, min_bus, avg_econ,
                                                                       avg_bus, str(datetime.date.today()))
        mycursor.execute(record_command)
        mydb.commit()
        mycursor.close()

        # Now update the dict
        self.info_dict[str(datetime.date.today())] = (self.flight_id, self.depart_date, min_eco, min_bus, avg_econ,
                                                      avg_bus)


class User:
    def __init__(self):
        """
        return a new user object
        flights_dict has flight_id as key, flight object as content.
        """
        self.name = ''
        self.age = -1
        self.username = ''
        self.password = ''
        self.flights_dict = dict()

    def __is_valid_Pass__(self):
        """
        __is_valid_Pass_(self): checks if a string meets the acceptance criteria for a password.
        Time: O(n) -> Θ(4n), where n is the length of the string.
        :return: boolean indicating if the password is valid.
        """

        special_chars = ("[", "@", "_", "!", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "?", "/", "\\", "|", "}",
                         "{", "~", ":", "]", '"')  # Tuple of Characters Considered as Special Characters
        password = self.password  # the password string to be examined.

        if (any(i.isupper() for i in password) and  # Check if Password Contains a Uppercase Character
                any(i.islower() for i in password) and  # Check if Password Contains a Lowercase Character
                any(i.isdigit() for i in password) and  # Check if Password Contains a Numerical Digit Character
                any(i in special_chars for i in password) and  # Check if Password Contains a Special Character
                len(password) >= 6):  # Check if Password is Minimum 6 Characters Length
            return True
        else:
            return False

    def __password_setup__(self, reset: Optional[bool] = False):
        """
        __password_setup__(self): maintains the process to successful password setup for a User ID.
        Side Effects: Mutates UserID
                      Print to I/O
        Time: O(n * m), where n is the length of the password and m is the number of attempts to setup a password.
        :return: object with qualified password; password string
        """

        while True:  # Request New Password Till Successful Completion of User ID Password Set-up
            while not self.__is_valid_Pass__:  # Check if User ID Password is Valid
                # Print Valid Password Acceptance Criteria
                print("Please make sure you're password has at least:\n")
                print("1) At least one upper case character;\n")
                print("2) At least one lower case character;\n")
                print("3) At least one numerical digit character;\n")
                print("4) At least one special character; and\n")
                print("5) Minimum 6 characters.")

                if reset:
                    self.password = input("Please enter your new password: ")
                else:
                    self.password = input("Please enter your password: ")  # Request User ID Password

            check_password: str = input("Please re-enter your password: ")  # Request Password Confirmation

            if check_password == self.password:  # Acceptance Criteria
                break  # Successful Password Setup
            else:
                self.password = "0"  # Automatic Password Failure to Reset Password Set-Up Process

from typing import Optional

from flights import Flight, User
from filters import Filters
from general_dbs import UsersDB, FlightsDB
from notifications import Notification


class App:
    """
    App class is the main instance. It is the intersection of dbs and objects.
    Therefore, all functions that change DB RAMs and objects must be place in this class to access dicts.
    """

    def __init__(self):
        """
        loads userDb and flightsDB in RAM dictionary.
        loads all flights and Users objects and store in RAM dictionary.
        flights_users_dict: username as key, user object as content.
        Gets the largest flight_id over all flights.
        """
        self.users_db = UsersDB()
        self.flights_db = FlightsDB()
        self.flight_id = max(self.flights_db.flights_dict.keys()) + 1
        temp_dict = dict()

        for key in self.users_db.users_dict.items():
            temp_user = User()
            self.__load_user__(key, temp_user)
            self.__load_user_dict__(temp_user)
            temp_dict[key] = temp_user
        self.users_flights_dict = temp_dict

    def __load_flight__(self, flight_id: int, flight: Flight):
        """
        loads a flight object by obtaining into from general DB
        :param flight_id:
        :param flight:
        :return:
        """
        info_tuple = self.flights_db.flights_dict[flight_id]

        # load into flight object
        flight.username = info_tuple[0]
        flight.flight_type = info_tuple[1]
        flight.depart = info_tuple[2]
        flight.dest = info_tuple[3]
        flight.depart_date = info_tuple[4]
        flight.return_date = info_tuple[5]
        flight.table_name = 'tb_' + str(flight_id)
        flight.flight_id = flight_id

        temp_filter = Filters()
        temp_filter.insert_day_filter(info_tuple[6])
        temp_filter.insert_depart_time_filter(info_tuple[7])
        temp_filter.insert_max_duration_filter(info_tuple[8])
        temp_filter.insert_price_amount_filter(info_tuple[9])
        flight.filters = temp_filter

        temp_noti = Notification()
        if info_tuple[10] != "NULL":
            limit_min = info_tuple[10].split(';')[0]
            limit_max = info_tuple[10].split(':')[1]
            temp_noti.insert_amount(limit_min, limit_max)
        if info_tuple[11] != "NULL":
            temp_noti.insert_diff(int(info_tuple[11]))
        if info_tuple[12] != "NULL":
            days_since_reset = info_tuple[12].split(';')[0]
            inc_num = info_tuple[12].split(';')[1]
            direction = info_tuple[12].split(';')[2]
            temp_noti.insert_trend(days_since_reset, inc_num, direction)
        flight.notifications = temp_noti

    def __load_user__(self, username: str, target_user: User):
        info_tuple = self.users_db.users_dict[username]

        target_user.name = info_tuple[0]
        target_user.age = info_tuple[1]
        target_user.username = username
        target_user.password = info_tuple[2]

    def __load_user_dict__(self, target_user: User):
        temp_flights_dict = dict()
        for key, content in self.flights_db.flights_dict.items():
            if content[0] == target_user.username:
                temp_flight = Flight()
                self.__load_flight__(key, temp_flight)
                temp_flight.__load_flight_dict__()
                temp_flights_dict[key] = temp_flight
        target_user.flights_dict = temp_flights_dict

    def __new_flight__(self, username: str, depart: str, dest: str, depart_date: str, flight_type: str,
                       target_user: User, return_date: Optional[str] = None):
        """
        :param username: username of the user that is creating this flight instance
        :return: a flight object by using info passed in. Info will be obtained from front-end.
        """
        new_flight = Flight()
        new_flight.__new_flight__(self.flight_id, username, depart, dest, depart_date, flight_type, return_date)
        target_user.flights_dict[self.flight_id] = new_flight
        self.flights_db.add_flight(new_flight.flight_id, new_flight.username, new_flight.flight_type,
                                   new_flight.depart, new_flight.dest, new_flight.depart_date,
                                   new_flight.return_date, new_flight.filters.day_filter,
                                   new_flight.filters.depart_time_filter, new_flight.filters.max_duration_filter,
                                   new_flight.filters.price_amount_filter, new_flight.notifications.amount,
                                   new_flight.notifications.diff, new_flight.notifications.trend)
        self.flight_id += 1

    def __username_setup__(self, target_user: User):
        """
        __username_setup__ requests user's username from I/O stream, verifies its validity, and stores it to the field.
        :param user: the UserDB object to have its username set up
        Side Effect: Mutate UserDB
        Time: O(1)
        """
        valid = False
        while not valid:
            target_user.username = input('Please enter your username')
            if target_user.username in self.users_db.users_dict.keys():
                print('The username you have entered is taken.')
            else:
                valid = True

    def __new_user__(self, name: str, age: int, password: str):
        target_user = User()

        # Set up user object and add to dict
        target_user.name = name
        target_user.age = age
        self.__username_setup__(target_user)
        target_user.__password_setup__()
        target_user.flights_dict = dict()

        # Add to dicts and dbs
        self.users_db.add_user(target_user.name, target_user.age, target_user.username, target_user.password)
        self.users_flights_dict[target_user.username] = target_user

    def change_username(self, target_user: User):
        old_username = target_user.username
        self.__username_setup__(target_user)

        self.users_db.update_username(old_username=old_username, new_username=target_user.username)
        self.flights_db.update_username(old_username=old_username, new_username=target_user.username)

        self.users_flights_dict[target_user.username] = target_user
        del self.users_flights_dict[old_username]

    def change_password(self, target_user: User):
        attempt: int = 0

        # Request old password for security:
        while attempt <= 3:
            if input("Please enter your old password") == target_user.password:
                break  # successful
            elif attempt == 3:
                return  # exit from procedure due to security
            else:
                attempt += 1

        target_user.__password_setup__(reset=True)  # Create Successful Password Setup
        self.users_db.update_user(username=target_user.username, password=target_user.password)

    def update_flight(self, flight_id: int, flight_type: Optional[str] = None,
                      depart: Optional[str] = None, dest: Optional[str] = None, depart_date: Optional[str] = None,
                      return_date: Optional[str] = None, day_filter: Optional[str] = None,
                      depart_time_filter: Optional[str] = None, max_duration_filter: Optional[str] = None,
                      price_amount_filter: Optional[int] = None, noti_amount: Optional[str] = None,
                      noti_diff: Optional[int] = None, noti_trend: Optional[str] = None):
        """
        update_flight updates the flight record info in both flights_table and flights dict
        :param flight_id: mandatory, the flight Id of the flight to be modified
        :param flight_type: flight type, 'economy', 'business', or 'both'
        :param depart: departure airport
        :param dest: destination airport
        :param depart_date: departure date
        :param return_date: Optional: return date.
        :param day_filter: Day filter: excluded_days is in the form of a string e.g. 'Monday;Wednesday;Thursday'
        :param depart_time_filter: time_range in the form of military time, e.g. '11:30;14:30'
        :param max_duration_filter:  time_range in the form of military time, e.g. '2:30'
        :param price_amount_filter: price in int.
        :param noti_amount: '500;1000' min_amount/max_amount
        :param noti_diff: +100 signed amount int.
        :param noti_trend: '5;2;1' days since reset;number of price increase over days;direction(1/-1)
        :return: Update flights_table and dicts
        """
        username = self.flights_db.flights_dict[flight_id][0]

        if flight_type:
            self.flights_db.update_flight(flight_id=flight_id, flight_type=flight_type)
            self.users_flights_dict[username].flights_dict[flight_id].flight_type = flight_type

        if depart:
            self.flights_db.update_flight(flight_id=flight_id, depart=depart)
            self.users_flights_dict[username].flights_dict[flight_id].depart = depart

        if dest:
            self.flights_db.update_flight(flight_id=flight_id, dest=dest)
            self.users_flights_dict[username].flights_dict[flight_id].dest = dest

        if depart_date:
            self.flights_db.update_flight(flight_id=flight_id, depart_date=depart_date)
            self.users_flights_dict[username].flights_dict[flight_id].depart_date = depart_date

        if return_date:
            self.flights_db.update_flight(flight_id=flight_id, return_date=return_date)
            self.users_flights_dict[username].flights_dict[flight_id].return_date = return_date

        if day_filter:
            self.flights_db.update_flight(flight_id=flight_id, day_filter=day_filter)
            self.users_flights_dict[username].flights_dict[flight_id].filters.insert_day_filter(day_filter)

        if depart_time_filter:
            self.flights_db.update_flight(flight_id=flight_id, depart_time_filter=depart_time_filter)
            self.users_flights_dict[username].flights_dict[flight_id].filters.insert_depart_time_filter(
                depart_time_filter)

        if max_duration_filter:
            self.flights_db.update_flight(flight_id=flight_id, max_duration_filter=max_duration_filter)
            self.users_flights_dict[username].flights_dict[flight_id].filters.insert_max_duration_filter(
                max_duration_filter)

        if price_amount_filter:
            self.flights_db.update_flight(flight_id=flight_id, price_amount_filter=price_amount_filter)
            self.users_flights_dict[username].flights_dict[flight_id].filters.insert_price_amount_filter(
                price_amount_filter)

        if noti_amount:
            limit_min = int(noti_amount.split(';')[0])
            limit_max = int(noti_amount.split(';')[1])

            self.flights_db.update_flight(flight_id=flight_id, noti_amount=noti_amount)
            self.users_flights_dict[username].flights_dict[flight_id].notifications.insert_amount(limit_min, limit_max)

        if noti_diff:
            self.flights_db.update_flight(flight_id=flight_id, noti_diff=noti_diff)
            self.users_flights_dict[username].flights_dict[flight_id].notifications.insert_diff(noti_diff)

        if noti_trend:
            days_since_reset = int(noti_trend.split(';')[0])
            inc_num = int(noti_trend.split(';')[1])
            direction = int(noti_trend.split(';')[2])

            self.flights_db.update_flight(flight_id=flight_id, noti_trend=noti_trend)
            self.users_flights_dict[username].flights_dict[flight_id].notifications.insert_trend(days_since_reset,
                                                                                                 inc_num, direction)

    def update_user(self, username: str, name: Optional[str] = None, age: Optional[int] = None,
                    password: Optional[str] = None):
        """
                update_accounts updates the user record info in both users_table and users dict.
                :param username: mandatory. The username of the user record to be updated.
                :param name: Updated User's name
                :param age: Updated User's age
                :param password: Updated password
                :return: Updated users_table and users dict.
        """
        if name:
            self.users_db.update_user(username, name=name)
            self.users_flights_dict[username].name = name
        if age:
            self.users_db.update_user(username, age=age)
            self.users_flights_dict[username].age = age
        if password:
            self.users_db.update_user(username, password=password)
            self.users_flights_dict[username].password = password

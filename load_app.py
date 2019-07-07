from general_dbs import UsersDB, FlightsDB
from Flights import Flight
from typing import Optional
import mysql.connector


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
        self.flight_id = 0

    def __new_flight__(self, username: str, depart: str, dest: str, depart_date: str, flight_type: str,
                       return_date: Optional[str] = None):
        """
        :param username: username of the user that is creating this flight instance
        :return: a flight object by using info passed in. Info will be obtained from front-end.
        """
        new_flight = Flight()
        new_flight.__new_flight__(self.flight_id, username, depart, dest, depart_date, flight_type, return_date)
        # TODO: add flight to FlightDB after notificadtion and filters are properly implemented.


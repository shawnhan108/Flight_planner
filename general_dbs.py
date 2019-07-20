from typing import Optional

import mysql.connector


class UsersDB:
    def __init__(self):
        """
        Creates a Users object, retrieves user records from users_table, and stores it in a dictionary in RAM.
        that is, copies database into a dict.
        Time: O(n) where n is the size of the users_table
        COMMENT: Users dict has username as key, and other columns stored as tuple in contents.
        Category: Load, DB.
        """
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        # Retrieve data from users_table and store in dict.
        out_dict = dict()
        mycursor.execute("SELECT * FROM users_table;")
        data_list = mycursor.fetchall()

        for record in data_list:
            out_dict[record[2]] = record[:2] + (record[3],)
        self.users_dict = out_dict

        mycursor.close()

    def reconstruct_users_db(self):
        """
        Removes current users_table and creates a new users table.
        Time: O(1)
        :return: Truncated users_table
        Category: DB
        """
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')

        # Remove the old table
        mycursor = mydb.cursor()
        remove_command = 'DROP TABLE users_table;'
        mycursor.execute(remove_command)
        mydb.commit()

        # Create a new accounts_table in mySQL database
        create_table_command = 'CREATE TABLE {0} (Name varchar(255), Age int, Username varchar(255),' \
                               ' Password varchar(255));'.format('users_table')

        mycursor.execute(create_table_command)
        mydb.commit()
        mycursor.close()

        self.users_dict = dict()

    def add_user(self, name: str, age: int, username: str, password: str):
        """
        creates a record in users_table and a key-content in users dict that records the new user.
        :param name: name of user
        :param age: age of user
        :param username: username
        :param password: password
        :return: updated users_table with updated users dict
        Time: O(1)
        Category: DB
        """
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        # Generate the new user record into users_table
        commit_command = 'INSERT INTO {0} (Name, Age, Username, Password) VALUES ({1}, {2}, {3}, {4});'.format(
            'users_table', name, age, username, password)
        mycursor.execute(commit_command)
        mydb.commit()
        mycursor.close()

        # add key to dictionary
        self.users_dict[username] = (name, age, password)

    def delete_user(self, username: str):
        """
        removes the record of the user from users_table and users dict.
        :param username: the username of the user to be deleted.
        :return: an updated user table and user dict
        Time: O(n)
        Category: DB
        """
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        # Delete the record in users_table
        delete_command = 'DELETE FROM users_table WHERE Username={0}'.format(username)
        mycursor.execute(delete_command)
        mydb.commit()
        mycursor.close()

        # delete key from the dictionary as well
        del self.users_dict[username]

    def update_username(self, old_username: str, new_username: str):
        """
        Updates Users_db and its corresponding dict/RAM instances.
        :param old_username: original username
        :param new_username: new username
        :return: Updated dbs.
        Time: O(n) where n = size of Users_db
        COMMENT: expensive DB function.
        """
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        #  Update Users_db
        update_command = "UPDATE users_table SET Username = '{0}' WHERE Username = {1};".format(new_username,
                                                                                                old_username)
        mycursor.execute(update_command)
        mydb.commit()
        mycursor.close()

        #  Update users_dict
        for key, content in self.users_dict.items():
            if key == old_username:
                self.users_dict[new_username] = content
                del self.users_dict[old_username]

    def update_user(self, username: str, name: Optional[str] = None, age: Optional[int] = None,
                    password: Optional[str] = None):
        """
        update_accounts updates the user record info in both users_table and users dict.
        :param username: mandatory. The username of the user record to be updated.
        :param name: Updated User's name
        :param age: Updated User's age
        :param password: Updated password
        :return: Updated users_table and users dict.
        Time: O(n), where n is the size of users_table
        Category: DB function
        """
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        if name:
            # Update database
            update_command = "UPDATE users_table SET Name = '{0}' WHERE Username = {1};".format(name, username)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.users_dict[username]
            self.users_dict[username] = (name,) + original_record[1:]

        if age:
            # Update database
            update_command = "UPDATE users_table SET Age = '{0}' WHERE Username = {1};".format(age, username)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.users_dict[username]
            self.users_dict[username] = (original_record[0],) + (age,) + (original_record[2])

        if password:
            # Update database
            update_command = "UPDATE users_table SET Password = '{0}' WHERE Username = {1};".format(password,
                                                                                                    username)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.users_dict[username]
            self.users_dict[username] = original_record[:2] + (password,)

        mycursor.close()


class FlightsDB:
    def __init__(self):
        """
        creates a flightsDB object and update the flights attribute.
        retrieves flight records from flights_table, and stores it in a dict in RAM for faster use.
        Time: O(n) where n is the size of flights_table.
        COMMENT: the flights dict has flight_id as key, other columns stores in as tuple.
        Category: Load, DB
        """
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        # retrieve data from accounts_table and store in dictionary.
        out_dict = dict()
        mycursor.execute("SELECT * FROM flights_table;")
        data_list = mycursor.fetchall()

        for record in data_list:
            out_dict[record[0]] = record[1:]

        self.flights_dict = out_dict

        mycursor.close()

    def reconstruct_flights_db(self):
        """
        Truncates the flights_table
        Time: O(1)
        :return: Updated, empty flights_table.
        Category: DB
        """
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        # Remove the old table
        remove_command = 'DROP TABLE flights_table;'
        mycursor.execute(remove_command)
        mydb.commit()

        # Create a new flights table in mySQL database
        create_table_command = 'CREATE TABLE {0} (Flight_id int, Username varchar(255), Flight_type varchar(255), ' \
                               'Depart varchar(255), Dest varchar(255), Depart_date varchar(255), ' \
                               'Return_date varchar(255), Day_filter varchar(255), Depart_time_filter varchar(255), ' \
                               'Max_duration_filter varchar(255), Price_amount_filter int, Noti_amount varchar(255), ' \
                               'Noti_diff int, Noti_trend varchar(255));'.format('flights_table')
        mycursor.execute(create_table_command)
        mydb.commit()
        mycursor.close()

        self.flights_dict = dict()

    def add_flight(self, flight_id: int, username: str, flight_type: str, depart: str, dest: str, depart_date: str,
                   return_date: Optional[str] = 'NULL', day_filter: Optional[str] = 'NULL',
                   depart_time_filter: Optional[str] = 'NULL', max_duration_filter: Optional[str] = 'NULL',
                   price_amount_filter: Optional[int] = 'NULL', noti_amount: Optional[str] = 'NULL',
                   noti_diff: Optional[int] = 'NULL', noti_trend: Optional[str] = 'NULL'):
        """
        creates a new flight object, sets up dictionaries and dicts.
        :param flight_id: flight ID
        :param username: username
        :param flight_type: flight type, 'economy', 'business', or 'both'
        :param depart: departure airport
        :param dest: destination airport
        :param depart_date: departure date, e.g. '08/23/2019' meaning August 23rd, 2019
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
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        # Generate new flight record into flights_table
        self.flights_dict[flight_id] = (username, flight_type, depart, dest, depart_date, return_date, day_filter,
                                        depart_time_filter, max_duration_filter, price_amount_filter, noti_amount,
                                        noti_diff, noti_trend)
        commit_command = "INSERT INTO {0} (Flight_id, Username, Flight_type, Depart, Dest, Depart_date, Return_date, " \
                         "Day_filter, Depart_time_filter, Max_duration_filter, Price_amount_filter, Noti_amount, " \
                         "Noti_diff, Noti_trend) VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, " \
                         "{12}, {13}, {14});".format('flights_table', flight_id, username, flight_type, depart, dest,
                                                     depart_date, return_date, day_filter, depart_time_filter,
                                                     max_duration_filter, price_amount_filter, noti_amount, noti_diff,
                                                     noti_trend)
        mycursor.execute(commit_command)
        mydb.commit()
        mycursor.close()

    def delete_flight(self, flight_id: int):
        """
        removes the record of the flight from table
        :param flight_id: flight ID
        :return: updated flights_table, and flight dict
        Time: O(n)
        Category: DB
        """
        # Connect to SQL DB
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        # Delete the record from flights_table
        delete_command = "DELETE FROM flights_table WHERE Flight_id={0}".format(flight_id)
        mycursor.execute(delete_command)
        mydb.commit()
        mycursor.close()

        # Delete from dictionary
        del self.flights_dict[flight_id]

    def update_flight(self, flight_id: int, username: Optional[str] = None, flight_type: Optional[str] = None,
                      depart: Optional[str] = None, dest: Optional[str] = None, depart_date: Optional[str] = None,
                      return_date: Optional[str] = None, day_filter: Optional[str] = None,
                      depart_time_filter: Optional[str] = None, max_duration_filter: Optional[str] = None,
                      price_amount_filter: Optional[int] = None, noti_amount: Optional[str] = None,
                      noti_diff: Optional[int] = None, noti_trend: Optional[str] = None):
        """
        update_flight updates the flight record info in both flights_table and flights dict
        :param flight_id: mandatory, the flight Id of the flight to be modified
        :param username: username
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
        Time: O(1)
        Category: DB
        """
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        if username:
            update_command = "UPDATE flights_table SET Username={0} WHERE Flight_id={1};".format(username, flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = (username,) + original_record[1:]

        if flight_type:
            update_command = "UPDATE flights_table SET Flight_type={0} WHERE Flight_id={1};".format(flight_type,
                                                                                                    flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = (original_record[0],) + (flight_type,) + original_record[2:]

        if depart:
            update_command = "UPDATE flights_table SET Depart={0} WHERE Flight_id={1};".format(depart, flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:2] + (depart,) + original_record[3:]
        if dest:
            update_command = "UPDATE flights_table SET Dest={0} WHERE Flight_id={1};".format(dest, flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:3] + (dest,) + original_record[4:]
        if depart_date:
            update_command = "UPDATE flights_table SET Depart_date={0} WHERE Flight_id={1};".format(depart_date,
                                                                                                    flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:4] + (depart_date,) + original_record[5:]
        if return_date:
            update_command = "UPDATE flights_table SET Return_date={0} WHERE Flight_id={1};".format(return_date,
                                                                                                    flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:5] + (return_date,) + original_record[6:]
        if day_filter:
            update_command = "UPDATE flights_table SET Day_filter={0} WHERE Flight_id={1};".format(day_filter,
                                                                                                   flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:6] + (day_filter,) + original_record[7:]
        if depart_time_filter:
            update_command = "UPDATE flights_table SET Depart_time_filter={0} WHERE Flight_id={1};".format(
                depart_time_filter, flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:7] + (depart_time_filter,) + original_record[8:]
        if max_duration_filter:
            update_command = "UPDATE flights_table SET Max_duration_filter={0} WHERE Flight_id={1};".format(
                max_duration_filter, flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:8] + (max_duration_filter,) + original_record[9:]
        if price_amount_filter:
            update_command = "UPDATE flights_table SET Price_amount_filter={0} WHERE Flight_id={1};".format(
                price_amount_filter, flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:9] + (price_amount_filter,) + original_record[10:]
        if noti_amount:
            update_command = "UPDATE flights_table SET Noti_amount={0} WHERE Flight_id={1};".format(
                noti_amount, flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:10] + (noti_amount,) + original_record[11:]
        if noti_diff:
            update_command = "UPDATE flights_table SET Noti_diff={0} WHERE Flight_id={1};".format(
                noti_diff, flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:11] + (noti_diff,) + original_record[12:]
        if noti_trend:
            update_command = "UPDATE flights_table SET Noti_trend={0} WHERE Flight_id={1};".format(
                noti_trend, flight_id)
            mycursor.execute(update_command)
            mydb.commit()

            original_record = self.flights_dict[flight_id]
            self.flights_dict[flight_id] = original_record[:12] + (noti_trend,) + original_record[13:]

        mycursor.close()

    def update_username(self, old_username: str, new_username: str):
        """
        Updates flights_table and its dict
        :param old_username: original username
        :param new_username: new username
        :return: Update dbs and dicts
        Time: O(n) where n = size of flights_table
        COMMENT: expensive DB function
        """
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='flightplanner', database='FP_database')
        mycursor = mydb.cursor()

        #  Update flights_table
        update_command = "UPDATE flights_table SET Username={0} WHERE Username = {1};".format(new_username,
                                                                                              old_username)
        mycursor.execute(update_command)
        mydb.commit()
        mycursor.close()

        #  Update dict
        for key, content in self.flights_dict.items():
            if content[0] == old_username:
                self.flights_dict[key] = (new_username,) + content[1:]

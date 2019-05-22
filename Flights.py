import mysql.connector


class Flight_oneway:
    flight_type = 'oneway'
    track_counter = 0

    # Initializer with attributes
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

    # store information in database
    def push_info(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='flightplanner',
            database='FP_database'
        )
        my_cursor = mydb.cursor()

        # Table columns: Username, track_id, table_name, trip_type, depart, dest
        push_command = 'INSERT INTO User_info VALUES ({0}, {1}, {2}, {3},{4},{5});'.format(
            self.username, self.track_id, self.table_name, self.flight_type, self.depart, self.dest
        )
        my_cursor.execute(push_command)

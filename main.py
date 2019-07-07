import airportcodes
import searchAirport
import SearchDriver
import mysql.connector
from datetime import datetime
import time
import datetime
import Flights


# print(airportcodes.giveCode("York Landing, MB"))

# print(searchAirport.airportSearch("To"))

# list structure of a single flight search output:  flight_info
# [[['Ottawa', 'Vancouver'], ['07:00', 'Non-stop - 5hr40m', '09:40'], ['366', '1112']],
# [['Ottawa', 'Vancouver'], ['17:35', 'Non-stop - 5hr40m', '20:15'], ['366', '1112']],
# [['Ottawa', 'Vancouver', 'YUL'], ['05:45', '1 Stop - 7hr15m', '10:00'], ['366', '893']],
# [['Ottawa', 'Vancouver', 'YWG'], ['07:05', '1 Stop - 7hr32m', '11:37'], ['NULL', '1468']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['05:25', '1 Stop - 7hr37m', '10:02'], ['446', '1112']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['17:30', '1 Stop - 7hr38m', '22:08'], ['371', '897']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['16:00', '1 Stop - 8hr02m', '21:02'], ['NULL', '1473']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['17:00', '1 Stop - 8hr08m', '22:08'], ['371', '897']],
# [['Ottawa', 'Vancouver', 'YYC'], ['07:25', '1 Stop - 8hr15m', '12:40'], ['NULL', '1473']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['06:00', '1 Stop - 8hr17m', '11:17'], ['371', '897']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['07:00', '1 Stop - 8hr17m', '12:17'], ['NULL', '1473']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['14:00', '1 Stop - 8hr17m', '19:17'], ['371', '897']],
# [['Ottawa', 'Vancouver', 'YUL'], ['15:35', '1 Stop - 8hr31m', '21:06'], ['NULL', '1473']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['19:00', '1 Stop - 8hr47m - arriving next day', '00:47'], ['366', '1112']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['05:25', '1 Stop - 8hr52m', '11:17'], ['408', '2291']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['15:00', '1 Stop - 9hr02m', '21:02'], ['371', '2291']],
# [['Ottawa', 'Vancouver', 'YUL'], ['10:00', '1 Stop - 9hr08m', '16:08'], ['371', '2291']],
# [['Ottawa', 'Vancouver', 'YUL'], ['14:55', '1 Stop - 9hr11m', '21:06'], ['366', '893']],
# [['Ottawa', 'Vancouver', 'YYC'], ['07:25', '1 Stop - 9hr15m', '13:40'], ['NULL', '1468']],
# [['Ottawa', 'Vancouver', 'YYZ'], ['06:00', '1 Stop - 9hr17m', '12:17'], ['371', '2291']]]

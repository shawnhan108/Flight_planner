import airportcodes
import searchAirport

print(airportcodes.giveCode("York Landing, MB"))

print(searchAirport.airportSearch("To"))

test = "Ottawa\nYUL"

substring = test[test.find("\n") + 1:]
print(substring)
print(test)

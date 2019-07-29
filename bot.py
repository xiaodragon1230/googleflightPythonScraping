import collectData
import helpers
import datetime
import csv


# Returns list of cheapest flight objects based on destinations.csv searches
# Parameters:
#   driver: (Selenium.webdriver) Selenium driver object
# Returns:
#   cheapest: (list<Flight>) list of cheapest Flight objects
def search(maximum_price):
    destinations_filename = 'destinations.csv'
    cheapest = []
    # Used to find flights only during the university summer
    summerStart = datetime.date(2018, 5, 5)
    summerEnd = datetime.date(2018, 8, 15)

    # List of destinations
    searches = helpers.openCSV(destinations_filename)
    destinations = helpers.destListToObject(searches)
    googleFlight = collectData.GoogleFlight()
    for dest in destinations:
        driver = helpers.getDriver(False)
        cheapFlight = googleFlight.get_flights( driver=driver,
                                                departing='CVG',
                                                destination=dest.dest,
                                                tripLen=dest.tripLen,
                                                lowBound=summerStart,
                                                highBound=summerEnd)
        cheapest.append(cheapFlight)
        driver.close()

    csv_filename = 'data.csv'
    cheapest_flights_with_max = filter_flights(csv_filename, maximum_price)
    return cheapest_flights_with_max

def filter_flights(csv_filename, maximum_price):
    cheapest_flights = read_csv(csv_filename)
    cheapest_flights_with_max = []
    for cheapest_flight in cheapest_flights:
        if cheapest_flight['Price'] <= maximum_price:
            cheapest_flights_with_max.append(cheapest_flight)
    return cheapest_flights_with_max

def read_csv(csv_filename):
    fieldnames = ['Price', 'Departing airport', 'Destination airport', 'Depart date']
    csv_file = open(csv_filename)
    flights = []
    csv_file_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    for row in csv_file_reader:
        try:
            row['Price'] = int(row['Price'])
        except Exception:
            row['Price'] = 0
        flights.append(row)
    csv_file.close()
    return flights

# upload the cheapest list
def upload(list):
    pass

if __name__ == '__main__':
    cheapest = search(200)
    print(cheapest)
    # flights = filter_flights('data.csv', 39000)
    # for flight in flights:
    #     print(flight['Price'])
    #upload(cheapest)

import csv
from selenium import webdriver
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re


class Flight:
    def __init__(self, dep='', dest='', price=10000000, avg=1, logDate=datetime.date,
                 depDate=datetime.date, retDate=datetime.date, percentage=-1.00, tweeted=False):
        self.dep = dep         # (String) departing airport
        self.dest = dest       # (String) destination airport
        self.price = price     # (int) price
        self.avg = avg         # (int) average price
        self.logDate = logDate  # (date) date at which this was logged
        self.depDate = depDate  # (date) departing date
        self.retDate = retDate  # (date) return date
        self.tweeted = tweeted  # (bool) True = tweeted, False = not tweeted
        self.percentage = 1000000.0
        self.destinationsFile = 'destinations.csv'

    def __str__(self):
        city = 'N/A'
        country = 'N/A'
        searches = helpers.openCSV(self.destinationsFile)
        destinations = helpers.destListToObject(searches)
        for dest in destinations:
            if dest.dest == self.dest:
                city = dest.city
                country = dest.country
        dateFormat = "%m/%d/%Y"
        ret = '$' + str(self.price) + ' round trip:\n'
        ret += 'Cincinnati, Ohio'
        ret += ' \xE2\x9C\x88 ' + city + ', ' + country + '\n'
        ret += self.depDate.strftime(dateFormat)
        ret += ' - ' + self.retDate.strftime(dateFormat) + '\n'
        ret += self.getURL()
        return ret

    def getURL(self):
        URL_DATE_FORMAT = "%Y-%m-%d"
        URL = 'https://www.google.com/flights/#search;f={};t={};d={};r={}'
        return URL.format(self.dep, self.dest, self.depDate.strftime(URL_DATE_FORMAT),
                          self.retDate.strftime(URL_DATE_FORMAT))

    def setAverage(self, avg):
        self.avg = avg
        self.percentage = (float(self.price) / self.avg) * 100

    def tweeted(self):
        # Call if this flight was tweeted (BEFORE LOGGING)
        self.tweeted = True

    def log(self):
        # .csv format:
        # time, departing airport, price, average price, percentage, tweeted
        dateFormat = "%m/%d/%Y"
        dataFolder = paths.dirname(paths.realpath(__file__))
        with open(paths.dataFolder + self.dest + '.csv', 'a') as logFile:
            logFile.write(self.logDate.strftime(dateFormat) + ',' +
                          self.dep + ',' +
                          self.dest + ',' +
                          self.depDate.strftime(dateFormat) + ',' +
                          self.retDate.strftime(dateFormat) + ',' +
                          str(self.price) + ',' +
                          str(self.avg) + ',' +
                          str(self.tweeted) + '\n')


class Destination:
    def __init__(self, dest, tripLen, city, country):
        self.dest = dest
        self.tripLen = tripLen
        self.city = city
        self.country = country


# Parse CSV and return a list
def openCSV(path):
    with open(path) as filename:
        return list(csv.reader(filter(lambda row: row[0] != '#', filename)))

# Takes a list of destinations and turns them into a list of Destination objects


def destListToObject(list):
    destination_objects = []
    for item in list:
        destination_objects.append(Destination(
            item[0], int(item[1]), item[2], item[3]))
    return destination_objects

# Returns either a headless or headed webdriver
# Parameters:
#   headless: (Bool) if True, create a headless driver
# Returns:
#   driver: (Selenium.webdriver) Selenium webdriver object

def getDriver(headless=True):
    if headless:
        options = Options()
        options.add_argument("--headless")
        return webdriver.Chrome()
    else:
        return webdriver.Chrome()

def arabic_to_english(string):
    arabic = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
    english = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(10):
        string = string.replace(arabic[i], english[i])
    return string

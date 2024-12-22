import urllib.request
import logging
from html.parser import HTMLParser

class WeatherScraper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.day = 0
        self.month = 0
        self.year = 0

        self.day_dictionary = {}
        self.history_dictionary = {}

        self.row_encountered = False
        self.date_encountered = False
        self.td_encountered = False

        self.end_of_month = False

        self.title_encountered = False
        self.furthest_reached = False
        self.display_past_month = ""

    def handle_starttag(self, tag, attr):
        try:
            if tag == "title":
                self.title_encountered = True
            elif tag == "tr" and not self.furthest_reached:
                self.row_encountered = True
            elif tag == "th" and self.row_encountered:
                self.date_encountered = True
            elif tag == "td" and self.row_encountered and not self.end_of_month:
                self.td_encountered = True
        except Exception:
            logging.exception("WeatherScraper - handle_starttag error: ")

    def handle_data(self, data):
        try:
            if self.title_encountered:
                current_month = data[data.index("for") + len("for") + 1 : data.index('-') - 1]

                if current_month == self.display_past_month:
                    self.furthest_reached = True

                self.display_past_month = current_month
                self.title_encountered = False

            if self.date_encountered:
                if data == "Sum":
                    self.end_of_month = True
                self.day = data
                self.date_encountered = False
                return

            if self.td_encountered:
                if "Mean" in self.day_dictionary:
                    return

                try:
                    temp = float(data)

                    if "Min" in self.day_dictionary:
                        self.day_dictionary["Mean"] = temp
                    if "Max" in self.day_dictionary:
                        self.day_dictionary["Min"] = temp
                    else:
                        self.day_dictionary["Max"] = temp

                    self.td_encountered = False
                except ValueError:
                    self.td_encountered = False
                    self.row_encountered = False
        except Exception:
            logging.exception("WeatherScraper - handle_data error: ")

    def handle_endtag(self, tag):
        try:
            if tag == "tr":
                if self.td_encountered:
                    self.history_dictionary[
                        f"{self.year}-{self.month}-{self.day}"] = self.day_dictionary
                self.day_dictionary = {}
                self.row_encountered = False
                self.td_encountered = False
        except Exception:
            logging.exception("WeatherScraper - handle_endtag error: ")

    def scrape(self, start_month, start_year, end_month=None, end_year=None):
        try:
            self.history_dictionary = {}

            self.month = start_month
            self.year = start_year

            while not self.furthest_reached:
                url = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2023&Day=1&Year={self.year}&Month={self.month}#"

                with urllib.request.urlopen(url) as response:
                    html = str(response.read())

                self.feed(html)
                self.close()

                if(end_month is not None and end_year is not None and
                   end_month == self.month and end_year == self.year):
                    return self.history_dictionary

                self.end_of_month = False
                self.year = self.year if self.month > 1 else self.year - 1
                self.month = self.month - 1 if self.month > 1 else 12

            return self.history_dictionary
        except Exception:
            logging.exception("WeatherScraper - scrape error: ")
    
import datetime
import logging
from menu import Menu
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor:
    def __init__(self):
        self.database = DBOperations()
        self.scraper = WeatherScraper()
        self.plotter = PlotOperations()
        self.database.initialize_db()

    def main(self):
        options = [("Download full set of weather data", self.retrieve_weather_data, {"mode": "f"}),
                   ("Update weather data", self.retrieve_weather_data, {"mode": "u"}),
                   ("Generate box plot", self.generate_box_plot),
                   ("Generate line plot", self.generate_line_plot),
                   ("Exit", Menu.CLOSE)]
        main_menu = Menu(message = "Pick one of the options: ", options = options)
        main_menu.open()

    def retrieve_weather_data(self, **options):
        today = datetime.datetime.now()
        year = today.year
        month = today.month

        temperature_dict = {}

        if options["mode"] == "f":
            temperature_dict = self.scraper.scrape(month, year)
        elif options["mode"] == "u":
            latest_date = self.database.get_latest_date()[0]
            date_list = latest_date.split('-')
            temperature_dict = self.scraper.scrape(month, year, date_list[1], date_list[0])

        self.database.save_data(temperature_dict)

    def generate_box_plot(self):
        data = self.database.fetch_data()
        start_year = int(input("Enter the start year for the box plot: "))
        end_year = int(input("Enter the end year for the box plot: "))
        self.plotter.plot_box_plot(start_year, end_year, data)

    def generate_line_plot(self):
        data = self.database.fetch_data()
        month = int(input("Enter the month for the line plot: "))
        year = int(input("Enter the year for the line plot: "))
        self.plotter.plot_line_plot(year, month, data)

logging.basicConfig(filename="errors.log",
                    format='%(asctime)s %(message)s')
processor = WeatherProcessor()
processor.main()

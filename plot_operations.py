import logging
import matplotlib.pyplot as pyplot

class PlotOperations:
    def __init__(self):
        self.database_fields = {
            "id": 0, "date": 1, "location": 2, "min_temp": 3, "max_temp": 4, "avg_temp": 5}

    def plot_box_plot(self, start_year, end_year, raw_data):
        try:
            plot_data = []

            for i in range(12):
                plot_data.append([])

            for row in raw_data:
                date = row[self.database_fields["date"]]

                month = int(date[date.index("-") + 1:date.rfind("-")])
                year = int(date[:date.index("-")])

                avg_temp = row[self.database_fields["avg_temp"]]

                if start_year <= year <= end_year:
                    mean_temperatures = plot_data[month - 1]
                    mean_temperatures.append(avg_temp)

            pyplot.boxplot(plot_data)
            pyplot.xlabel("Month")
            pyplot.ylabel("Temperature (Celcius)")
            pyplot.suptitle(f"Monthly Temperature Distribution for: {start_year} to {end_year}")
            pyplot.show()
        except Exception:
            logging.exception("PlotOperations - plot_box_plot error: ")

    def plot_line_plot(self, target_year, target_month, raw_data):
        try:
            temps = []
            dates = []
            temp_dict = {}

            for row in raw_data:
                date = row[self.database_fields["date"]]

                current_day = int(date[date.rfind("-") + 1:])
                current_month = int(date[date.index("-") + 1:date.rfind("-")])
                current_year = int(date[:date.index("-")])

                if current_year == target_year and current_month == target_month:
                    temp_dict[current_day] = row[self.database_fields["avg_temp"]]
    
            for i in range(len(list(temp_dict.keys()))):
                dates.append(f"{target_year}-{target_month}-{i + 1}")
                try:
                    temps.append(temp_dict[i + 1])
                except KeyError:
                    temps.append(None)

            fig, axis = pyplot.subplots()
            axis.plot(dates, temps)
            axis.set_xticklabels(axis.get_xticklabels(), rotation = 45, fontsize = 7, ha='right')
            pyplot.suptitle("Daily Avg Temperatures")
            pyplot.xlabel("Day of Month")
            pyplot.ylabel("Avg Daily Temp")
            pyplot.show()
        except Exception:
            logging.exception("PlotOperations - plot_line_plot error: ")
        
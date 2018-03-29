import csv_import
from event import Event

if __name__ == '__main__':
    importer = csv_import.csv_import("./ImportCSV/Round2-Bells.csv")
    surfer_pool = importer.generate_surfer_list()
    event = Event()
    result_dict = event.calculate_average_points(surfer_pool, 1000)
    result_dict2 = event.calculate_average_points(surfer_pool, 1000)
    a = result_dict == result_dict2
    b=1
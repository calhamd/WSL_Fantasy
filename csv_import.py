import csv
import surfer

class csv_import:
    def __init__(self, file_location):
        self.file_location = file_location

    def generate_surfer_list(self) -> [surfer]:
        with open(self.file_location, 'r', encoding='utf-8-sig') as csv_surfer_file:
            surfers = []
            surfer_reader = csv.DictReader(csv_surfer_file, delimiter=',')
            for cav_surfer in surfer_reader:
                surfers.append(surfer.Surfer(cav_surfer["Surfer"], int(cav_surfer["Odds"]), cav_surfer["Tier"], cav_surfer["Heat"]))
        return surfer.SurferPool(surfers)

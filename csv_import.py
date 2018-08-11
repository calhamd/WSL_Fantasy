import csv
import surfer

class csv_import:
    def __init__(self, file_location):
        self.file_location = file_location

    def generate_surfer_list(self) -> [surfer]:
        with open(self.file_location, 'r', encoding='utf-8-sig') as csv_surfer_file:
            surfers = []
            surfer_reader = csv.DictReader(csv_surfer_file, delimiter=',')
            for csv_surfer in surfer_reader:
                if "Rank" in csv_surfer and csv_surfer["Rank"] != '':
                    rank = int(csv_surfer["Rank"])
                else:
                    rank = -1
                surfers.append(surfer.Surfer(csv_surfer["Surfer"], int(csv_surfer["Odds"]), csv_surfer["Tier"], csv_surfer["Heat"], rank=rank))
        return surfer.SurferPool(surfers)

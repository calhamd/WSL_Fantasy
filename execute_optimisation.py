import csv_import
from event import Event
import itertools

if __name__ == '__main__':
    importer = csv_import.csv_import("./ImportCSV/Round10-Pipe.csv")
    surfer_pool = importer.generate_surfer_list()
    event = Event()
    print("Calculating Estimated Surfer Scores")
    result_dict = event.calculate_average_points(surfer_pool, 10000)

    ASurfers = surfer_pool.get_surfers_in_tier("A")
    BSurfers = surfer_pool.get_surfers_in_tier("B")
    CSurfers = surfer_pool.get_surfers_in_tier("C")

    total = []
    combosA = list(itertools.combinations(ASurfers, 2))
    combosB = list(itertools.combinations(BSurfers, 4))
    combosC = list(itertools.combinations(CSurfers, 2))
    total_len = len(combosA)*len(combosB)*len(combosC)
    print("Testing Combinations")
    for comboA in combosA:
        print('Testing Combos: {}%'.format(round((len(total)*100)/total_len), 2))
        for comboB in combosB:
            for comboC in combosC:
                aSccore = sum([result_dict[x.name] for x in comboA])
                bSccore = sum([result_dict[x.name] for x in comboB])
                cSccore = sum([result_dict[x.name] for x in comboC])
                combo_total = sum([aSccore, bSccore, cSccore])
                total.append((combo_total, list(comboA + comboB + comboC)))
    print("Sorting")
    total.sort(key=lambda s: s[0], reverse=True)
    print("Max score: {}".format(total[0][0]))
    for i in range(0, 4):
        print('{}: Estimated total {}'.format(i, total[i][0]))
        for surfer in total[i][1]:
            print('Surfer {}, scores {}'.format(surfer.name, result_dict[surfer.name]))
    a = 1


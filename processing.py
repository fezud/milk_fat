import os
import csv
import pickle

fat_percentage = "1.5"
concentrations = [0, 1/40, 1/80, 1/10, 1/160]

def get_data(fat_percentage=fat_percentage, concentrations=concentrations):
    directory = os.getcwd()

    filenames = os.listdir(f'{directory}\\{fat_percentage}')

    assert len(filenames) == len(concentrations), "Unknown concentrations"

    data = {}

    for filename in filenames:
        with open(f'{directory}\\{fat_percentage}\\{filename}') as file:
            reader = csv.reader(file)
            lambdas = []
            abs = []

            for row in reader:
                try:
                    float(row[0])
                except (TypeError, ValueError):
                    pass
                else:
                    lambdas.append(float(row[0]))
                    abs.append(float(row[1])) if float(row[1]) <=2 else abs.append(float(0))
            
            concentration = concentrations[filenames.index(filename)]
            data[concentration] = {"lambda": lambdas, "abs": abs}
    
    return data

# with open('zero.pickle', 'wb') as file:
#     pickle.dump({"lambda": data[0]["lambda"], "abs": data[0]["abs"]}, file)

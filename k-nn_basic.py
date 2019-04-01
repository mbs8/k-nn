import bisect
import csv

class instance:
    def __init__(self, id, params, classification):
        self.id = id
        self.params = params
        self.classification = classification
        self.distances = []

def readCsv(file): 
    params = []
    tests = []
    with open(file) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        line_count = 0
        for row in csvReader:
            if (line_count == 0):
                params = row
            elif (row != []):      
                test = instance(line_count, row[:len(row)-1], row[len(row)-1])
                tests.append(test)
            line_count += 1
    return (params, tests)

def main(): 
    params = []
    tests  = [] 

    params, tests = readCsv("./Datasets/CM1_software_defect_prediction.csv")


main()

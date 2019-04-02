import bisect
import csv
import math
import time

class Instance:
    def __init__(self, id, params, classification):
        self.id = id
        self.params = params
        self.classification = classification
        self.distances = []

    def euclideanDistance(self, datasetInstance, minArg, maxArg):
        distance = 0
        for i, param in enumerate(datasetInstance.params):
            distance += ((param - self.params[i]) ** 2) / (maxArg[i] - minArg[i])
        distance = math.sqrt(distance)       
        return distance
    
    def insertDistance(self, distance): 
        bisect.insort(self.distances, distance)

# atualiza o array de minimo e maximo de cada um dos parametros
def updateMinMax(row, minArg, maxArg):
    row = [float(i) for i in row]
    if (maxArg == []):
        minArg = list(row)
        maxArg = list(row)
        return minArg, maxArg
    else:
        for i, param in enumerate(row):
            if maxArg[i] < param:
                maxArg[i] = param
            if minArg[i] > param:
                minArg[i] = param
    return minArg, maxArg

# ler do arquivo csv e salva as informações nos arrays
def readCsv(file): 
    params = []
    tests = []
    maxArg = []
    minArg = []

    with open(file) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        line_count = 0
        for row in csvReader:
            if (line_count == 0):
                params = row
            elif (row != []):
                param = [float(i) for i in row[:len(row)-1]]     
                classification = row[len(row)-1]
                test = Instance(line_count-1, param, classification)
                tests.append(test)
                minArg, maxArg = updateMinMax(row[:len(row)-1], minArg, maxArg) 
            line_count += 1
    
    return (params, tests, minArg, maxArg)

def crossFold(dataSet, k, foldSize):
    params = []                     # array contendo o nome das colunas dos parametros
    tests  = []                     # array contendo todas as instancias no banco de dados
    maxArg = []                     # array contendo o maximo de cada parametro
    minArg = []                     # array contendo o minimo de cada parametro
    div = 1

    params, tests, minArg, maxArg = readCsv(dataSet)

    while ((div * foldSize) < len(tests)):
        testingSet  = tests[(div-1)*foldSize : div*foldSize]
        trainingSet = tests[ : (div-1)*foldSize] + tests[div*foldSize : len(tests)-1] 
        div += 1

        # calcula todas as distancias para i-esima instancia do conjunto de teste
        for testInstance in testingSet:
            for trainInstance in trainingSet:
                testInstance.insertDistance(testInstance.euclideanDistance(trainInstance, minArg, maxArg))

def main(): 
    kValues = [1]
    # kValues = [1,3,5,7,9,11,13,15]  # vetor dos valores de k
    foldSize = 10
    dataSets = ["./Datasets/CM1_software_defect_prediction.csv", "./Datasets/KC2_software_defect_prediction.csv"]

    for i, dataSet in enumerate(dataSets):
        print("DataSet " + str(i+1) + ":\n")
        for k in kValues:
            print("K = " + str(k))
            begin = time.time()
            crossFold(dataSet, k, foldSize)
            end = time.time()
            print("tempo: " + str(end - begin) + "\n")
        print("----------------------------------------------------------------------\n")
    

main()






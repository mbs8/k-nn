import csv
import math
import time



class Instance:
    def __init__(self, id, params, classification):
        self.id = id
        self.params = params
        self.classification = classification
        self.distancesToInstances = []

    def euclideanDistance(self, datasetInstance, minArg, maxArg):
        distance = 0
        for i, param in enumerate(datasetInstance.params):
            distance += ((param - self.params[i]) ** 2) / (maxArg[i] - minArg[i])
        distance = math.sqrt(distance)       
        return distance
    
    def insertDistance(self, distanceToInstance, instance): 
        distInst = (distanceToInstance, instance)
        if self.distancesToInstances == []:
            self.distancesToInstances.append(distInst)
        else:
            for i, (dist, _) in enumerate(self.distancesToInstances):
                if dist > distanceToInstance:
                    self.distancesToInstances.insert(i, distInst)
                    return
            self.distancesToInstances.append(distInst)
    
    # testa se a instancia foi classificada corretamente
    def classify(self, numNeighbor):
        classTrue = 0 
        classFalse = 0

        for i in range(0, numNeighbor):
            if self.distancesToInstances[i][1].classification == 'true' or self.distancesToInstances[i][1].classification == 'yes':
                classTrue  += 1
            else:
                classFalse += 1

        if ((classTrue < classFalse) and (self.classification == 'false' or self.classification == 'no')):
            return True
        if ((classTrue > classFalse) and (self.classification == 'true' or self.classification == 'yes')):
            return True
        return False

                     


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
    hit    = 0                      # numero de acertos em cada teste de crossfold
    accuracy = 0
    div = 1                             

    params, tests, minArg, maxArg = readCsv(dataSet)

    while ((div * foldSize) < len(tests)):
        testingSet  = tests[(div-1)*foldSize : div*foldSize]
        trainingSet = tests[ : (div-1)*foldSize] + tests[div*foldSize : len(tests)-1] 
        div += 1

        # calcula todas as distancias para i-esima instancia do conjunto de teste e classifica de acordo com os k vizinhos mais proximos
        for testInstance in testingSet:
            for trainInstance in trainingSet:
                testInstance.insertDistance((testInstance.euclideanDistance(trainInstance, minArg, maxArg)), trainInstance)
                if (testInstance.distancesToInstances[0] == 0):
                    break
            if testInstance.classify(k):
                hit += 1
        
        accuracy += (hit/len(testingSet))
        hit = 0
    
    print("Accuracy: %.2f%%\n" % ((accuracy/div) * 100))
        
                

                

def main(): 
    kValues = [1,3,5,7,9,11,13,15]  # vetor dos valores de k
    dataSets = ["./Datasets/CM1_software_defect_prediction.csv", "./Datasets/KC2_software_defect_prediction.csv"]
    foldSize = 10
    totalTime = 0
    timePerDataSet = 0
    

    for i, dataSet in enumerate(dataSets):
        print("DataSet " + str(i+1) + ":\n")
        for k in kValues:
            print("K = " + str(k))
            begin = time.time()
            crossFold(dataSet, k, foldSize)
            end = time.time()
            timePerDataSet += end - begin
            print("tempo: %.2f\n" % (end - begin))
        totalTime += timePerDataSet
        print("Tempo(%s): %.2f" % (dataSets[i],timePerDataSet))
        print("----------------------------------------------------------------------\n")
        timePerDataSet = 0

    print("Tempo total = %.2f" % (totalTime))
    
        
    

main()






#Train motion data using HMM and output hidden state sequence.
from hmmlearn.hmm import GaussianHMM
import numpy as np
from matplotlib import cm, pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator
import re



def readTrain(filename, trainData, SegLength):
    fid = open(filename, 'r')
    feature = []
    sequence = []
    for line in fid :
        #print(line, end='')
        if line == '\n':
            trainData.append(sequence)
            SegLength.append(len(sequence))
            sequence = []
            continue
        temp = re.split('\s+',line)
        for item in temp :
            if item == '':
                continue
            else :
                feature.append(float(item))
        sequence.append(feature)
        feature = []


def main():
    filename = 'trainData01.txt'
    trainData = []
    seglength = []
    readTrain(filename, trainData, seglength)
    finalData = []
    for items in trainData:
        for item in items :
            finalData.append(item)
    print(trainData)
    print(seglength)
    model = GaussianHMM(n_components = 8, covariance_type = "diag" , n_iter = 1000).fit(finalData, seglength)
    hidden_states = model.predict(finalData)
    #print(hidden_states)
    print(len(hidden_states))
    print("Transition matrix")
    print(model.transmat_)
    print("Means and vars of each hidden state")
    for i in range(model.n_components):
        print("{0}th hidden state".format(i))
        print("mean = ", model.means_[i])
        print("var = ", np.diag(model.covars_[i]))
        print()

if __name__ == '__main__':
  main()



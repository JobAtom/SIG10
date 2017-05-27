#Train motion data using HMM and output hidden state sequence.
from hmmlearn.hmm import GaussianHMM
import numpy as np
from matplotlib import cm, pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator
import re
from sklearn.externals import joblib




def readTrain(filenames, trainData, SegLength):
    for filename in filenames:
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
    filenames = ['trainData01.txt', 'trainData02.txt', 'trainData03.txt','trainData04.txt','trainData05.txt', 'trainData06.txt', 'trainData07.txt']
    trainData = []
    seglength = []
    readTrain(filenames, trainData, seglength)
    finalData = []
    for items in trainData:
        for item in items :
            finalData.append(item)
    print(trainData)
    print(seglength)
    model = GaussianHMM(n_components = 7, covariance_type = "diag" , n_iter = 1000, algorithm = 'viterbi').fit(finalData, seglength)
    #output state sequences
    output = open('HMMoutput01.txt','w')
    for data in trainData:
        hs = model.predict(data)
        for item in hs:
            output.write(str(item))
            output.write(' ')

        #output.write(str(hs))
        output.write('\n')
    output.close()
    #hidden_states = model.predict(finalData)
    #print(hidden_states)
    #print(len(hidden_states))
    print("Transition matrix")
    print(model.transmat_)
    print("Means and vars of each hidden state")
    for i in range(model.n_components):
        #print("{0}th hidden state".format(i))
        print("mean = ", model.means_[i])
        print("var = ", np.diag(model.covars_[i]))
        print()
    joblib.dump(model, 'HMMModel.pkl')


if __name__ == '__main__':
  main()



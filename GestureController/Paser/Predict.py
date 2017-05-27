import pycrfsuite
from hmmlearn.hmm import GaussianHMM
import numpy as np
from numpy import linalg as LA
import sklearn
from sklearn.externals import joblib
import re


StatesNum = 7
delayTime = [0.1, 0.06, 0.06, 0.05, 0.13, 0.04, 0.11]
def readData(filenames, data):
    fid = open(filenames, 'r')
    oneSet = []
    for line in fid :
        if line == '\n' :
            oneSet = []
            continue
        items = re.split('\s+', line)
        for item in items :
            if item == '' :
                continue
            oneSet.append(float(item))
        data.append(oneSet)
        oneSet = []
   # print(data)
    fid.close()


def sound2Features(soundfiles) :
    for soundfile in soundfiles:
        trainFea = []
        features = []
        fsound = open(soundfile, 'r')
        for line in fsound :
            if line == '\n' :
                if len(features)!= 0 :
                    trainFea.append(features)
                    features = []
                continue

            items = re.split(r'\s+', line)
            feature = {'F': float(items[0]),'I': float(items[1]), 'L': float(items[2])}
            features.append(feature)
        if len(features)!= 0 :
            trainFea.append(features)
            features = []
    return trainFea


def ReadSeg(filenames) :
    AllSeg = []
    for file in filenames :
        fid = open(file, 'r')
        for line in fid :
            feature = []
            if line == '\n' :
                continue
            item = re.split(r'\s+', line)
            for i in item :
                if i != '' :
                    feature.append(float(i))
            AllSeg.append(feature)
    return AllSeg

def GetLength(filenames):
    SegLength = []
    for file in filenames:
        fid = open(file, 'r')
        for line in fid:
            if line == '\n':
                continue
            items = re.split(r'\s+', line)
            tempSeg = []
            for item in items:
                if item == '':
                    continue
                tempSeg.append(int(item))
            tempSeg = sorted(tempSeg)
            last = tempSeg[0]
            for i in range(1, len(tempSeg)):
                if tempSeg[i]-last ==0:
                    continue
                SegLength.append(int((tempSeg[i] - last)/4.004))
                last = tempSeg[i]

    return SegLength

def GetStartFrame(filenames):
    startFrame = []
    filecount = 0
    for file in filenames :
        fid = open(file, 'r')
        for line in fid:
            if line == '\n':
                continue
            items = re.split(r'\s+', line)
            tempSeg = []
            for item in items:
                if item == '':
                    continue
                tempSeg.append(int(item))
            tempSeg = sorted(tempSeg)
            for i in range(len(tempSeg)-1):
                if tempSeg[i] == tempSeg[i+1]:
                    continue
                startFrame.append((round(((tempSeg[i]/120 - delayTime[filecount]) * 29.97)), filecount))
        filecount += 1
    return startFrame

def DeleteShortSeg(AllSeg, SegLength, StartFrame):
    print('delete very short segmentation')
    count = 0
    while count < len(AllSeg):
        if count > len(AllSeg) - 1:
            break
        if SegLength[count] < 1 :
            del AllSeg[count]
            del StartFrame[count]
            SegLength.remove(SegLength[count])
        else :
            count += 1



def S(table, Segi, Segj, framei, framej):
    return table['%s,%s,%s,%s' %(Segi,Segj,framei,framej)]

    #print('calculate S')

def calculateTable(AllSeg, SegLength, trcFiles):
    table = {}
    for i in range(len(AllSeg)):
        for framei in range(SegLength[i]):
            for j in range(len(AllSeg)):
                for framej in range(SegLength[j]):
                    if i == j :
                        if framei + 1 == framej and framei < SegLength[i] - 1:
                            table.update({('%s,%s,%s,%s' % (i, j, framei, framej)): 0})
                        else :
                            table.update({('%s,%s,%s,%s' % (i, j, framei, framej)): np.inf})
                        #print('non zero')
                        #if framei + 1 == framej and framei < SegLength[i] - 1:

                    elif framei == (SegLength[i]-1) and framej ==0 and i < len(AllSeg)-1 and j>0 :
                        if i == j - 1 :
                            table.update({('%s,%s,%s,%s' % (i, j, framei, framej)): 0})
                        else :
                            Dsp = LA.norm(np.array(AllSeg[i+1])-np.array(AllSeg[j])) + LA.norm(np.array(AllSeg[i]-np.array(AllSeg[j-1])))
                            table.update({('%s,%s,%s,%s' %(i,j,framei,framej)):Dsp})
                        #print('non zero')
                    else :
                        table.update({('%s,%s,%s,%s' %(i,j,framei,framej)):np.inf})
    return table

def calculateE(rt, Segs, segcount):
    #print('calculate a good seg')
    #load HMM model get mean value
    model = joblib.load('HMMModel.pkl')
    #count the segmentation
    #countseg = 0
    #minCount = 100000
    #minSum = 100000
    #for seg in Segs :
    sum = 0
    for state in range(0,StatesNum):
        s = rt[state]*LA.norm(np.array(model.means_[state])-np.array(Segs[segcount]))
        sum += s
        #if sum <= minSum :
        #    minSum = sum
        #    minCount = countseg
        #countseg += 1
    sum = sum / 5000
    return sum

def main():
    #load HMM model
    Segfiles = ['trainData01.txt']#, 'trainData02.txt', 'trainData03.txt']#,'trainData04.txt']#,'trainData05.txt', 'trainData06.txt', 'trainData07.txt']
    FrameFiles = ['SegTime01.txt']#, 'SegTime02.txt', 'SegTime03.txt']#, 'SegTime04.txt']#, 'SegTime05.txt', 'SegTime06.txt', 'SegTime07.txt']
    trcFiles = [r'C:/Users/CGML/Desktop/WorkSpace/twopartytrc/Day2-Jonathan-Stephen-Trial001-Mocap-withfingers-Jonathan.trc']
    SegLength = GetLength(FrameFiles)
    AllSeg = ReadSeg(Segfiles)
    SegStartFrame = GetStartFrame(FrameFiles)

    DeleteShortSeg(AllSeg, SegLength, SegStartFrame)

    print(len(AllSeg))
    print(len(SegStartFrame))
    #calculate all segmentations' cost
    print('calculating frame table...')
    table = calculateTable(AllSeg, SegLength, trcFiles)
    #print(table['127,128,7,0'])
    #print(SegLength[128])
    #for item in table:
    #    print(item)

    #print(AllSeg)



    model = joblib.load('HMMModel.pkl')
    for i in range(model.n_components):
        #print("{0}th hidden state".format(i))
        print("mean = ", model.means_[i])
        print("var = ", np.diag(model.covars_[i]))
        print()
    filenames = ['TestResultTemp.txt']
    #filenames = ['soundFile\soundresult01.txt']
    soundSegFile = [r'soundFile\soundSeg07.txt']
    motionSegFile = ['SegTime07.txt']
    Data = sound2Features(filenames)
    #load CRF model
    tagger = pycrfsuite.Tagger()
    tagger.open('crfoutput.crfsuite')

    print(tagger.labels())
    #for item in Data:
    #    tagger.set(item)
    #    print('Predicted:', ' '.join(tagger.tag()))
    resSeg = []
    foutput = open('finalResult.txt', 'w')

    numCount = 0
    print(len(Data))
    for item in Data :
        tagger.set(item)
        Qt = []
        Qt_1 = []
        minPath = []
        finalPath = []
        #nulllist = []
        #init Qt
        for i in range(len(AllSeg)):
            temp = []
            temp_1 = []
            tpath = []
            tfpath = []
            for j in range(SegLength[i]):
                temp.append(0)
                temp_1.append(0)
                tpath.append([])
                tfpath.append([])
            Qt.append(temp)
            Qt_1.append(temp_1)
            minPath.append(tpath)
            finalPath.append(tfpath)
            #minPath.append(nulllist)
        #finalPath = minPath[:]
        print(len(item))
        for i in range(len(item)):
            print('%s th frame' %(i))
            rt = []
            for num in range(0, StatesNum):
                rt.append(tagger.marginal(('%s' %(num)), i))
            #rt.append(tagger.marginal('0', i))
            #rt.append(tagger.marginal('1', i))
            #rt.append(tagger.marginal('2', i))
            #rt.append(tagger.marginal('3', i))
            #rt.append(tagger.marginal('4', i))
            for j in range(len(AllSeg)):
                E = calculateE(rt, AllSeg, j)
                #print(E)
                #for k in range(len(Qt)):
                for framej in range(SegLength[j]):
                    Qmin = np.inf
                    smallFrame = np.inf
                    smallSeg = np.inf
                    for k in range(len(AllSeg)):
                        for framei in range(SegLength[k]):
                            Qtemp = S(table, k, j ,framei, framej ) + Qt_1[k][framei]
                            if Qmin > Qtemp :
                                Qmin = Qtemp
                                smallFrame = framei
                                smallSeg = k
                                #print(smallFrame)
                                #print(smallSeg)
                                #print(Qmin)
                                #print(Qtemp)


                                    #minPath[j][framej].append((smallSeg, smallFrame))
                    if smallSeg != np.inf and smallFrame != np.inf :
                        finalPath[j][framej] = minPath[smallSeg][smallFrame][:]
                        finalPath[j][framej].append((smallSeg, smallFrame))
                    Qt[j][framej] = Qmin + E
                    #else :
                        #Qt[j][framej] = np.inf
            Qt_1 = Qt[:]
            for a in range(len(finalPath)) :
                for b in range(len(finalPath[a])) :
                    minPath[a][b] = finalPath[a][b][:]
            #minPath = finalPath[:]




        value = np.inf
        finalSeg = 0
        finalFrame = 0
        for i in range(len(AllSeg)):
            for framei in range(SegLength[i]):
                if value > Qt[i][framei]:
                    finalSeg = i
                    finalFrame = framei
                    value = Qt[i][framei]

        print(finalPath[finalSeg][finalFrame])
        FinalResult = finalPath[finalSeg][finalFrame]
        #write final result to file
        for num in range(len(FinalResult)):
            SegNum = FinalResult[num][0]
            offset = FinalResult[num][1]
            StartFrame = SegStartFrame[SegNum][0]
            filenum = SegStartFrame[SegNum][1]
            foutput.write('%s %s' %(filenum, StartFrame + offset))
            foutput.write('\n')
        #foutput.close()
        #numCount += 1
        #if numCount == 6:
          #  foutput.close()
    foutput.close()


            #resSeg.append(calculateE(rt, AllSeg, i))

            #print('0:', tagger.marginal('0',i))
            #print('1:',  tagger.marginal('1',i))
            #print('2:',  tagger.marginal('2',i))
            #print('3:',  tagger.marginal('3', i))
            #print('4:',  tagger.marginal('4', i))

    #print(len(resSeg))









if __name__=='__main__':
    main()

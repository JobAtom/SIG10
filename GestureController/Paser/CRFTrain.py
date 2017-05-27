#train data useing CRF based on HMM states
import pycrfsuite
import sklearn
import re
import numpy as np

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

#how to label one segmentation, one list in finalMark means the label of one sequence.
def MarkTrainData(soundSegfile, motionSegfile, finalMark, replacedDur):
    for i in range(len(soundSegfile)):
        soundSeg = []
        motionSeg = []
        #finalMark = []
        #soundfiles = ''
        #motionfiles = ''
        tempMark = []
        readData(soundSegfile[i], soundSeg)
        readData(motionSegfile[i], motionSeg)
        #motionSeg = sorted(motionSeg)
        if len(soundSeg) != len(motionSeg) :
            print('sound and motion are not equal')
            return
        length = len(soundSeg)
        count = 0
        while count < length:
            countM = 1
            #countS = 0
            oneSound = []
            motionSeg[count]=sorted(motionSeg[count])
            #startF = soundSeg[count][0]
            for csound in range(1,len(soundSeg[count])) :
                startTime = soundSeg[count][csound-1] + delayTime[i]
                endTime = soundSeg[count][csound] + delayTime[i]
                endFrame = round(endTime * 120)
                marked = False
                if motionSeg[count][countM] < endFrame:
                    while countM < len(motionSeg[count]) and motionSeg[count][countM] < endFrame :
                        curFrame = motionSeg[count][countM]
                        dur = float(curFrame)/120 - startTime
                        if dur < 0 :
                            dur = 0.001
                        replacedDur.append(dur)
                        oneSound.append(countM)
                        startTime = float(curFrame) /120
                        marked = True
                        countM += 1
                else :
                    oneSound.append(countM)
                if marked:
                    startTime = soundSeg[count][csound] + delayTime[i]
                    curFrame = motionSeg[count][countM]
                    dur = float(curFrame) / 120 - startTime
                    oneSound.append(countM)
                    if dur < 0 :
                        dur = 0.001
                    replacedDur.append(dur)
                tempMark.append(oneSound)
                oneSound = []
            finalMark.append(tempMark)
            tempMark = []
            count += 1


def sound2Features(soundfiles) :
    trainFea = []
    for soundfile in soundfiles:
        features = []
        fsound = open(soundfile, 'r')
        for line in fsound :
            if line == '\n':
                if len(features)!= 0 :
                    trainFea.append(features)
                    features = []
                continue
            items = re.split(r'\s+', line)
            feature = {'F': float(items[0]),'I': float(items[1]), 'L': float(items[2])}
            features.append(feature)
    return trainFea

def GetResult(HMMfile):
    sequences = open(HMMfile, 'r')
    stateSequences = []
    for line in sequences :
        setemp = []
        items = re.split('\s+', line)
        for item in items :
            if item == '':
                continue
            setemp.append(int(item))
        stateSequences.append(setemp)
    return stateSequences

def sound2Label(finalMark, HMMOutput) :
    StateSequence = GetResult(HMMOutput)
    labelSequences = []
    #print(len(StateSequence))
    #print(len(finalMark))
    if len(finalMark) != len(StateSequence) :
        print('the length of training sequences is not equal to the length of state sequences')
        exit(-1)
    #count state sequences
    countSS = 0
    ltemp = []
    lstemp = []
    for items in finalMark:
        for item in items :
            for l in item :
                if(l-1>=len(StateSequence[countSS])):
                    #print('error')
                    #print(countSS)
                    continue
                #ltemp +=str(StateSequence[countSS][l-1])
                ltemp.append(StateSequence[countSS][l-1])
            lstemp.append(ltemp)
            ltemp = []
            #countSS += 1
        labelSequences.append(lstemp)
        lstemp = []
        countSS += 1
        #print(countSS)
    return labelSequences

def StanderFea_Label(features, labels, trainFea, trainLabels, replacedDur):
    #finalFeature = []
    #finalLabel = []
    countFea = 0
    ctemp = 0
    for item in labels :
        #print(item)
        tempFea = []
        tempLab = []
        for i in range(len(item)) :
            if len(item[i]) == 1:
                tempFea.append(features[countFea][i])
                tempLab.append(str(item[i][0]))
            else :
                count = len(item[i])-1
                for it in item[i] :
                    tempLab.append(str(it))
                while count >= 0 :
                    features[countFea][i]['L']=replacedDur[ctemp]
                    ctemp += 1
                    tempFea.append(features[countFea][i])
                    count -= 1
        trainFea.append(tempFea)
        trainLabels.append(tempLab)
        countFea += 1
    #trainFea = finalFeature
    #trainLabels = finalLabel









def main():

    soundfiles = [r'soundFile\soundresult01.txt','soundFile\soundresult02.txt','soundFile\soundresult03.txt','soundFile\soundresult04.txt','soundFile\soundresult05.txt','soundFile\soundresult06.txt','soundFile\soundresult07.txt']
    soundSegFile = [r'soundFile\soundSeg01.txt', 'soundFile\soundSeg02.txt', 'soundFile\soundSeg03.txt', 'soundFile\soundSeg04.txt', 'soundFile\soundSeg05.txt', 'soundFile\soundSeg06.txt','soundFile\soundSeg07.txt']
    motionSegFile = ['SegTime01.txt','SegTime02.txt', 'SegTime03.txt', 'SegTime04.txt', 'SegTime05.txt', 'SegTime06.txt', 'SegTime07.txt']
    HMMoutput = 'HMMoutput01.txt'
    finalMark = []
    replacedDur = []
    MarkTrainData(soundSegFile, motionSegFile, finalMark, replacedDur)
    count = 0
    for items in finalMark:
        for item in items:
            if len(item)>1:
                for j in item:
                    count+=1
    print(count)
    print(len(replacedDur))
    print(replacedDur)
    trainFea = sound2Features(soundfiles)
    labels = sound2Label(finalMark, HMMoutput)
    finalTrainFeature = []
    finalTrainLabels = []
    StanderFea_Label(trainFea, labels, finalTrainFeature, finalTrainLabels, replacedDur)
    print(finalTrainFeature)
    print(finalTrainLabels)
    #print(len(labels))
    #print(len(finalMark))
    #print(labels)


    trainer = pycrfsuite.Trainer(verbose=False)
    trainer.select('lbfgs', type='crf1d')
    print(trainer.params())
    for xseq, yseq in zip(finalTrainFeature, finalTrainLabels):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0,  # coefficient for L1 penalty
        'c2': 1e-1, # coefficient for L2 penalty
        'max_iterations': 1000,  # stop earlier
        #'num_memories' : 3,
        #'epsilon' : 1e-10,
        # include transitions that are possible, but not observed
         #'feature.possible_transitions': True,
         #'feature.minfreq' : 0.1
    })
    trainer.train('crfoutput.crfsuite')

    #show results
    filenames = ['soundFile\soundresult01.txt']
    soundSegFile = [r'soundFile\soundSeg01.txt']
    motionSegFile = ['SegTime01.txt']
    Data = sound2Features(filenames)


    tagger = pycrfsuite.Tagger()
    tagger.open('crfoutput.crfsuite')

    for i in range(len(Data)):
        tagger.set(Data[1])
        print(tagger.probability(['0','0']))
        print('Predicted: ', ' '.join(tagger.tag()))
    #for item in Data:
    #    tagger.set(item)
    #    for i in range(len(item)):
    #        print('0:', tagger.marginal('0', i))
    #        print('1:', tagger.marginal('1', i))
    #        print('2:', tagger.marginal('2', i))
    #        print('3:', tagger.marginal('3', i))
    #        print('4:', tagger.marginal('4', i))

if __name__=='__main__':
    main()

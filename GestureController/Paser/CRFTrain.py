#train data useing CRF based on HMM states
import pycrfsuite
import sklearn
import re
import numpy as np

delayTime = 0.01

#read sound features for each segmentation
def readSoundFeatures(soundfiles, durfiles, sequence):
    fsound = open(soundfiles, 'r')
    fdur = open(durfiles, 'r')

def readData(filenames, data):
    fid = open(filenames, 'r')
    oneSet = []
    for line in fid :
        items = re.split('\s+', line)
        for item in items :
            if item == '' :
                continue
            oneSet.append(float(item))
        data.append(oneSet)
        oneSet = []


def MarkTrainData(soundSeg, motionSeg):
    soundSeg = []
    motionSeg = []
    finalMark = []
    soundfiles = ''
    motionfiles = ''
    readData(soundfiles, soundSeg)
    readData(motionfiles, motionSeg)
    motionSeg = sorted(motionSeg)
    tempMark = []
    if len(soundSeg) != len(motionSeg) :
        print('sound and motion are not equal')
        return
    length = len(soundSeg)
    count = 0
    while count < length:
        countM = 1
        countS = 0
        oneSound = []
        for item in soundSeg :
            endTime = item - delayTime
            endFrame = endTime * 120
            if motionSeg(countM) <= endFrame:
                while motionSeg(countM) <= endFrame:
                    oneSound.append(countM)
                    countM += 1
            else :
                oneSound.append(countM)
            tempMark.append(oneSound)
        finalMark.append(tempMark)
        tempMark = []
        count += 1









def main():
    print('hello')
    soundfiles = ''
    durfiles = 'SegTime01.txt'


if __name__=='__main__':
    main()

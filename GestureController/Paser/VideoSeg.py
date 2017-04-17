<<<<<<< HEAD
import cv2
import io
import re



def readTxT(frameData):
    fid=open('SegTime.txt','r')
    for line in fid:
        temp = re.split('\s+',line)
        tempFrame = []
        for item in temp:
            if item != '':
                tempFrame.append(int(item))

        frameData.append(tempFrame)

    fid.close()

def OpenVideo(frameData):
    cap = cv2.VideoCapture('renderdata\MichelleTrial001.mp4')
    countFrame = 0
    t = 1
    isStart = False
    startData = []
    endData = []
    pauseData = []

    for items in frameData :
        startData.append(round(items[0]/5))
        endData.append(round(items[1]/5))
        for i in range(2,len(items)):
            pauseData.append(round(items[i]/5))

    print(startData)
    print(endData)

    while(cap.isOpened()):
        cliTime = False



        ret, frame = cap.read()
        startFrame = frame.copy()
        midFrame = frame.copy()
        endFrame = frame.copy()

        if countFrame in startData :
            cv2.putText(startFrame, "start: " + str(countFrame), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)
            t = 4000
            cliTime = True
            cv2.imshow('frame', startFrame)
            cv2.waitKey(1*t)
        if countFrame in pauseData :
            cv2.putText(midFrame, "mid: " + str(countFrame), (50, 500), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)
            t = 1000
            cliTime = True
            cv2.imshow('frame', midFrame)
            cv2.waitKey(1*t)
        if countFrame in endData :
            cv2.putText(endFrame, "end: " + str(countFrame), (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)
            t = 4000
            cliTime = True
            cv2.imshow('frame', endFrame)
            cv2.waitKey(1*t)

        if cliTime == False:
            t = 1
            cv2.imshow('frame', frame)
            cv2.waitKey(1*t)

        countFrame += 1


    cap.release()
    cv2.destroyAllWindows()


def main():
    #print('helloworld')
    frameData=[]
    readTxT(frameData)
    OpenVideo(frameData)
    print(frameData)

if __name__=='__main__':
    main()
=======
import cv2
import io
import re



def readTxT(frameData):
    fid=open('SegTime.txt','r')
    for line in fid:
        temp = re.split('\s+',line)
        tempFrame = []
        for item in temp:
            if item != '':
                tempFrame.append(int(item))

        frameData.append(tempFrame)

    fid.close()

def OpenVideo(frameData):
    cap = cv2.VideoCapture('renderdata\MichelleTrial001.mp4')
    countFrame = 0
    t = 1
    isStart = False
    startData = []
    endData = []
    pauseData = []

    for items in frameData :
        startData.append(round(items[0]/5))
        endData.append(round(items[1]/5))
        for i in range(2,len(items)):
            pauseData.append(round(items[i]/5))

    print(startData)
    print(endData)

    while(cap.isOpened()):
        cliTime = False



        ret, frame = cap.read()
        startFrame = frame.copy()
        midFrame = frame.copy()
        endFrame = frame.copy()

        if countFrame in startData :
            cv2.putText(startFrame, "start: " + str(countFrame), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)
            t = 4000
            cliTime = True
            cv2.imshow('frame', startFrame)
            cv2.waitKey(1*t)
        if countFrame in pauseData :
            cv2.putText(midFrame, "mid: " + str(countFrame), (50, 500), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)
            t = 1000
            cliTime = True
            cv2.imshow('frame', midFrame)
            cv2.waitKey(1*t)
        if countFrame in endData :
            cv2.putText(endFrame, "end: " + str(countFrame), (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)
            t = 4000
            cliTime = True
            cv2.imshow('frame', endFrame)
            cv2.waitKey(1*t)

        if cliTime == False:
            t = 1
            cv2.imshow('frame', frame)
            cv2.waitKey(1*t)

        countFrame += 1


    cap.release()
    cv2.destroyAllWindows()


def main():
    #print('helloworld')
    frameData=[]
    readTxT(frameData)
    OpenVideo(frameData)
    print(frameData)

if __name__=='__main__':
    main()
>>>>>>> e292d594e52180987cc5afefde20166751446e47

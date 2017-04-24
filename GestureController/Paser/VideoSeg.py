
import cv2
import io
import re
import pygame
from time import time


def readTxT(frameData):
    fid=open('SegTime01.txt','r')
    for line in fid:
        temp = re.split('\s+',line)
        tempFrame = []
        for item in temp:
            if item != '':
                tempFrame.append(int(item))

        frameData.append(tempFrame)

    fid.close()

def OpenVideo(frameData):
    filename = r'c:\Users\CGML\Desktop\videodata\MichelleTrial001.mp4'
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    #print(fps)
    countFrame = 0
    t = 1
    isStart = False
    startData = []
    endData = []
    pauseData = []

    for items in frameData :
        startData.append(round(items[0]/4.004))
        endData.append(round(items[1]/4.004))
        for i in range(2,len(items)):
            if len(pauseData)!=0 and pauseData[-1] != round(items[i]/4.004):
                    pauseData.append(round(items[i]/4.004))
            else:
                pauseData.append(round(items[i]/4.004))

   # print(startData)
    #print(pauseData)
    #print(endData)
    if 3 in startData:
        print('have 3')
    pygame.mixer.init()
    pygame.mixer.music.load(r"Day1-Michelle-Shenae-Trial001-Audio.mp3")

    startPlay = False
    DelayTime = 0.01
    DelayFrame = round(0.0*29.97)


    #ot = 0
    while(cap.isOpened()):


        #ct = time()
        #if ot ==0:
        #    ot = ct
        #else:
        #    print(ct - ot)
        #    ot = ct
        cliTime = False


        soundTime = pygame.mixer.music.get_pos()/1000
        print(soundTime)
        videoTime = countFrame / 29.97
        print(videoTime)
        print('_______________________')
        if soundTime <= videoTime-DelayTime:
            pygame.mixer.music.unpause()
        #else:
           # pygame.mixer.music.pause()
        ret, frame = cap.read()
        startFrame = frame.copy()
        midFrame = frame.copy()
        endFrame = frame.copy()

        if(countFrame > DelayFrame and not startPlay):
            startPlay = True
            pygame.mixer.music.play()
        if countFrame in pauseData :
            pygame.mixer.music.pause()
            cv2.putText(midFrame, "mid: " + str(countFrame), (50, 500), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)
            cliTime = True
            cv2.imshow('frame', midFrame)
            cv2.waitKey(600)
            #pygame.mixer.music.unpause()
        if countFrame in endData :
            pygame.mixer.music.pause()
            cv2.putText(endFrame, "end: " + str(countFrame), (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)
            cliTime = True
            cv2.imshow('frame', endFrame)
            cv2.waitKey(2000)
            #pygame.mixer.music.unpause()
        if countFrame in startData :
            pygame.mixer.music.pause()
            cv2.putText(startFrame, "start: " + str(countFrame), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)
            cliTime = True
            cv2.imshow('frame', startFrame)
            pygame.mixer.music.pause()
            cv2.waitKey(2000)
            #pygame.mixer.music.unpause()
            #pygame.mixer.music.set_pos(soundtime)
            #pygame.mixer.music.play()
        if cliTime == False:
            cv2.imshow('frame', frame)
            if soundTime> videoTime-DelayTime :
                cv2.waitKey(1)
            else:
                cv2.waitKey(31)
            #pygame.mixer.music.unpause()
        countFrame += 1


    cap.release()
    cv2.destroyAllWindows()


def main():
    frameData=[]
    readTxT(frameData)
    OpenVideo(frameData)
    print(frameData)

if __name__=='__main__':
    main()


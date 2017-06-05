import cv2
import numpy as np


def main():
    print('Begin combine')
    video1 = 'oriVideo.avi'
    video2 = 'video2.avi'
    cap1 = cv2.VideoCapture(video1)
    cap2 = cv2.VideoCapture(video2)
    length1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
    length2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))

    length = min(length1, length2)
    count = 1
    cap1.set(1, 1)
    ret1, frame1 = cap1.read()

    cap2.set(1,1)
    ret2, frame2 = cap2.read()

    height1, width1, layers1 = frame1.shape
    height2, width2, layers2 = frame2.shape

    newFrame = np.hstack((frame1, frame2))

    newFrame = cv2.resize(newFrame, (1280, 480), interpolation = cv2.INTER_CUBIC)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    video = cv2.VideoWriter('CombinedVideo.avi', fourcc, 29.97, (1280, 480))
    while count < length-1 :
        cap1.set(1, count)
        cap2.set(1, count)
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()


        newFrame = np.hstack((frame1, frame2))

        newFrame = cv2.resize(newFrame, (1280, 480), interpolation = cv2.INTER_CUBIC)
        video.write(newFrame)
        count += 1

    video.release()

    #cv2.imshow('result', newFrame)
    #cv2.waitKey(10000)





if __name__ == "__main__" :
    main()
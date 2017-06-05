import re
import cv2

delayTime = [0.1, 0.06, 0.06, 0.05, 0.13, 0.04, 0.11]

def GetResult(filename):
    list = []
    count = 0
    fid = open(filename, 'r')
    for line in fid :
        items = re.split('\s+', line)
        temp = []
        for item in items :
            if item == '':
                continue
            temp.append(int(item))
        list.append(temp)
    count = len(list)
    return list, count

def GetFrames(filename, count) :
    list = []
    fid = open(filename, 'r')
    for line in fid :
        if line == '\n':
            continue
        if count == 0 :
            break

        items = re.split('\s+', line)
        temp = []
        temp.append(round((float(items[0])/120 + delayTime[0])*29.97))
        temp.append(round((float(items[1])/120 + delayTime[0])*29.97))
        list.append(temp)
        count -= 1
    return list

def main():
    print('hello')
    filename = 'finalResult.txt'
    sigFile = 'SegTime01.txt'
    countFrame = 6
    StartToEnd = GetFrames(sigFile, countFrame)
    print(StartToEnd)
    videos = [r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial001.mp4',
              r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial002.mp4',
              r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial003.mp4',
              r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial004.mp4',
              r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial005.mp4',
              r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial006.mp4',
              r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial007.mp4']
    filename = 'finalResult.txt'
    cap = cv2.VideoCapture(videos[0])
    cap.set(1, 1)
    ret, frame = cap.read()
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    video = cv2.VideoWriter('oriVideo.avi', fourcc, 29.97, (width, height))
    for iseq in StartToEnd:
        startF = iseq[0]
        endF = iseq[1]
        curF = startF
        while curF <= endF :
            cap.set(1, curF)
            ret, frame = cap.read()
            video.write(frame)
            curF += 1

        # cv2.destoryAllWindows()
    video.release()

    seq, count = GetResult(filename)


    foutput = open('TRCresult.txt', 'w')

    for iseq in seq :
        trueFrame = round((iseq[1] / 29.97 + delayTime[0]) * 120)
        foutput.write('%s' %(trueFrame))
        foutput.write('\n')


    foutput.close()
if __name__ == '__main__' :
    main()

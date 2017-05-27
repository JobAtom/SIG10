import re
import cv2


def GetResult(filename):
    list = []
    fid = open(filename, 'r')
    for line in fid :
        items = re.split('\s+', line)
        temp = []
        for item in items :
            if item == '':
                continue
            temp.append(int(item))
        list.append(temp)
    return list

def main():
    print('hello')
    videos = [r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial001.mp4', r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial002.mp4',r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial003.mp4',r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial004.mp4',r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial005.mp4',r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial006.mp4',r'c:\Users\CGML\Desktop\videodata\TwoPartyJonathanTrial007.mp4']
    filename = 'finalResult.txt'
    seq = GetResult(filename)
    cap = cv2.VideoCapture(videos[0])
    cap.set(1,1)
    ret, frame = cap.read()
    height , width , layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    video = cv2.VideoWriter('video2.avi', fourcc, 29.97, (width, height))

    for iseq in seq :
        cap.set(1, iseq[1])
        ret, frame = cap.read()
        video.write(frame)

   # cv2.destoryAllWindows()
    video.release()




if __name__=='__main__':
    main()

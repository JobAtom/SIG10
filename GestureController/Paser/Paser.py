import io
import re
import numpy as np
import math

class TexPas:
    def __init__(self, name, delaytime):
        self.name = name #name of actor
        self.time = [] #duration of speaking
        self.text = [] #speaking text
        self.TrcData = [] #Trcdata
        self.finalResult = [] #final data we want for training
        self.delay = delaytime #delaytime of video to Trc file

    def openTexfile(self, filenames):
        for filename in filenames:
            fid = open(filename, "r")
            min_num = 0
            max_num = 0
            findmin = False
            findmax = False
            findname = False
            for line in fid:
                #name of actor we want to get
                S_name = re.search(r' name ', line)
                if S_name:
                    name = re.search('= \"(\S+)\" ', line)
                    if name.group(1) == self.name:
                        findname = True
                if findname:
                    if re.search(r' xmin (\S+) ', line):
                        min = re.search(r'\d+(.\d+)*', line)
                        min_num = float(min.group())
                        findmin = True
                    if re.search(r' xmax (\S+) ', line):
                        max = re.search(r'\d+(.\d+)*', line)
                        max_num = float(max.group())
                        findmax = True
                    word = re.search('text', line)
                    if word:
                        words = re.search('= \"(.*)\"', line)
                        self.text.append(words.group(1))
                    if (findmin and findmax):
                        self.time.append((min_num, max_num))
                        findmin = False
                        findmax = False
            fid.close()
        return
    #read Trc file and get hands wrist and hands palm data.
    def openTrcfile(self, filenames):
        start = False
        for filename in filenames:
            fid = open(filename, 'r')
            for line in fid:
                temp = re.split('\s+', line)
                if temp[0] == '1':
                    start = True
                if start:
                    d1 = []
                    #frame id
                    d1.append(float(temp[0]))
                    #left hand wrist
                    d1.append([float(temp[80]), float(temp[81]), float(temp[82])])
                    #left hand palm
                    d1.append([float(temp[83]), float(temp[84]), float(temp[85])])
                    #right hand wrist
                    d1.append([float(temp[128]), float(temp[129]), float(temp[130])])
                    #right hand palm
                    d1.append([float(temp[131]), float(temp[132]), float(temp[133])])
                    if len(self.TrcData) > 0:
                        p1 = self.TrcData[-1]
                        delt = (d1[0] - p1[0]) / 120.0
                        #mean velocity of two hands for wrist in vector
                        d1.append((((np.array(d1[1]) - np.array(p1[1])) + (np.array(d1[3]) - np.array(p1[3]))) / (
                            2.0 * delt)).tolist())
                        #mean velocity of two hands for palm in vector
                        d1.append((((np.array(d1[2]) - np.array(p1[2])) + (np.array(d1[4]) - np.array(p1[4]))) / (
                            2.0 * delt)).tolist())
                        #mean acceleration of two hands for wrist in vector
                        d1.append(((np.array(d1[5]) - np.array(p1[5])) / delt).tolist())
                        #mean acceleration of two hands for palm in vector
                        d1.append(((np.array(d1[6]) - np.array(p1[6])) / delt).tolist())
                        #cross product of velocity and acceleration for wrist
                        d1.append(np.cross(d1[5], d1[7]).tolist())
                        #cross product of velocity and acceleration for palm
                        d1.append(np.cross(d1[6], d1[8]).tolist())

                    else:
                        d1.append(0.0)
                        d1.append(0.0)
                        d1.append(0.0)
                        d1.append(0.0)
                        d1.append(0.0)
                        d1.append(0.0)
                    print(d1)
                    self.TrcData.append(d1)
        fid.close()
        return
    #get the final result that do not have text free part.
    def getFinal(self):
        if len(self.time) == 0 or len(self.TrcData) == 0:
            print('please do openTexfile and openTrcfile first')
            return
        id = 0
        for data in self.time:
            if id > len(self.text):
                break
            if id == 0:
                id += 1
                continue
            if self.text[id - 1] == '':
                id += 1
                continue
            startF = data[0]
            endF = data[1]
            #convert to TRC 120 frames/second
            startF = round((startF + self.delay) * 120)
            endF = round((endF + self.delay) * 120)

            countF = startF
            results = []
            dataF = []
            dur = [startF, endF]
            textinf = self.text[id - 1]
            results.append(dur)
            results.append(textinf)
            while countF <= endF:
                #tF = round((countF / 29.97 + self.delay) * 120)
                tF = countF
                if tF >= len(self.TrcData):
                    return
                dataF.append(self.TrcData[tF])
                countF += 1
            results.append(dataF)
            self.finalResult.append(results)
            id += 1
        return



#y = TexPas('Shenae', 0)
#y.openTexfile(Texfilenames)


def main():

    x = TexPas('Michelle', 0.01)
    Texfilenames = ['C:/Users/CGML/Desktop/WorkSpace/sound/Day1-Michelle-Shenae-Trial001-Audio.TextGrid']
    Trcfilenames = [
        'C:/Users/CGML/Desktop/WorkSpace/twopartytrc/Day1-Michelle-Shenae-Trial001-Mocap-withfingers-Michelle.trc']
    if len(Texfilenames) != len(Trcfilenames) :
        print(' Text file number should equal to Trc file number')
        return

    x.openTexfile(Texfilenames)
    x.openTrcfile(Trcfilenames)
    x.getFinal()

    wfile = open('result.txt', 'w')
    for item in x.finalResult:
        wfile.write("%s\n" % item)
    wfile.close()

    #total sentences with segmentation information
    total_slides = []
    # define threshold for hand velocity
    VT = 90
    # output segmentation time to file
    wfile = open('SegTime.txt', 'w')

    for items in x.finalResult:
        startF = items[0][0]
        endF = items[0][1]
        wfile.write('%s ' % startF)
        wfile.write('%s ' % endF)
        # segmentation information for one sentence
        time_slides = []
        time_slides.append(startF)
        time_slides.append(endF)
        id = 0
        pv = 0
        lastId = 0
        for item in items[2]:
            vl = item[5]
            vc = math.sqrt(vl[0] * vl[0] + vl[1] * vl[1] + vl[2] * vl[2])
            if id == 0:
                pv = vc
                id += 1
                continue
            if (pv - VT) * (vc - VT) < 0:
                wfile.write('%s ' % (startF + id))
                time_slides.append(startF + id)
            id += 1
            pv = vc
        wfile.write('\n')
        total_slides.append(time_slides)

    wfile.close()

    ffile = open('trainData.txt', 'w')

#write final features to text
    countRe = 0
    for data in total_slides :
        startF = data[0]
        endF = data[1]
        sortdata = sorted(data)
        senData = x.finalResult[countRe]
        #set weights for every feature: wt, wd, wv, wa, wc, wh, bt, bd, bv, ba, bc, bh
        wt = 1
        wd = 1
        wv = 1
        wa = 1
        wc = 1
        wh = 1
        bt = 100
        bd = 10
        bv = 1
        ba = 1
        bc = 1
        bh = 1
        #print(data)
        firstF = 0
        secondF = 1
        while secondF < len(sortdata):
           # print(sortdata[secondF]- sortdata[firstF])
            if sortdata[secondF] - sortdata[firstF] == 0:
                secondF += 1
                continue
            T_av = wt * math.log( bt * (sortdata[secondF] - sortdata[firstF]),10)
            sumD = np.array([0.0,0.0,0.0])
            sumV = np.array([0.0,0.0,0.0])
            sumA = np.array([0.0,0.0,0.0])
            sumC = np.array([0.0,0.0,0.0])
            sumH = 0.0

            for index in range (sortdata[firstF], sortdata[secondF]+1):
                p = index - startF
                item = senData[2][p]
                sitem = senData[2][0]
                #using wrist point
                sumD += np.array(item[1])+ np.array(item[3]) - np.array(sitem[1]) - np.array(sitem[3])
                sumV += np.array(item[5])
                sumA += np.array(item[7])
                sumC += np.array(item[9])
                sumH += item[1][2] + item[3][2]
                #print(senData[1])
            D_av = wd * math.log( np.linalg.norm( bd * sumD / T_av), 10 )
            V_av = wv * math.log( np.linalg.norm( bv * sumV / T_av), 10 )
            A_av = wa * math.log( np.linalg.norm( ba * sumA / T_av), 10 )
            C_av = wc * math.log( np.linalg.norm( bc * sumC / T_av), 10 )
            H_av = wh * math.log( bh * sumH / T_av, 10 )
            firstF = secondF
            secondF += 1
            ffile.write('%s %s %s %s %s %s' %(T_av, D_av, V_av, A_av, C_av, H_av))
            ffile.write('\n')
        countRe += 1
        ffile.write('\n')

    ffile.close()




if __name__ == '__main__':
  main()





# print(x.TrcData[0])
# print(x.TrcData[2])
# print(y.time)
# print(y.text)


# print(x.time)
# print(x.text)

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
                S_name = re.search(r' name =', line)
                if S_name:
                    name = re.search('= \"(\S+)\" ', line)
                    print(name.group(1))
                    if name.group(1) == self.name:
                        findname = True
                    else:
                        findname = False
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
                #print('read trc file...')
                temp = re.split('\s+', line)
                if temp[0] == '1':
                    start = True
                if start:
                    d1 = []
                    #frame id
                    d1.append(float(temp[0]))
                    #left hand wrist
                    d1.append([float(temp[80]), float(temp[81]), float(temp[82])])
                    #left LBWT
                    d1.append([float(temp[10]), float(temp[11]), float(temp[12])])
                    #right hand wrist
                    d1.append([float(temp[128]), float(temp[129]), float(temp[130])])
                    #right RBWT
                    d1.append([float(temp[13]), float(temp[14]), float(temp[15])])
                    if len(self.TrcData) > 0:
                        p1 = self.TrcData[-1]
                        delt = (d1[0] - p1[0]) / 120.0
                        #mean velocity of two hands for wrist in vector
                        vl = np.linalg.norm(np.array(d1[1])-np.array(p1[1]))/delt
                        vr = np.linalg.norm(np.array(d1[3])-np.array(p1[3]))/delt
                        vbl = np.linalg.norm(np.array(d1[2]-np.array(p1[2])))/delt
                        vbr = np.linalg.norm(np.array(d1[4]-np.array(p1[4])))/delt
                        d1.append((vl+vr-vbl - vbr)/2)
                        #d1.append((((np.array(d1[1]) - np.array(p1[1]))-(np.array(d1[2])-np.array(p1[2])) + (np.array(d1[3]) - np.array(p1[3]))-(np.array(d1[4])-np.array(p1[4]))) / (
                         #   2.0 * delt)).tolist())
                        #mean velocity of two hands for palm in vector
                        #d1.append((((np.array(d1[2]) - np.array(p1[2])) + (np.array(d1[4]) - np.array(p1[4]))) / (
                        #    2.0 * delt)).tolist())
                        #mean acceleration of two hands for wrist in vector
                        # d1.append(((np.array(d1[5]) - np.array(p1[5])) / delt).tolist())
                        d1.append((d1[5]-p1[5])/delt)
                        #mean acceleration of two hands for palm in vector
                        #d1.append(((np.array(d1[6]) - np.array(p1[6])) / delt).tolist())
                        #cross product of velocity and acceleration for wrist
                        #d1.append(np.cross(d1[5], d1[6]).tolist())
                        d1.append(d1[5]*d1[6])
                        #cross product of velocity and acceleration for palm
                        #d1.append(np.cross(d1[6], d1[8]).tolist())

                    else:
                        d1.append(0)
                        d1.append(0)
                        d1.append(0)
                    #print(d1)
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

    x = TexPas('Jonathan', 0.13)
    Texfilenames = ['C:/Users/CGML/Desktop/WorkSpace/sound/men/Day2-Jonathan-Stephen-Trial005-Audio.TextGrid']

    #Trcfilenames = [
    #    'C:/Users/CGML/Desktop/WorkSpace/twopartytrc/Day2-Jonathan-Stephen-Trial001-Mocap-withfingers-Jonathan.trc']
    #Trcfilenames = [r'C:/Users/CGML/Desktop/WorkSpace/twopartytrc/Day2-Jonathan-Stephen-Trial002-Mocap-withfingers_Jonathan.trc']
    #Trcfilenames = ['C:/Users/CGML/Desktop/WorkSpace/twopartytrc/Day2-Jonathan-Stephen-Trial003-1-40653-withfingers_Jonathan.trc']
    #Trcfilenames = ['C:/Users/CGML/Desktop/WorkSpace/twopartytrc/Day2-Jonathan-Stephen-Trial004_Mocap_withfingers_Jonathan.trc']
    Trcfilenames = [
        'C:/Users/CGML/Desktop/WorkSpace/twopartytrc/Day2-Jonathan-Stephen-Trial005_1_35777_withfingers_Jonathan.trc']
    #Trcfilenames = [
    #    'C:/Users/CGML/Desktop/WorkSpace/twopartytrc/Day2-Jonathan-Stephen-Trial006-Mocap-withfingers-Jonathan.trc']
    #Trcfilenames = [
    #    'C:/Users/CGML/Desktop/WorkSpace/twopartytrc/Day2-Jonathan-Stephen-Trial007-Mocap-withfingers-Jonathan.trc']

    if len(Texfilenames) != len(Trcfilenames) :
        print(' Text file number should equal to Trc file number')
        return

    x.openTexfile(Texfilenames)
    x.openTrcfile(Trcfilenames)
    x.getFinal()
    #print(x.finalResult)

    wfile = open('result5.txt', 'w')
    for item in x.finalResult:
        wfile.write("%s\n" % item)
    wfile.close()

    #total sentences with segmentation information
    total_slides = []
    # define threshold for hand velocity
    VT = 200
    # output segmentation time to file
    wfile = open('SegTime05.txt', 'w')
    hfile = open('handsSpeed.txt','w')
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
        lid = 0
        pv = 0
        lastId = 0
        for item in items[2]:
            vl = item[5]
            if vl ==0:
                continue
            #print(vl)
            #vc = math.sqrt(vl[0] * vl[0] + vl[1] * vl[1] + vl[2] * vl[2])
            vc = vl
            hfile.write('%s' % (vc))
            hfile.write('\n')
            if id == 0:
                pv = vc
                id += 1
                continue
            if (pv - VT) * (vc - VT) < 0 and (lid== 0 or id - lid > 30):
                wfile.write('%s ' % (startF + id))
                time_slides.append(startF + id)
                lid = id
            id += 1
            pv = vc
        wfile.write('\n')
        total_slides.append(time_slides)

    wfile.close()
    hfile.close()

    ffile = open('trainData05.txt', 'w')

#write final features to text
    countRe = 0
    for data in total_slides :
        startF = data[0]
        endF = data[1]
        sortdata = sorted(data)
        senData = x.finalResult[countRe]
        #set weights for every feature: wt, wd, wv, wa, wc, wh, bt, bd, bv, ba, bc, bh
        wt = 100
        wd = 100
        wv = 200
        wa = 200
        wc = 100
        wh = 200
        bt = 1.1
        bd = 100
        bv = 0.1
        ba = 0.1
        bc = 0.001
        bh = 0.01
        #print(data)
        firstF = 0
        secondF = 1
        while secondF < len(sortdata):
           # print(sortdata[secondF]- sortdata[firstF])
            if sortdata[secondF] - sortdata[firstF] == 0:
                secondF += 1
                continue
            T_av = wt * math.log( bt * (sortdata[secondF] - sortdata[firstF]))
            sumD = np.array([0.0,0.0,0.0])
            sumV = 0.0
            sumA = 0.0
            sumC = 0.0
            #sumV = np.array([0.0,0.0,0.0])
            #sumA = np.array([0.0,0.0,0.0])
            #sumC = np.array([0.0,0.0,0.0])
            sumH = 0.0

            for index in range (sortdata[firstF], sortdata[secondF]+1):
                p = index - startF
                item = senData[2][p]
                sitem = senData[2][0]
                #using wrist point
                #sumD += np.array(item[1])+ np.array(item[3]) - np.array(sitem[1]) - np.array(sitem[3])
                sumD += np.array(item[1])+ np.array(item[3])
                sumV += item[5]
                sumA += item[6]
                sumC += item[7]
                #sumV += np.array(item[5])
                #sumA += np.array(item[6])
                #sumC += np.array(item[7])
                sumH += item[1][2] + item[3][2]
                #print(senData[1])
            D_av = wd * math.log( np.linalg.norm( bd * sumD / T_av - np.array(sitem[1])-np.array(sitem[3])), 10 )
            V_av = wv * math.log(abs(bv* sumV / T_av))
            A_av = wa * math.log(abs(ba* sumA / T_av))
            C_av = wc * math.log(abs(bc* sumC / T_av))
            #V_av = wv * math.log( np.linalg.norm( bv * sumV / T_av), 10 )
            #A_av = wa * math.log( np.linalg.norm( ba * sumA / T_av), 10 )
           # C_av = wc * math.log( np.linalg.norm( bc * sumC / T_av), 10 )
            H_av = wh * math.log( bh * sumH / T_av )
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

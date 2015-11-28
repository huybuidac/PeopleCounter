__author__ = 'pc'
import cv2
import numpy as np

class DetectMoving(object):
    def __init__(self,sizeImg):
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        self.sizeImg = sizeImg
        self.WIDTH_PCONS = 50
        self.HEIGHT_PCONS = 50
        self.near = np.array([[0,0,1,1,1,-1,-1,-1], [1,-1,0,-1,1,0,1,-1]], np.int8)
        self.threshHold = 8

    def compare(self,a, b):
        a = np.int(a)
        b = np.int(b)
        if abs(a-b) <= self.threshHold:
            return 0
        if (b-a) > self.threshHold:
            return 1
        else:
            return -1

    def resize4detect(self,pon1,pon2,pon3,w,h):
        datah = 50 - pon3[1]
        dataw = 60 - pon3[0]
        data11 = data10 = data20 = data21 = 0
        if datah < 0 or dataw < 0:
            if datah < 0:
                datah1 = -datah
                if datah1 % 2 != 0:
                    data11= int(datah1/2)
                    data21 = data11 + 1
                else:
                    data21 =data11 = int(datah1/2)
                if dataw >= 0:
                    if dataw % 2 != 0:
                        data10= int(dataw/2)
                        data20 = data10 + 1
                    else:
                        data20 =data10= int(dataw/2)
                    if pon1[0]-data10 < 0:
                        data20 += (data10 - pon1[0])
                        data10 = pon1[0]
                    if pon2[0]+data20 >= w:
                        data10 += (data20 - (w - pon2[0]))
                        data20 = (w - pon2[0])
                    return (pon1[0]-data10,pon1[1]+data11),(pon2[0]+data20,pon2[1]-data21)
            if dataw < 0:
                dataw1 = -dataw
                if dataw1 % 2 != 0:
                    data10= int(dataw1/2)
                    data20 = data10 + 1
                else:
                    data20 =data10= int(dataw1/2)
                if datah >= 0:
                    if datah % 2 != 0:
                        data11= int(datah/2)
                        data21 = data11 + 1
                    else:
                        data21 =data11 = int(datah/2)
                    if pon1[1]-data11 < 0:
                        data21 += (data11 - pon1[1])
                        data11 = pon1[1]
                    if pon2[1]+data21 >= h:
                        data11 += (data21 - (h - pon2[1]))
                        data21 = (h - pon2[1])
                    return (pon1[0]+data10,pon1[1]-data11),(pon2[0]-data20,pon2[1]+data21)
            return (pon1[0]+data10,pon1[1]+data11),(pon2[0]-data20,pon2[1]-data21)
        if datah % 2 != 0:
            data11= int(datah/2)
            data21 = data11 + 1
        else:
            data21 =data11 = int(datah/2)
        if dataw % 2 != 0:
            data10= int(dataw/2)
            data20 = data10 + 1
        else:
            data20 =data10= int(dataw/2)

        if pon1[0]-data10 < 0:
            data20 += (data10 - pon1[0])
            data10 = pon1[0]
        if pon1[1]-data11 < 0:
            data21 += (data11 - pon1[1])
            data11 = pon1[1]
        # print pon1,pon2
        if pon2[0]+data20 >= w:
            data10 += (data20 - (w - pon2[0]))
            data20 = (w - pon2[0])
        if pon2[1]+data21 >= h:
            data11 += (data21 - (h - pon2[1]))
            data21 = (h - pon2[1])
        return (pon1[0]-data10,pon1[1]-data11),(pon2[0]+data20,pon2[1]+data21)

    def CheckRectDetect(self,pon1,pon2,pon3,w,h):
        datah = self.sizeImg - pon3[1]
        dataw = self.sizeImg - pon3[0]
        if datah % 2 != 0:
            data11= int(datah/2)
            data21 = data11 + 1
        else:
            data21 =data11 = int(datah/2)
        if dataw % 2 != 0:
            data10= int(dataw/2)
            data20 = data10 + 1
        else:
            data20 =data10= int(dataw/2)

        if pon1[0]-data10 < 0:
            data20 += (data10 - pon1[0])
            data10 = pon1[0]
        if pon1[1]-data11 < 0:
            data21 += (data11 - pon1[1])
            data11 = pon1[1]
        # print pon1,pon2
        if pon2[0]+data20 >= w:
            data10 += (data20 - (w - pon2[0]))
            data20 = (w - pon2[0])
        if pon2[1]+data21 >= h:
            data11 += (data21 - (h - pon2[1]))
            data21 = (h - pon2[1])
        return (pon1[0]-data10,pon1[1]-data11),(pon2[0]+data20,pon2[1]+data21)


    def locRec(seft,pon1,pon2):
        if pon2[1] - pon1[1] < seft.WIDTH_PCONS or pon2[0] - pon1[0] < seft.WIDTH_PCONS:
            return False
        else:
            return True
    # def detectObjectInImage(self,image):
    #     # h,w = image.shape
    #     opening = cv2.morphologyEx(image.copy(),cv2.MORPH_OPEN,self.kernel, iterations = 3)
    #     re,thresh1 = cv2.threshold(opening,75,255,cv2.THRESH_BINARY)
    #     contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #     PosObj = []
    #     # PosObj150 = []
    #     for cn in contours:
    #         ver = cv2.boundingRect(cn)
    #         if cv2.contourArea(cn) > 500:
    #             maiorArea = cv2.contourArea(cn)
    #             rect = ver
    #             # print rect
    #             ponto1 = (rect[0], rect[1])
    #             ponto2 = (rect[0]+ rect[2],rect[1]+rect[3])
    #             ponto3 = (rect[2],rect[3])
    #             # self.CheckRectDetect(ponto1,ponto2,ponto3,w,h)
    #             # PosObj.append((self.CheckRectDetect(ponto1,ponto2,ponto3,w,h)))
    #             if self.locRec(ponto1,ponto2):
    #                 PosObj.append((ponto1,ponto2,ponto3))
    #                 # PosObj150.append((self.CheckRectDetect(ponto1,ponto2,ponto3,w,h)))
    #     return  PosObj

    def detectObjectInImage(self,img):
        h,w = img.shape
        image = img.copy()
        image = cv2.medianBlur(image, 31)
        image = cv2.resize(image, (image.shape[1]/20, image.shape[0]/20))
        height, width = image.shape[:2]
        output = np.ones(image.shape[:2], dtype=int) * (np.nan)
        output[0,0] = 0
        for y in range(height):
            for x in range(width):
                # print "--------------"
                for t in range(8):
                    x_next = x + self.near[0,t]
                    y_next = y + self.near[1,t]
                    if x_next < 0 or y_next < 0 or x_next==width or y_next==height:
                        continue
                    # print t

                    if self.compare(image[y,x], image[y_next, x_next]) == 0:
                        output[y_next, x_next] = output[y,x]

                    elif self.compare(image[y,x], image[y_next, x_next]) == 1:
                        if np.isnan(output[y_next, x_next]):
                            output[y_next, x_next] = output[y,x] + 1
                            continue
                        if abs(output[y_next, x_next] - output[y,x]) < 2:
                            output[y_next, x_next] = output[y,x] + 1
                            # print output[y_next, x_next]


                    elif self.compare(image[y,x], image[y_next, x_next]) == -1:
                        if np.isnan(output[y_next, x_next]):
                            output[y_next, x_next] = output[y,x] -1
                            if(output[y_next, x_next]< 0):
                                output[y_next, x_next] = 0
                            continue
                        if abs(output[y_next, x_next] - output[y,x]) < 2 and output[y,x] > 0:
                            output[y_next, x_next] = output[y,x] - 1
                            # print output[y_next, x_next]
                            if(output[y_next, x_next] == -1):
                                pass
                            # if(output[y_next, x_next]< 0):
                            #     output[y_next, x_next] = 0

                    # print "[" + str(y) + "," + str(x) + "] "+ str(image[y,x]) + "  : " + str(y_next) + "," + str(x_next) + " : " +str(image[y,x]) +" | "+ str(output[y_next, x_next])
        output = np.uint8(output)
        PosObj = []
        PosObj150 = []

        # threshValue = output.max()-3
        # if threshValue <1:
        #     threshValue = 1

        (T, output) = cv2.threshold(output, 1, 255, cv2.THRESH_BINARY)
        # output = cv2.medianBlur(output, 3)

        contours, hierarchy = cv2.findContours(output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for cn in contours:
            print "size contour: " + str(cv2.contourArea(cn))
            if cv2.contourArea(cn) > 30:
                print "sss"

                (dist_transform, label) = cv2.distanceTransformWithLabels(output,cv2.cv.CV_DIST_L2,3)
                ret, sure_fg = cv2.threshold(dist_transform,0.5*dist_transform.max(),255,0)

                output = sure_fg
                output = np.uint8(output)
                output = cv2.resize(output, (output.shape[1] * 2, output.shape[0] * 2))
                (T, output) = cv2.threshold(output,1, 255, cv2.THRESH_BINARY)
                output = cv2.medianBlur(output,3)
                output = cv2.resize(output, (output.shape[1] / 2, output.shape[0] / 2))
                (T, output) = cv2.threshold(output,128, 255, cv2.THRESH_BINARY)
                print output

        contours, hierarchy = cv2.findContours(output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cn in contours:
            ver = cv2.boundingRect(cn)
            if cv2.contourArea(cn) > 1:
                maiorArea = cv2.contourArea(cn)
                rect = ver
                # print rect
                ponto1 = (rect[0]*20, rect[1]*20)
                ponto2 = ((rect[0]+ rect[2])*20,(rect[1]+rect[3])*20)
                ponto3 = (ponto2[0]-ponto1[0],ponto2[1]-ponto1[1])

                if ponto3[0] <= 150 :
                    # cv2.rectangle(imagex, ponto1, ponto2,(255,255,255), 2)
                    # data1,data2 = CheckRectDetect(ponto1,ponto2,ponto3,352,288)
                    # cv2.rectangle(imagex, data1, data2,(255,255,255), 1)
                # if ponto3[0] > self.sizeImg*2:
                #     pontow = ponto3[0]/2
                #     ponton11 = (ponto1[0], ponto1[1])
                #     ponton12 = (ponton11[0]+pontow,ponto2[1])
                #     ponton13 = (pontow,ponto3[1])
                #     datax,datay = self.resize4detect(ponton11,ponton12,ponton13,w,h)
                #     PosObj.append((datax,datay,(datay[0]-datax[0],datay[1]-datax[1])))
                #     ponton11 = (ponton12[0], ponto1[1])
                #     ponton12 = (ponton11[0]+pontow,ponto2[1])
                #     ponton13 = (pontow,ponto3[1])
                #     datax,datay = self.resize4detect(ponton11,ponton12,ponton13,w,h)
                #     PosObj.append((datax,datay,(datay[0]-datax[0],datay[1]-datax[1])))
                # # elif ponto3[1] > self.sizeImg and ponto3[0] < self.sizeImg*2:
                # #     pontoh = ponto3[1]/2
                # #     ponton11 = (ponto1[0], ponto1[1])
                # #     ponton12 = (ponto2[0],ponton11[1]+pontoh)
                # #     ponton13 = (ponto3[0],pontoh)
                # #     datax,datay = self.resize4detect(ponton11,ponton12,ponton13,w,h)
                # #     PosObj.append((datax,datay,(datay[0]-datax[0],datay[1]-datax[1])))
                # #     ponton11 = (ponto1[0], ponton12[1])
                # #     ponton12 = (ponto2[0],ponton11[1]+pontoh)
                # #     ponton13 = (ponto3[0],pontoh)
                # #     datax,datay = self.resize4detect(ponton11,ponton12,ponton13,w,h)
                # #     PosObj.append((datax,datay,(datay[0]-datax[0],datay[1]-datax[1])))
                # else:
                # cv2.rectangle(imagex, ponto1, ponto2,(255,255,255), 2)
                # data1,data2 = CheckRectDetect(ponto1,ponto2,ponto3,352,288)
                # cv2.rectangle(imagex, data1, data2,(255,255,255), 1)
                    datax,datay = self.resize4detect(ponto1,ponto2,ponto3,w,h)
                    PosObj.append((datax,datay,(datay[0]-datax[0],datay[1]-datax[1])))
                    PosObj150.append((self.CheckRectDetect(ponto1,ponto2,ponto3,w,h)))
        return  PosObj, PosObj150
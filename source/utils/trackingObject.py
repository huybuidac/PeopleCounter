from source.utils import const

__author__ = 'pc'
import cv2
import numpy as np

class TrackingObj(object):
    def __init__(self, queue_update_pc, queue_post2web):
        self.allObj = []
        self.InSh = 0
        self.OutSh = 0
        self.maxPass = 10
        self.queue_update_pc = queue_update_pc
        self.queue_post2web = queue_post2web
        self.topPosition = 144-70
        self.midPosition = 144
        self.botPosition = 144+70


    def resetTracking(self):
        for data in self.allObj:
            data[3] = False
        return None

    def remove_track(self):
        for data in self.allObj:
            if data[3] == False:
                if data[5] < self.maxPass:
                    data[5] += 1
                else:
                    self.allObj.remove(data)
                    # data[0] = None
                    # data[1] = None
                    # data[2] = None
                    # data[3] = None
                    # data[5] = 0
                    # data[6] = 0
        return None

    def check_in_out(self,data,ln):
        #0: out
        #1: in
        #-1: unknow
        if data[4] > 0 and ln != data[6] and ln!=None:
            data[6] = ln
            data[4] = 0
            if ln == 0:
                return 1
            else:
                return 0
        else:
            return -1

    def sysn_line(self,data,y,h):
        ln = self.check_withLine(y,h)
        if ln == 1:
            data[4] = ln
            return False,ln
        else:
            if data[4] == 0 and ln != data[6] and ln != None:
                data[6] = ln
            return True,ln


    def check_withLine(self,y,h):
        if y <= self.topPosition <= y+h:
            return 0

        elif y <= self.botPosition <= y+h:
            return 2

        elif self.topPosition < y and self.botPosition > y+h:
            return 1


    # def trackingObj(self,pon1,pon2):
    #     y, x = [pon1[1],pon1[0]]
    #     h, w = [pon2[1],pon2[0]]
    #     # print x,y,w,h
    #     if len(self.allObj) == 0:
    #         self.allObj.append([x,y,w,h,True,0,0,None])
    #         return None
    #     haveline = False
    #
    #     for data in self.allObj:
    #         if data[0] != None:
    #             if (data[1] <= y <= data[1]+data[3] and x <= data[0] <= x + w) or (x<=data[0]<=x+w and y <= data[1]<=y+h)or (data[0] <= x <= data[0] + data[2] and y<=data[1]<=y+h) or (data[0] <= x <= data[0]+data[2] and data[1]<=y<=data[1]+data[3]):
    #                 # Point1 = ((data[0]+data[2])/2,(data[1]+data[3])/2)
    #                 data[0] = x
    #                 data[1] = y
    #                 data[2] = w
    #                 data[3] = h
    #                 data[4] = True
    #                 res, ln = self.sysn_line(data,y,h)
    #                 if res:
    #                     inout = self.check_in_out(data,ln)
    #
    #                     if inout == 0:
    #                         self.OutSh +=1
    #                         self.queue_update_pc.put(const.TYPE_OUT)
    #                         self.queue_post2web.put(const.TYPE_OUT)
    #                     elif inout == 1:
    #                         self.InSh +=1
    #                         self.queue_update_pc.put(const.TYPE_IN)
    #                         self.queue_post2web.put(const.TYPE_IN)
    #                 haveline = True
    #                 break
    #     if haveline == False:
    #         try:
    #             ins = self.allObj.index([None,None,None,None,False,0,0,None])
    #             self.allObj.insert(ins,[x,y,w,h,True,0,0,None])
    #             self.allObj.remove(self.allObj[ins+1])
    #         except Exception as e:
    #             self.allObj.append([x,y,w,h,True,0,0,None])
    #     return None

    def trackingObj(self,pon1,pon2,rad):
        y, x = [pon1[1] +pon2[1]/2,pon1[0] + pon2[0]/2]
        # print x,y,w,h
        if len(self.allObj) == 0:
            self.allObj.append([x,y,rad,True,0,0,None])
            return None
        haveline = False

        for data in self.allObj:
            if data[0] != None:
                if (abs(x-data[0])<rad*2 and abs(y-data[1])<rad*2):
                    # Point1 = ((data[0]+data[2])/2,(data[1]+data[3])/2)
                    data[0] = x
                    data[1] = y
                    data[2] = rad
                    data[3] = True
                    res, ln = self.sysn_line(data,y,rad)
                    if res:
                        inout = self.check_in_out(data,ln)

                        if inout == 0:
                            self.OutSh +=1
                            self.queue_update_pc.put(const.TYPE_OUT)
                            self.queue_post2web.put(const.TYPE_OUT)
                        elif inout == 1:
                            self.InSh +=1
                            self.queue_update_pc.put(const.TYPE_IN)
                            self.queue_post2web.put(const.TYPE_IN)
                    haveline = True
                    break
        if haveline == False:
            try:
                ins = self.allObj.index([None,None,None,False,0,0,None])
                self.allObj.insert(ins,[x,y,rad,True,0,0,None])
                self.allObj.remove(self.allObj[ins+1])
            except Exception as e:
                self.allObj.append([x,y,rad,True,0,0,None])
        return None


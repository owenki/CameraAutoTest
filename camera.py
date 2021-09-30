# coding=utf-8
import xlrd
#import os
import cv2
import numpy as np
import time
import keyboard


lower_blue=np.array([78,43,46])
upper_blue=np.array([110,255,255])
lower_dark=np.array([0,0,0])
upper_dark=np.array([128,128,128])

#os.system("chcp 936")  
#os.system("setx OPENCV_VIDEOIO_PRIORITY_MSMF 0")  
xunHuanCiShu=1

while(xunHuanCiShu):
    area=0
    area2=0
    zero=0
    rate=0.0
    height=0
    width=0

    
    #结果文件保存
    starttime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    f=open(starttime+'result.txt','a')
    print(starttime+'开始抽测')
    configFile='1.xlsx'
    book=xlrd.open_workbook(configFile)
    sheet1=book.sheets()[0]
    nrows=sheet1.nrows
    for i in range(nrows):

        area=0
        area2=0
        zero=0
        rate=0.0
        height=0
        width=0

        rtspStr = "rtsp://"
        rtspStr = rtspStr+str(sheet1.cell(i,3).value)+":"+str(sheet1.cell(i,4).value)+"@"+str(sheet1.cell(i,1).value)+":554/cam/realmonitor?channel="+str(int(sheet1.cell(i,2).value))+"&subtype=0"
        #print(rtspStr)
        changJia=sheet1.cell(i,0).value
        sheXiangJiName=sheet1.cell(i,5).value
        yunTai=sheet1.cell(i,6).value
        neiWai=sheet1.cell(i,7).value
        #cap = cv2.VideoCapture(rtspStr)
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        rtspStr = rtspStr.strip("rtsp://")
        rtspStr = rtspStr.strip(sheet1.cell(i,3).value)
        rtspStr = rtspStr.strip(":")
        rtspStr = rtspStr.strip(sheet1.cell(i,4).value)
        rtspStr = rtspStr.strip("@")
        rtspStr = rtspStr.replace(":554/cam/realmonitor?channel=","  通道  ")
        rtspStr = rtspStr.strip("&subtype=0")
        rtspStr = rtspStr+"\t"+sheXiangJiName+"\t"
        print(rtspStr)
        f.write(rtspStr)
        ret, frame = cap.read()
        if ret :
            #cv2.imwrite(time.strftime('%Y%m%d%H%M%S-2',time.localtime(time.time()))+'.png',frame)
            #cv2.imshow("capture", frame)# change to hsv model
            #time.sleep(10)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #cv2.imshow("hsv", hsv)# change to hsv model


            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            #cv2.imshow('Mask', mask)
            ret,thresh1 = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
            #time.sleep(5)
            mask2 = cv2.inRange(hsv, lower_dark, upper_dark)
            #cv2.imshow('Mask2', mask2)
            ret2,thresh2 = cv2.threshold(mask2,127,255,cv2.THRESH_BINARY)


            height,width = thresh1.shape

            #res = cv2.bitwise_and(frame, frame, mask=mask)
            #cv2.imshow('res', res)


            for i in range(height):
                for j in range(width):
                    if(thresh1[i,j] == 255) :
                        area += 1
                    if(thresh2[i,j] == 0) :
                        area2 += 1
            #print(area)
            #print(area2)
            rate=area / (height*width)
            rate2=area2 / (height*width)
            #print(height*width)
            #cv2.imwrite(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.png',frame)
            if rate > 0.95 :
                print("蓝屏确认")
                f.write("蓝屏，请检查行为分析仪器至相机线缆连接情况\n")
                #cv2.imwrite(time.strftimtime(time.time()))+'.png',thresh1)
                cv2.imwrite(time.strftime(rtspStr+'-BLUE-%Y%m%d%H%M%S',time.localtime(time.time()))+'.png',frame)
                
            elif rate2 > 0.95 :
                print("黑屏确认")
                f.write("黑屏，请检查相机至编码器线缆连接状态\n")
                #cv2.imwrite(time.strftime(rtspStr+'dark%Y%m%d%H%M%S-2',time.localtime(time.time()))+'.png',thresh2)
                cv2.imwrite(time.strftime(rtspStr+'-BLACK-%Y%m%d%H%M%S',time.localtime(time.time()))+'.png',frame)
                
            else :
                print("视频正常")
                f.write("视频正常\n")
            #print(rate,"%")
            #print(rate2,"%")
            
        else :
            print("无视频流")
            
        
        #cv2.imwrite(time.strftime('%Y%m%d%H%M%S-2',time.localtime(time.time()))+'.png',frame)
        del frame
        del hsv
        del mask
        del mask2
        del thresh1
        del thresh2
        cap.release()
        cv2.destroyAllWindows()
        rtspStr=""
        #print(rtspStr)
    endtime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

    print(endtime+'抽测完成')
    
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        print('任务完成!')
        break  # finishing the loop
    else:
        print('结果输出中请稍后...')
        time.sleep(3)
        print('请查看结果\n\n')
        time.sleep(2)
        pass
    xunHuanCiShu=xunHuanCiShu-1
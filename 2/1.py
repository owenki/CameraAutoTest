# encoding:utf-8

import cv2
import numpy as np
import time
import keyboard
import os


#os.system("chcp 936")  
#os.system("setx OPENCV_VIDEOIO_PRIORITY_MSMF 0")  
zero=1
while(zero):
    zero=0
    #结果文件保存
    starttime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    f=open(starttime+'result.txt','a')
    print(starttime+'开始抽测')
    file= open("./config.txt")
    for line in open("./config.txt"):
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            break  # finishing the loop
        else:
            pass
        line = line.strip('\n')
        #print(line)
        #line=int(line)
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #cap = cv2.VideoCapture(line)
        line = line.strip("rtsp://crsc:crsc@")
        line = line.replace(":554/cam/realmonitor?channel=","  通道  ")
        line = line.strip("&subtype=0")
        print(line)
        f.write(line+"\n")
        line = line.replace(" 通道 ","-channel-")
        ret, frame = cap.read()
        if ret :
            cv2.imwrite(time.strftime('%Y%m%d%H%M%S-2',time.localtime(time.time()))+line+'.png',frame)
            #cv2.imshow("capture", frame)# change to hsv model
        #cv2.imwrite(time.strftime('%Y%m%d%H%M%S-2',time.localtime(time.time()))+'.png',frame)
        del frame
        cap.release()
        cv2.destroyAllWindows()
        line=""
        #print(line)
    endtime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    print(endtime+'抽测完成')
    print('结果输出中请稍后...')
    print('请查看结果\n\n')

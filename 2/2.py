# encoding:utf-8

import cv2
import numpy as np
import time
import keyboard
import os

lower_blue=np.array([78,43,46])
upper_blue=np.array([110,255,255])
lower_dark=np.array([0,0,0])
upper_dark=np.array([128,128,128])

#os.system("chcp 936")  
#os.system("setx OPENCV_VIDEOIO_PRIORITY_MSMF 0")  

while(1):
    area=0
    area2=0
    zero=0
    rate=0.0
    height=0
    width=0
    i=0
    j=0 
    
    #结果文件保存
    starttime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    f=open(starttime+'result.txt','a')
    print(starttime+'开始抽测')
    file= open("./config.txt")
    
    
    for line in open("./config.txt"):
        area=0
        area2=0
        zero=0
        rate=0.0
        height=0
        width=0
        i=0
        j=0 
        line = line.strip('\n')
        #print(line)
        #line=int(line)
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #cap = cv2.VideoCapture(line)
        line = line.strip("rtsp://crsc:crsc@")
        line = line.replace(":554/cam/realmonitor?channel=","  通道  ")
        line = line.strip("&subtype=0")
        print(line)
        f.write(line)
        line = line.replace(" 通道 ","-channel-")
        ret, frame = cap.read()
        #while(1):
            #ret, frame = cap.read()
            #cv2.imshow("1",frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break
        if ret :
            cv2.imwrite(time.strftime('%Y%m%d%H%M%S-2',time.localtime(time.time()))+'.png',frame)
            #cv2.imshow("capture", frame)# change to hsv model
            #time.sleep(10)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #cv2.imshow("hsv", hsv)# change to hsv model


            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            #cv2.imshow('Mask', mask)
            ret,thresh1 = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)

            mask2 = cv2.inRange(hsv, lower_dark, upper_dark)
            #cv2.imshow('Mask2', mask2)
            ret,thresh2 = cv2.threshold(mask2,127,255,cv2.THRESH_BINARY)


            height,width = thresh1.shape

            #res = cv2.bitwise_and(frame, frame, mask=mask)
            #cv2.imshow('res', res)


            for i in range(height):
                for j in range(width):
                    if(thresh1[i,j] == 255) :
                        area += 1
                    if(thresh2[i,j] == 255) :
                        area2 += 1
            rate=area / (height*width)
            rate2=area2 / (height*width)
            #print(rate)
            #print(rate2)
            #cv2.imwrite(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.png',frame)
            if rate > 0.95 :
                print("蓝屏确认")
                f.write("蓝屏，请检查行为分析仪器至相机线缆连接情况\n")
                #cv2.imwrite(time.strftimtime(time.time()))+'.png',thresh1)
                cv2.imwrite(time.strftime(line+'-BLUE-%Y%m%d%H%M%S',time.localtime(time.time()))+'.png',frame)
                
            elif rate2 > 0.95 :
                print("黑屏确认")
                f.write("黑屏，请检查相机至编码器线缆连接状态\n")
                #cv2.imwrite(time.strftime(line+'dark%Y%m%d%H%M%S-2',time.localtime(time.time()))+'.png',thresh2)
                cv2.imwrite(time.strftime(line+'-BLACK-%Y%m%d%H%M%S',time.localtime(time.time()))+'.png',frame)
                
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
        line=""
        #print(line)
    endtime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

    print(endtime+'抽测完成')
    
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        print('任务完成!')
        break  # finishing the loop
    else:
        print('结果输出中请稍后...')
        time.sleep(1)
        print('请查看结果\n\n')
        time.sleep(2)
        pass

import os
#import mediapipe as mp
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
detector = PoseDetector()
# Define the desired width and height of the output screen
output_width = 1200
output_height = 700

shirtFolderPath = ("Resources/Shirts")
listShirt = os.listdir(shirtFolderPath)
print(listShirt)
fixedRatio =262/190
shirtRatioHeightWidth = 581/440
imageNumber=0
imgButtonRight= cv2.imread("Resources/button.png",cv2.IMREAD_UNCHANGED)
imgButtonLeft= cv2.flip(imgButtonRight,1)
counterRight=0
counterLeft=0
selectionSpeed=10


while True:
    success, img = cap.read()
    img = detector.findPose(img)
    #img = cv2.flip(img,1)
    scale_percent = 60  # percent of original size
    width = int(imgButtonRight.shape[1] * scale_percent / 100)
    height = int(imgButtonRight.shape[0] * scale_percent / 100)

    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False,draw=False)
    if lmList:
        #center = bboxInfo["center"]
        lm11= lmList[11][1:3]
        lm12 = lmList[12][1:3]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath,listShirt[imageNumber]),cv2.IMREAD_UNCHANGED)


        widthOfShirt = int((lm11[0]-lm12[0])*fixedRatio)
        print(widthOfShirt)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt*shirtRatioHeightWidth)), None, 0.5, 0.5)
        currentScale= (lm11[0]-lm12[0])/190
        offset = int(44*currentScale),int(48*currentScale)
        try:
            img = cvzone.overlayPNG(img,imgShirt,(lm12[0]-offset[0],lm12[0]-offset[1]))
        except:
            pass


        imgButton1 = cv2.resize(imgButtonRight, (width,height), 0.5,0.5)
        imgButton2 = cv2.resize(imgButtonLeft, (width, height), 0.5, 0.5)
        img = cvzone.overlayPNG(img, imgButton1, (500, 200))
        img = cvzone.overlayPNG(img, imgButton2, (70, 200))

        if lmList[16][1]<150:
            counterRight +=1
            cv2.ellipse(img,(107,237),(30,30),0,0,
                        counterRight*selectionSpeed,(0,255,0),10)
            if counterRight*selectionSpeed>360:
                counterRight=0
                if imageNumber< len(listShirt)-1:
                    imageNumber+=1

        elif lmList[15][1]>450:
            counterLeft += 1
            cv2.ellipse(img, (537, 237), (30, 30), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 10)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1

        else:
            counterRight=0
            counterLeft=0

    img = cv2.resize(img, (output_width, output_height))
    cv2.imshow("Image",img)
    cv2.waitKey(1)
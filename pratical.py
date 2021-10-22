#  import the libraries
import cv2
import cvzone
import csv
import time
from cvzone.HandTrackingModule import HandDetector

# take the image from the camera
cap = cv2.VideoCapture(0)
cap.set(3, 1288)
cap.set(4, 720)

# hand detection module import in detector
detector = HandDetector(detectionCon=0.8)


# 333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333


class MCQ:
    def __init__(self, data):
        self.Question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), cv2.FILLED)
                return x + 1
        return 0


# 22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222


# import csv file data
pathCSV = "MCQS.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]
print(dataAll)

# create the object of each MCQ
mcqList = []
for q in dataAll:
    mcqList.append(MCQ(q))

print("Total mCQ Objects Created : ", len(mcqList))

qNo = 0
qTotal = len(dataAll)
userAns = 0



# 33333333333333333333333333333333333333333333333333333333333333333333333333333333

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    cv2.putText(img,"'Virtual Reality (VR) Quiz'", (200,50), cv2.FONT_HERSHEY_DUPLEX, 2, 255)
    
    mcq = mcqList[0]

    if qNo < qTotal:
        mcq = mcqList[qNo]

        img, bbox = cvzone.putTextRect(img, mcq.Question, [100, 150], 2, 2, colorR=(255,234,0), offset=15, border=1)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [150, 250], 2, 2,colorR=(255,150,90), offset=15, border=1)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [150, 350], 2, 2,colorR=(255,150,90), offset=15, border=1)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [150, 450], 2, 2, colorR=(255,150,90),offset=15, border=1)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [150, 550], 2, 2,colorR=(255,150,90), offset=15, border=1)
        print(qNo)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, info, img = detector.findDistance(lmList[8], lmList[12], img)
            if length < 60:
                if userAns == 0:
                    userAns = mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                    print("user" + str(userAns))

        if userAns > 0:
            if userAns == 1:
                img, selectA = cvzone.putTextRect(img, "Option 'A' is selected", [900, 450], 2, 2, offset=15, border=1)
            if userAns == 2:
                img, selectB = cvzone.putTextRect(img, "Option 'B' is selected", [900, 450], 2, 2, offset=15, border=1)
            if userAns == 3:
                img, selectC = cvzone.putTextRect(img, "Option 'C' is selected", [900, 450], 2, 2, offset=15, border=1)
            if userAns == 4:
                img, selectD = cvzone.putTextRect(img, "Option 'D' is selected", [900, 450], 2, 2, offset=15, border=1)

            img, next1 = cvzone.putTextRect(img, "Next", [1000, 300], 2, 2, offset=15, border=1)
            x1, y1, x2, y2 = next1
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                print("inside")
                time.sleep(0.3)
                qNo = qNo + 1
                userAns = 0

    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score += 1
        score = round((score / qTotal) * 100, 2)
        img, clan = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2,colorR=(255,100,100), offset=15, border=2)
        img, sco = cvzone.putTextRect(img, " Your Score : " + str(score) + "%", [700, 300], 2, 2,colorR=(255,100,100), offset=15, border=2)
        img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [603, 629], 1, 2, offset=15 ,border=1)
        if qNo == qTotal:
            img, exit =cvzone.putTextRect(img,"EXIT " ,[400,500],2,2,colorR=(64,64,255), offset=10,border=1)
            img, retry =cvzone.putTextRect(img,"Retry " ,[700,500],2,2,colorR=(80,80,255),offset=10,border=1)
            if hands:
                    lmList = hands[0]['lmList']
                    cursor = lmList[8]
                    length1, info, img = detector.findDistance(lmList[8], lmList[12], img)
                    if length < 60:
                        x1, y1, x2, y2 = exit
                        if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                            print("cut")
                            break
                    if length < 60:
                        x1, y1, x2, y2 = retry
                        if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                            print("cut")
                            qNo=0

    barValue = 120 + (484 // qTotal) * qNo
    if barValue ==120 :
        barValue=barValue+14
    else:
        barValue = barValue
    cv2.rectangle(img, (120, 604), (barValue, 645), (50,205,50), cv2.FILLED)
    cv2.rectangle(img, (120, 604), (663, 645), (255,255,255), 2)
    # cv2.rectangle(img, (300, 200), (400, 200), (255, 0, 255), 3)
    img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [barValue, 629], 1, 2,(255,255,255),offset=15 ,border=0)
    cv2.putText(img,f'{round((qNo / qTotal) * 100)}%', (barValue+53, 655), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2,150)
    

    cv2.imshow("image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

        # ther we uplode the file


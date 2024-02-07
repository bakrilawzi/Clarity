import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import os
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from UserInterface import UserInterface
user = UserInterface()
# from adjustPictures import adjustPictur
# try:
#     key = os.environ['AZURE_KEY']
#     endpoint = os.environ['AZURE_ENDPOINT']
#     projectid = os.environ['AZURE_PROJECTID']
#     nameIter = os.environ['AZURE_NAME']
# except:
#     print("Please set the environment variables")
#     exit(1)    
# prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-Key": key})
# predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
offset = 20
imgSize = 300
folder = "Data"
counter = 0
count=0
X= False  
Ones_Dict = {}   
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        imgCropShape = imgCrop.shape
        
        aspectRatio = h / w
        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
        # cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("q") or key == ord("Q"):
        break
    if key == ord("s") or key == ord("S"):
         print("dome")
        #  data = {f"one{count}":[x,y,h,w]}
        #  with open("data.txt","a") as f:
        #      json_data = json.dumps(data)
        #      f.write(json_data)
        #  count+=1
        #  image_bytes = cv2.imencode(".jpg",imgWhite)[1].tobytes()
        #  counter += 1
        #  cv2.imwrite(f'{folder}/Image_{   time.time()}.jpg',imgWhite)#write image isnide the folder
        #  print(counter)
        #  results = predictor.detect_image(projectid, nameIter, image_bytes)
         
        #  for prediction in results.predictions:
        #     if prediction.probability>0.2:
        #              print(True)
        #              X = True  
    # if X==True:
    #      cv2.putText(
    #                     img, "stop", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
    #                       )         
cv2.destroyAllWindows()
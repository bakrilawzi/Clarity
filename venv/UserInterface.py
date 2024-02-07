import cv2
import numpy as np
import math
import os
import tkinter as tk
from tkinter import messagebox
from cvzone.HandTrackingModule import HandDetector
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from PIL import Image, ImageTk

class HandRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Recognition App")

        # Open the video source (webcam)
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=1)
        self.offset = 20
        self.imgSize = 300
        self.folder = "Data"
        self.counter = 0
        self.X = False
        self.count = 0

        # Buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_recognition)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_recognition)
        self.capture_button = tk.Button(root, text="Capture & Send", command=self.capture_and_send)

        self.start_button.pack(pady=5)
        self.stop_button.pack(pady=5)
        self.capture_button.pack(pady=5)

        # Canvas to display video feed
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.is_recognizing = False
        self.update()

    def start_recognition(self):
        self.is_recognizing = True

    def stop_recognition(self):
        self.is_recognizing = False

    def capture_and_send(self):
        if self.is_recognizing:
            messagebox.showinfo("Error", "Please stop recognition before capturing.")
            return

        success, img = self.cap.read()
        hands, img = self.detector.findHands(img)
        
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
            imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]
            imgCropShape = imgCrop.shape

            aspectRatio = h / w
            if aspectRatio > 1:
                k = self.imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((self.imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = self.imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((self.imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            cv2.imwrite(f'{self.folder}/Image_{self.count}.jpg', imgWhite)
            self.count += 1
            messagebox.showinfo("Capture & Send", "Image captured and sent to Azure.")

    def update(self):
        if self.is_recognizing:
            success, img = self.cap.read()
            hands, img = self.detector.findHands(img)
            
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
                imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]
                imgCropShape = imgCrop.shape

                aspectRatio = h / w
                if aspectRatio > 1:
                    k = self.imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((self.imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = self.imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((self.imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.root.after(10, self.update)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HandRecognitionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

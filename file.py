
from cvzone.HandTrackingModule import HandDetector
import cv2
import socket
#1280
#720
cap = cv2.VideoCapture(0)
cap.set(3, 620)
cap.set(4, 620)
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 6060)

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    data = []

    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        # print(lmList)
        for lm in lmList:
            data.extend([lm[0], h - lm[1], lm[2]])
        sock.sendto(str.encode(str(data)), serverAddressPort)

    # Display
    cv2.imshow("Image", img)
    key=cv2.waitKey(1)
    if key==ord('q'):
        break
    cv2.waitKey(1)
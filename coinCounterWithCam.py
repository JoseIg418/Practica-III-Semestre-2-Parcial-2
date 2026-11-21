import cv2 as cv
import numpy as np

def orderPoints(points):
    n_points = np.concatenate([points[0], points[1], points[2], points[3]]).tolist()
    y_order = sorted(n_points, key=lambda n_points: n_points[1])
    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])
    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])
    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

def alignments(image, width, hight):
    aligned_image = None
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    thresholdType, threshold1 = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
    cv.imshow('Threshold hoja', threshold1)
    contour = cv.findContours(threshold1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    contour = sorted(contour, key=cv.contourArea, reverse = True)[:1]

    for c in contour:
        epsilon = 0.01 * cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, epsilon, True)
        if len(approx)==4:
            points = orderPoints(approx)
            points1 = np.float32(points)
            points2 = np.float32([[0,0], [width, 0], [0, hight], [width, hight]])
            M = cv.getPerspectiveTransform(points1, points2)
            aligned_image = cv.warpPerspective(image, M, (width,hight))
    
    return aligned_image

#0 = webcam del PC, para el celular: "http://IP_DEL_CELULAR:4747/video"
CAMERA_SOURCE = "http://192.168.1.72:4747/video"
videocapture1 = cv.VideoCapture(CAMERA_SOURCE)
if not videocapture1.isOpened():
    print('No se pudo abrir la cámara.')
    exit()

while True:
    cameraType, camera = videocapture1.read()
    if cameraType == False:
        break
    A6_image = alignments(camera, width=480, hight=640)
    if A6_image is not None:
        points = []
        gray_image = cv.cvtColor(A6_image, cv.COLOR_BGR2GRAY)
        gaussianImage = cv.GaussianBlur(gray_image, (5,5), 1)
        _,threshold2 = cv.threshold(gaussianImage, 0, 255, cv.THRESH_OTSU + cv.THRESH_BINARY_INV)
        cv.imshow('Threshold monedas', threshold2)
        contourn1 = cv.findContours(threshold2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
        cv.drawContours(A6_image, contourn1, -1, (255,0,0), 2)
        sum1 = 0.0
        sum2 = 0.0
        sum3 = 0.0
        sum4 = 0.0
        sum5 = 0.0

        for c_1 in contourn1:
            area = cv.contourArea(c_1)
            moments1 = cv.moments(c_1)
            if (moments1["m00"] == 0):
                moments1["m00"] = 1.0
        
            x = int(moments1["m10"] / moments1["m00"])
            y = int(moments1["m01"] / moments1["m00"])
        
            if area > 6700 and area < 7200:
                font = cv.FONT_HERSHEY_SIMPLEX
                cv.putText(A6_image, "P/. $1", (x,y), font, 0.75, (0,255,0), 2)
                sum1 = sum1 + 1
            if area > 7300 and area < 8200:
                    font = cv.FONT_HERSHEY_SIMPLEX
                    cv.putText(A6_image, "P/. $2", (x,y), font, 0.75, (0,255,0), 2)
                    sum2 = sum2 + 2
            if area > 8500 and area < 10750:
                    font = cv.FONT_HERSHEY_SIMPLEX
                    cv.putText(A6_image, "P/. $0.25", (x,y), font, 0.75, (0,255,0), 2)
                    sum3 = sum3 + 0.25
            if area > 10800 and area < 11000:
                    font = cv.FONT_HERSHEY_SIMPLEX
                    cv.putText(A6_image, "P/. $0.5", (x,y), font, 0.75, (0,255,0), 2)
                    sum4 = sum4 + 0.5

            if area > 21000 and area < 28000:
                font = cv.FONT_HERSHEY_SIMPLEX
                cv.putText(A6_image, "ARS $2", (x,y), font, 0.75, (0,255,0), 2)
                sum5 = sum5 + 2

        total = sum1 + sum2 + sum3 + sum4 + sum5
        print("The total sum is: ", round(total,2))
        cv.imshow("This is the A6 image", A6_image)
        cv.imshow("This is the camera image", camera)

    if cv.waitKey(1) == ord('e'):
        break

videocapture1.release()
cv.destroyAllWindows()

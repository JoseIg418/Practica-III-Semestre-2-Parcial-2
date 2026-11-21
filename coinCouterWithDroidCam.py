import cv2 

# 0 = webcam de la PC
# Celular con DroidCam (misma red Wi-Fi): "http://IP_DEL_CELULAR:4747/video"
# Celular con IP del WebCam: "http://IP_DEL_CELULAR:8080/video"

CAMERA_SOURCE = "http://192.168.100.31:4747/video"

videoCapture1 = cv2.VideoCapture(CAMERA_SOURCE)
if not videoCapture1.isOpened():
    print('The videocamera is closed')
    exit()
while True:
    ok, frame = videoCapture1.read()
    if not ok:
        print("No se pudo leer el frame")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('In Live', gray)

    if cv2.waitKey(1) == ord("e"):
        break

videoCapture1.release()
cv2.destroyAllWindows()
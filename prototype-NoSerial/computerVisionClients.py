import numpy as np
import cv2
import time
import socket

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.settimeout(0.5) # 수신 타임아웃(수신이 안되서 컴퓨터 비전이 멈추는 현상 해소)
connectingScucess = False
net = cv2.dnn.readNet("/home/pi/Documents/python/OpenCV/YOLO/Tiny/ThirdTest/yolov3-tiny_training_last.weights", "/home/pi/Documents/python/OpenCV/YOLO/Tiny/ThirdTest/yolov3-tiny_training.cfg")
classes = []
with open("/home/pi/Documents/python/OpenCV/YOLO/Tiny/ThirdTest/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

cap = cv2.VideoCapture(0)
# cap으로 웹캠 영상을 불러옴

# 아래 코드가 화면이 안깨지고 잘 나오게 하는 고정 수치
cap.set(3,640) # set Width
cap.set(4,480) # set Height

font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0

# 영상 프레임 사이즈 결정

if cap.isOpened():   # 카메라가 실행 중이라면


    while True:
        # 제대로 카메라를 불러왔다면~ 반복문을 실행
        _, frame = cap.read()
        # frame = cv2.flip(frame, 0) # 좌우 반전
        # frame = cv2.flip(frame, 1) # 상하 반전
        # 사이즈 아주 적당함
        frame_id += 1
        # ret: True False value.
        # frame: 영상 프레임을 읽음
        height, width, channels = frame.shape

        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        #src = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE) # 그레이스케일
        #dst = cv2.Canny(src, 50, 150) # 윤곽선 검출


        #frame = cv2.flip(frame, 1)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # opencv의 특성상 컬러 영상은 기본적으로 BGR로 읽기 때문에 흑백 이미지로 만들어주어야 함

        #ret, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) # 이진화

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.4:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

                if connectingScucess: # 통신 연결이 활성화된 상타에서
                    try:
                        if class_ids == [0]:
                            print("right") # right 10번 올라가면 수신하게
                            clientSock.send("@2#".encode('utf-8'))
                        elif class_ids == [1]:
                            print("left")
                            clientSock.send("@1#".encode('utf-8'))
                        elif class_ids == [2]:
                            print("down")
                            clientSock.send("@3#".encode('utf-8'))
                    except socket.timeout:
                        ''' debuging '''
                        print("Debug: Message send timeout")

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)



        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)


        #cv2.imshow("camera", gray) # 흑백 영상
        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        #cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)

        cv2.imshow("test", frame)
        #cv2.imshow("dst", dst)


        if cv2.waitkey(2) & 0xFF == 99: # 서버 연결 트리거 버튼 = 'c'
            clientSock.connect(('127.0.0.1', 8080))
            connectingScucess = True
            print("dubug: 조종기 프로그램과 소켓연결 완료")


        if cv2.waitKey(1) & 0xFF == 27: # 종료 커맨드.
            break

cap.release()
cv2.destroyAllWindows()
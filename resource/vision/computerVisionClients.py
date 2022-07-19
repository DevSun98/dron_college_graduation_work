import numpy as np
import cv2
import socket


def startVision(VisionClientSock, VisionConnectingScucess):
    net = cv2.dnn.readNet(
        "/home/pi/Documents/python/AutoDroneControllerSystem/vision/yolov3-tiny_training_last.weights",
        "/home/pi/Documents/python/AutoDroneControllerSystem/vision/yolov3-tiny_training.cfg")
    classes = []
    with open("/home/pi/Documents/python/AutoDroneControllerSystem/vision/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0)]
    count = [0, 0, 0]

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # 해상도 변경
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # 해상도 변경
    # cap으로 웹캠 영상을 불러옴

    # 아래 코드가 화면이 안깨지고 잘 나오게 하는 고정 수치
    cap.set(3, 480)  # set Width
    cap.set(4, 320)  # set Height

    font = cv2.FONT_HERSHEY_PLAIN
    frame_id = 0

    # 영상 프레임 사이즈 결정

    if cap.isOpened():  # 카메라가 실행 중이라면

        while True:
            # 제대로 카메라를 불러왔다면~ 반복문을 실행
            _, frame = cap.read()
            # frame = cv2.resize(frame, dsize=(480, 320), fx=2, fy=2, interpolation=cv2.INTER_LINEAR)  # 확대 추가 실험
            frame = cv2.flip(frame, -1)  # 상하좌우 반전
            # frame = cv2.flip(frame, 0) # 좌우 반전
            # frame = cv2.flip(frame, 1) # 상하 반전
            # 사이즈 아주 적당함
            frame_id += 1
            # ret: True False value.
            # frame: 영상 프레임을 읽음
            height, width, channels = frame.shape

            blob = cv2.dnn.blobFromImage(frame, 0.00392, (480, 320), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            # src = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE) # 그레이스케일
            # dst = cv2.Canny(src, 50, 150) # 윤곽선 검출

            # frame = cv2.flip(frame, 1)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # opencv의 특성상 컬러 영상은 기본적으로 BGR로 읽기 때문에 흑백 이미지로 만들어주어야 함

            # ret, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) # 이진화

            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.3:
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

                        if VisionConnectingScucess:  # 통신 연결이 활성화된 상타에서
                            try:
                                if class_ids == [0]:
                                    # print("right")  # right 10번 올라가면 수신하게
                                    count[0] = count[0] + 1
                                    if count[0] > 5:
                                        print("RightVisionData Send")
                                        VisionClientSock.send("@2#".encode('utf-8'))
                                        count[0] = 0
                                elif class_ids == [1]:
                                    # print("left")
                                    count[1] = count[1] + 1
                                    if count[1] > 5:
                                        print("LeftVisionData Send")
                                        VisionClientSock.send("@1#".encode('utf-8'))
                                        count[1] = 0
                                elif class_ids == [2]:
                                    # print("down")
                                    count[2] = count[2] + 1
                                    if count[2] > 5:
                                        print("DownVisionData Send")
                                        VisionClientSock.send("@3#".encode('utf-8'))
                                        count[2] = 0
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
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 2, color, 2)

            # cv2.imshow("camera", gray) # 흑백 영상
            # cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)

            cv2.imshow("ComputerVision", frame)
            # cv2.imshow("dst", dst)

            keyPressValue = cv2.waitKey(1)
            if keyPressValue & 0xFF == 99:
                VisionClientSock.connect(('127.0.0.1', 8080))
                VisionConnectingScucess = True
                print("dubug: Sever Connecting Sucess")

            elif keyPressValue & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSock.settimeout(0.5)  # 수신 타임아웃(수신이 안되서 컴퓨터 비전이 멈추는 현상 해소)
    connectingScucess = False

    startVision(clientSock, connectingScucess)

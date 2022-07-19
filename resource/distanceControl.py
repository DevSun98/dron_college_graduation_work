import time

''' !반드시 목표 고도 2M로 설정하기! '''

def distanceUP(DC_gui):
    serial = DC_gui.getSerialIns()  # SerialCOM 인스턴스 가져오기

    goalCount = 0
    errorCount = 0
    DC_gui.distanceLabelF.configure(fg="#000000")
    DC_gui.distanceLabelS.configure(fg="#000000")
    DC_gui.distanceLabelT.configure(fg="#000000")

    while goalCount < 10 and errorCount < 3:  # 3초 timeout 생기면 루프 종료
        distance = serial.serialLidarMakeDistance()  # Lidar distance 가져오기
        DC_gui.distanceLabelS.configure(text=(distance - 2) / 100)

        ''' debuging!!!!! '''
        # if distance > 200:  # 목표 고도가 2미터 이상이 됐을 경우
        if distance > 190:  # 목표 고도가 2미터 이상이 됐을 경우
            goalCount = goalCount + 1

        elif distance == -1:  # 타임 아웃 에러 카운트
            errorCount = errorCount + 1

    if goalCount >= 10:
        DC_gui.distanceLabelF.configure(fg="#DDDDDD")
        DC_gui.distanceLabelS.configure(fg="#DDDDDD")
        DC_gui.distanceLabelT.configure(fg="#DDDDDD")

    if errorCount >= 3:
        DC_gui.distanceLabelT.configure(fg="#FF0000")
        DC_gui.distanceLabelS.configure(text="error")

    serial.serialLidarClose()


def distanceDown(DC_gui):
    serial = DC_gui.getSerialIns()  # SerialCOM 인스턴스 가져오기

    goalCount = 0
    errorCount = 0
    DC_gui.distanceLabelF.configure(fg="#000000")
    DC_gui.distanceLabelS.configure(fg="#000000")
    DC_gui.distanceLabelT.configure(fg="#000000")

    while goalCount < 10 and errorCount < 5:
        distance = serial.serialLidarMakeDistance()  # Lidar distance 가져오기
        DC_gui.distanceLabelS.configure(text=(distance - 2) / 100)

        if distance < 5:  # 목표 고도가 5cm으로 떨어졌을 경우
            goalCount = goalCount + 1

        elif distance == -1:  # 타임 아웃 에러카운트
            errorCount = errorCount + 1

    if goalCount >= 10:
        DC_gui.distanceLabelF.configure(fg="#DDDDDD")
        DC_gui.distanceLabelS.configure(fg="#DDDDDD")
        DC_gui.distanceLabelT.configure(fg="#DDDDDD")

    if errorCount >= 5:
        DC_gui.distanceLabelT.configure(fg="#FF0000")
        DC_gui.distanceLabelS.configure(text="error")
        time.sleep(8)  # 타임아웃 에러로 인한 추락 방지 딜레이

    serial.serialLidarClose()

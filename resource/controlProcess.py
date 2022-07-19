def throttleUp(throttleScaleValue, throttleScale, serial):
    throttleScaleValue = throttleScaleValue + 2  # 필수!! 무조건 짝수로 증가 및 감소
    serial.serialOutput(str(throttleScaleValue))
    throttleScale.set(throttleScaleValue)
    return throttleScaleValue


def throttleDown(throttleScaleValue, throttleScale, serial):
    throttleScaleValue = throttleScaleValue - 2  # 필수!! 무조건 짝수로 증가 및 감소
    serial.serialOutput(str(throttleScaleValue))
    throttleScale.set(throttleScaleValue)
    return throttleScaleValue


''' 시리얼 전송 값 메뉴얼 '''


# 1 : Yaw(1: right, 2: left, 0: idle)
# 2 : Pitch(1: right, 2: left, 0: idle)
# 3 : Roll(1: right, 2: left, 0: idle)
# 4 : arm(1: on, 0: off)
# 5 : flightMode(0: mode1, 1: mode2, 2: mode3, 3: mode4)

def yawLeft(yawScale, serial):
    yawScale.set(148)
    serial.serialOutput("012")
    return 0


def yawRight(yawScale, serial):
    yawScale.set(228)
    serial.serialOutput("011")
    return 0


def pitchLeft(pitchScale, serial):
    pitchScale.set(168)
    serial.serialOutput("022")
    return 0


def pitchRight(pitchScale, serial):
    pitchScale.set(208)
    serial.serialOutput("021")
    return 0


def rollLeft(rollScale, serial):
    rollScale.set(168)
    serial.serialOutput("032")
    return 0


def rollRight(rollScale, serial):
    rollScale.set(208)
    serial.serialOutput("031")
    return 0


def arm(startButton, serial, throttleScale):
    startButtonActivation = startButton["background"]  # startButtonLabel 속성값 출력
    throttleScaleValue = 113
    throttleScale.set(throttleScaleValue)

    if startButtonActivation != "#FF9664":  # 활성화x 일 때 시동On
        serial.serialOutput("041")  # 시동 명령에서 분기를 해야 할지 의문 써야 한다면 이 코드를 사용
        startButton.configure(bg="#FF9664")

    else:
        serial.serialOutput("040")  # 시동 명령에서 분기를 해야 할지 의문 써야 한다면 이 코드를 사용
        startButton.configure(bg="#DDDDDD")  # 활성화o 일 때 시동Off

    return throttleScaleValue


def flightMode(flightmodeLabel, Mode, serial):
    flightmodeLabel.configure(text=Mode)

    if Mode == "비행모드1":
        serial.serialOutput("050")

    elif Mode == "비행모드2":
        serial.serialOutput("051")

    elif Mode == "비행모드3":
        serial.serialOutput("052")

    elif Mode == "비행모드4":
        serial.serialOutput("053")

    return 0



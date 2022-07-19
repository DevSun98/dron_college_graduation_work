''' gui를 객체선언을 해서 거기에 있는 컨탠츠의 인스턴스 필드를 가져와야 함 '''
import controlProcess
import time

'''debuging'''


def start(order_channel, order_type, order_GUI):  # serial 써야 됨

    def streamThrottle():
        scriptsThrottleValue = [113, 159, 189, 209] # min, down, idle, up
        goalThrottleValue = scriptsThrottleValue[order_type]
        throttleScale = order_GUI.getThrottleScale()
        throttleScaleValue = throttleScale.get()

        if throttleScaleValue < goalThrottleValue:  # 증가
            throttleScale.configure(state='normal')  # 스케일 바 잠금 해제
            while throttleScaleValue < goalThrottleValue:
                throttleScaleValue = controlProcess.throttleUp(throttleScaleValue, throttleScale)
                time.sleep(0.08)
            throttleScale.configure(state='disable')  # 스케일 바 잠금

        elif goalThrottleValue < throttleScaleValue:  # 감소
            throttleScale.configure(state='normal')  # 스케일 바 잠금 해제
            while goalThrottleValue < throttleScaleValue:
                throttleScaleValue = controlProcess.throttleDown(throttleScaleValue, throttleScale)
                time.sleep(0.08)
            throttleScale.configure(state='disable')  # 스케일 바 잠금

    ''' 딕셔너리 규칙: 1: 증가, 0: 감소 '''
    controlCallback = {'t': lambda: streamThrottle(),
                       'y': lambda: controlProcess.yawRight(
                           order_GUI.getYawScale()) if order_type == 1 else controlProcess.yawLeft(
                           order_GUI.getYawScale()) if order_type == 0 else print("Error: YawCall_error"),
                       'p': lambda: controlProcess.pitchRight(
                           order_GUI.getPitchScale()) if order_type == 1 else controlProcess.pitchLeft(
                           order_GUI.getPitchScale()) if order_type == 0 else print("Error: PitchCall_error"),
                       'r': lambda: controlProcess.rollRight(
                           order_GUI.getRollScale()) if order_type == 1 else controlProcess.rollLeft(
                           order_GUI.getRollScale()) if order_type == 0 else print("Error: RollCall_error"),
                       'a': lambda: controlProcess.arm(order_GUI.getStartButton(),
                                                       order_GUI.getThrottleScale()) if order_type == 1 else print(
                           "Error: ArmCall_error"),
                       'f': lambda: controlProcess.flightMode(
                           order_GUI.getFlightmode(), "비행모드1")
                       if order_type == 0 else controlProcess.flightMode(order_GUI.getFlightmode(), "비행모드2")
                       if order_type == 1 else controlProcess.flightMode(order_GUI.getFlightmode(), "비행모드3")
                       if order_type == 2 else controlProcess.flightMode(order_GUI.getFlightmode(), "비행모드4")
                       if order_type == 3 else print("Error: flightModeCall_error")}

    controlCallback.get(order_channel, lambda: print("Error: controlCallback_error"))()


def stop(order_channel, order_GUI):  # serial 써야됨
    if order_channel == 'p':
        # order_serial.serialOutput("020")  # 조종기 IDLE 상태로 아두이노에게 전송
        print("Message: Pitch idle")
        order_GUI.getPitchScale().set(188)
    elif order_channel == 'r':
        # order_serial.serialOutput("030")  # 조종기 IDLE 상태로 아두이노에게 전송
        print("Message: Roll idle")
        order_GUI.getRollScale().set(188)
    elif order_channel == 'y':
        # order_serial.serialOutput("010")  # 조종기 IDLE 상태로 아두이노에게 전송
        print("Message: Yaw idle")
        order_GUI.getYawScale().set(188)
    else:
        print("Error: controlStopCallback_error")

# def start(order_channel, order_type, order_GUI):  # serial 써야 됨
#     order_serial = order_GUI.getSerialIns()

#     def streamThrottle():
#         scriptsThrottleValue = [113, 159, 189, 205]
#         goalThrottleValue = scriptsThrottleValue[order_type]
#         throttleScale = order_GUI.getThrottleScale()
#         throttleScaleValue = throttleScale.get()
#
#         if throttleScaleValue < goalThrottleValue:  # 증가
#             while throttleScaleValue < goalThrottleValue:
#                 throttleScaleValue = controlProcess.throttleUp(throttleScaleValue, throttleScale, order_serial)
#                 time.sleep(0.040)
#         elif goalThrottleValue < throttleScaleValue:  # 감소
#             while goalThrottleValue < throttleScaleValue:
#                 throttleScaleValue = controlProcess.throttleDown(throttleScaleValue, throttleScale, order_serial)
#                 time.sleep(0.040)
#
#     ''' 딕셔너리 규칙: 1: 증가, 0: 감소 '''
#     controlCallback = {'t': lambda: streamThrottle(),
#                        'y': lambda: controlProcess.yawRight(
#                            order_GUI.getYawScale(), order_serial) if order_type == 1 else controlProcess.yawLeft(
#                            order_GUI.getYawScale(), order_serial) if order_type == 0 else print("Error: YawCall_error"),
#                        'p': lambda: controlProcess.pitchRight(
#                            order_GUI.getPitchScale(), order_serial) if order_type == 1 else controlProcess.pitchLeft(
#                            order_GUI.getPitchScale(), order_serial) if order_type == 0 else print("Error: PitchCall_error"),
#                        'r': lambda: controlProcess.rollRight(
#                            order_GUI.getRollScale(), order_serial) if order_type == 1 else controlProcess.rollLeft(
#                            order_GUI.getRollScale(), order_serial) if order_type == 0 else print("Error: RollCall_error"),
#                        'a': lambda: controlProcess.arm(order_GUI.getStartButton(), order_serial,
#                                                        order_GUI.getThrottleScale()) if order_type == 1 else print(
#                            "Error: ArmCall_error"),
#                        'f': lambda: controlProcess.flightMode(
#                            order_GUI.getFlightmode(), "비행모드1", order_serial)
#                        if order_type == 0 else controlProcess.flightMode(order_GUI.getFlightmode(), "비행모드2", order_serial)
#                        if order_type == 1 else controlProcess.flightMode(order_GUI.getFlightmode(), "비행모드3", order_serial)
#                        if order_type == 2 else controlProcess.flightMode(order_GUI.getFlightmode(), "비행모드4", order_serial)
#                        if order_type == 3 else print("Error: flightModeCall_error")}
#
#     print("debug: order 도착")
#     controlCallback.get(order_channel, lambda: print("Error: controlCallback_error"))()
#
#
# def stop(order_channel, order_GUI):  # serial 써야됨
#     order_serial = order_GUI.getSerialIns()
#
#     if order_channel == 'p':
#         order_serial.serialOutput("020")  # 조종기 IDLE 상태로 아두이노에게 전송
#         print("Pitch idle")
#         order_GUI.getPitchScale().set(188)
#     elif order_channel == 'r':
#         order_serial.serialOutput("030")  # 조종기 IDLE 상태로 아두이노에게 전송
#         print("Roll idle")
#         order_GUI.getRollScale().set(188)
#     elif order_channel == 'y':
#         order_serial.serialOutput("010")  # 조종기 IDLE 상태로 아두이노에게 전송
#         print("Yaw idle")
#         order_GUI.getYawScale().set(188)
#     else:
#         print("Error: controlStopCallback_error")

''' start, stop 함수가 실행되는 스크립트 '''
import time
import droneController_order as DC_order

''' t: throttle
    p: pitch
    r: roll
    y: yaw
    a: armming
    f: flightmode'''

THROTTLE_MIN = 0
THROTTLE_DOWN = 1
THROTTLE_HOVER = 2
THROTTLE_UP = 3
PITCH_GOING = 1
PITCH_REVERSE = 0
ROLL_LEFT = 0
ROLL_RIGHT = 1
YAW_LEFT = 0
YAW_RIGHT = 1
ARM = 1
F_MODE1 = 0
F_MODE2 = 1
F_MODE3 = 2
F_MODE4 = 3

''' start(채널유형, 작동유형, 드론컨트롤러 GUI, 시리얼)
    stop(채널유형, 드론컨트롤러 GUI, 시리얼)'''

''' ! 중요 ! '''
''' serial 인스턴스를 GUI인스턴스에 묶었기 때문에 파라미터로 전송하지 않아도 됨, order 부분에서 호출하여 사용할 것임'''

'''debuging'''


def emergency(DC_gui):
    DC_order.stop('p', DC_gui)
    time.sleep(2)
    DC_order.stop('r', DC_gui)
    time.sleep(2)
    DC_order.stop('y', DC_gui)
    time.sleep(2)
    DC_order.start('t', THROTTLE_DOWN, DC_gui)
    # 일단 내려갈때 스로틀 수치를 서서히 낮추자는 의견이 있음 일단 지금은 딜레이로 시간을 정하도록 하겠습니다
    time.sleep(6)  # 실전 데이터 필요 (하강 딜레이)
    DC_order.start('t', THROTTLE_MIN, DC_gui)
    time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
    # DC_order.start('a', ARM, DC_gui)  # 실전에서는 arm
    time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)


# memo takeoff에서 시동을 작동시키지 않는다. armming을 실행하고 시동이 잘 작동되면 takeoff를 진행
def takeoff(DC_gui):
    # DC_order.start('a', ARM, DC_gui)  # 실전에서는 arm
    time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
    DC_order.start('t', THROTTLE_UP, DC_gui)  # throttle 189까지 올리기
    time.sleep(10)  # 실전 데이터 필요 (스크립트 진행 속도)
    DC_order.start('t', THROTTLE_HOVER, DC_gui)  # throttle 189까지 올리기


def goto(DC_gui):
    DC_order.start('p', PITCH_GOING, DC_gui)
    # 노 딜레이 바로 다음 실행

''' 장애물을 회피하는 회피기동 작동스크립트 '''


def left(DC_gui):
    DC_order.stop('p', DC_gui)
    time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
    DC_order.start('r', ROLL_LEFT, DC_gui)
    # 여기서 왼쪽으로 이동하는데 얼마만큼 유지할 건지 time.sleep()
    time.sleep(4)  # 실전 데이터 필요 (좌우 이동 딜레이)
    DC_order.stop('r', DC_gui)
    time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)

def right(DC_gui):
    DC_order.stop('p', DC_gui)
    time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
    DC_order.start('r', ROLL_RIGHT, DC_gui)
    # 여기서 오른쪽으로 이동하는데 얼마만큼 유지할 건지 time.sleep()
    time.sleep(4)  # 실전 데이터 필요 (좌우 이동 딜레이)
    DC_order.stop('r', DC_gui)
    time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)

def landing(DC_gui):
    # 여기도 goto멈추는 것을 여기서 진행할지 아니면 gotostop 호출할지 의문 지금은 여기서 실행하도록 설정
    DC_order.stop('p', DC_gui)
    time.sleep(4)  # 실전 데이터 필요 (호버링 딜레이)
    DC_order.start('t', THROTTLE_DOWN, DC_gui)
    # 일단 내려갈때 스로틀 수치를 서서히 낮추자는 의견이 있음 일단 지금은 딜레이로 시간을 정하도록 하겠습니다
    time.sleep(6)  # 실전 데이터 필요 (하강 딜레이)
    DC_order.start('t', THROTTLE_MIN, DC_gui)
    time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
    # DC_order.start('a', ARM, DC_gui)  # 실전에서는 arm
    time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)


''' 1106 테스트는 일단 보류'''

# def armming(DC_gui, serial):
#     DC_order.start('a', ARM, DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#
# # memo takeoff에서 시동을 작동시키지 않는다. armming을 실행하고 시동이 잘 작동되면 takeoff를 진행
# def takeoff(DC_gui, serial):
#     DC_order.start('f', F_MODE2, DC_gui, serial) # position mode 실행
#     time.sleep(2) # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.start('t', THROTTLE_HOVER, DC_gui, serial) # throttle 189까지 올리기
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.start('f', F_MODE3, DC_gui, serial) # takeoff mode 실행
#     # 올라간다 약간 예메한 부분: 목표고도까지 스크립트 진행을 멈춤 time.sleep()
#     time.sleep(4)  # 실전 데이터 필요 (상승 딜레이)
#     DC_order.start('f', F_MODE2, DC_gui, serial)  # position mode 실행
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#
# def goto(DC_gui, serial):
#     DC_order.start('p', PITCH_GOING, DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#
# # def gotoStop(DC_gui, serial):  # 만약 시나리오 생성기에서 gotostop 명령을 사용할 경우 이 함수를 사용
# #     DC_order.stop('p', DC_gui, serial)
# #     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#
# ''' 장애물을 회피하는 회피기동 작동스크립트 '''
# def left(DC_gui, serial):
#     DC_order.stop('p', DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.start('r', ROLL_LEFT,  DC_gui, serial)
#     # 여기서 왼쪽으로 이동하는데 얼마만큼 유지할 건지 time.sleep()
#     time.sleep(4)  # 실전 데이터 필요 (좌우 이동 딜레이)
#     DC_order.stop('r', DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.start('p', PITCH_GOING, DC_gui, serial)  # 일단은 의미로 left 스크립트에서 goto를 실행을 했음 시나리오 생성기 구현할 때 회피기동 끝나고 재시작 어떻게 할 껀지 결정바람
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#
#
# def right(DC_gui, serial):
#     DC_order.stop('p', DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.start('r', ROLL_RIGHT, DC_gui, serial)
#     # 여기서 오른쪽으로 이동하는데 얼마만큼 유지할 건지 time.sleep()
#     time.sleep(4)  # 실전 데이터 필요 (좌우 이동 딜레이)
#     DC_order.stop('r', DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.start('p', PITCH_GOING, DC_gui,
#                    serial)  # 일단은 의미로 left 스크립트에서 goto를 실행을 했음 시나리오 생성기 구현할 때 회피기동 끝나고 재시작 어떻게 할 껀지 결정바람
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#
# def landing(DC_gui, serial):
#     # 여기도 goto멈추는 것을 여기서 진행할지 아니면 gotostop 호출할지 의문 지금은 여기서 실행하도록 설정
#     DC_order.stop('p', DC_gui, serial)
#     time.sleep(4)  # 실전 데이터 필요 (호버링 딜레이)
#     DC_order.start('t', THROTTLE_DOWN,  DC_gui, serial)
#     # 일단 내려갈때 스로틀 수치를 서서히 낮추자는 의견이 있음 일단 지금은 딜레이로 시간을 정하도록 하겠습니다
#     time.sleep(6)  # 실전 데이터 필요 (하강 딜레이)
#     DC_order.start('t', THROTTLE_MIN, DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.start('a', ARM, DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#
# def emergency(DC_gui, serial):  # 비상상황 대처 스크립트
#     DC_order.stop('p',  DC_gui, serial)
#     time.sleep(0.5)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.stop('r', DC_gui, serial)
#     time.sleep(0.5)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.stop('y', DC_gui, serial)
#     time.sleep(0.5)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.start('t', THROTTLE_DOWN, DC_gui, serial)
#     # 일단 내려갈때 스로틀 수치를 서서히 낮추자는 의견이 있음 일단 지금은 딜레이로 시간을 정하도록 하겠습니다
#     time.sleep(6)  # 실전 데이터 필요 (하강 딜레이)
#     DC_order.start('t', THROTTLE_MIN, DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#     DC_order.start('a', ARM, DC_gui, serial)
#     time.sleep(2)  # 실전 데이터 필요 (스크립트 진행 속도)
#
# ''' 1106 테스트는 일단 보류'''

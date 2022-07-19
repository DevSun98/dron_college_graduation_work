''' start, stop 함수가 실행되는 스크립트 '''
import time
import droneController_order as DC_order
import distanceControl as distance

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


# 스크립트로 시동을 거는것은 너무 위험하다고 판단하여 실제로 arm을 실행하지 않고 로직만 실행되도록 설정
# DC_gui.startButton.configure(bg="#FF9664") <- arm이 되었다는 트리거로 사용되고 있다.


def armming(DC_gui):
    DC_order.start('a', ARM, DC_gui)


def emergency(DC_gui):
    DC_order.stop('p', DC_gui)
    time.sleep(0.5)
    DC_order.stop('r', DC_gui)
    time.sleep(0.5)
    DC_order.stop('y', DC_gui)
    time.sleep(2)
    DC_order.start('t', THROTTLE_DOWN, DC_gui)
    distance.distanceDown(DC_gui)  # 라이다 센서를 사용하여 일정고도 이하면 스로틀 낮추기
    DC_order.start('t', THROTTLE_MIN, DC_gui)
    time.sleep(3)
    DC_order.start('a', ARM, DC_gui)
    time.sleep(1)


# memo takeoff에서 시동을 작동시키지 않는다. armming을 실행하고 시동이 잘 작동되면 takeoff를 진행
def takeoff(DC_gui):
    # DC_gui.startButton.configure(bg="#FF9664")  # 스크립트로 시동을 거는것은 너무 위험하다고 판단하여 실제로 arm을 실행하지 않고 로직만 실행되도록 설정
    # time.sleep(2)
    DC_order.start('t', THROTTLE_UP, DC_gui)
    distance.distanceUP(DC_gui)  # 라이다 센서를 사용하여 일정고도(2m)에서 상승 멈추기
    DC_order.start('t', THROTTLE_HOVER, DC_gui)
    time.sleep(3)


def goto(DC_gui):
    DC_order.start('p', PITCH_GOING, DC_gui)
    # 노 딜레이 바로 다음 실행


def left(DC_gui):
    DC_order.stop('p', DC_gui)
    time.sleep(2)
    DC_order.start('r', ROLL_LEFT, DC_gui)
    # 여기서 왼쪽으로 이동하는데 얼마만큼 유지할 건지 time.sleep()

    ''' ! 반드시 ! '''
    time.sleep(4)  # 실전에서 포지션 모드에서 상태를 점검한 뒤에 설정

    DC_order.stop('r', DC_gui)
    time.sleep(3)


def right(DC_gui):
    DC_order.stop('p', DC_gui)
    time.sleep(2)
    DC_order.start('r', ROLL_RIGHT, DC_gui)
    # 여기서 왼쪽으로 이동하는데 얼마만큼 유지할 건지 time.sleep()

    ''' ! 반드시 ! '''
    time.sleep(4)  # 실전에서 포지션 모드에서 상태를 점검한 뒤에 설정

    DC_order.stop('r', DC_gui)
    time.sleep(3)


def landing(DC_gui):
    DC_order.stop('p', DC_gui)
    time.sleep(3)
    DC_order.start('t', THROTTLE_DOWN, DC_gui)
    distance.distanceDown(DC_gui)  # 라이다 센서를 사용하여 일정고도 이하면 스로틀 낮추기
    DC_order.start('t', THROTTLE_MIN, DC_gui)
    time.sleep(3)
    DC_order.start('a', ARM, DC_gui)
    time.sleep(1)

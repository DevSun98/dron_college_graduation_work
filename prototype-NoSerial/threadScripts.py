import threading
import droneController_scripts as DC_scripts
import tkinter.messagebox as msg
import scenarioGenerator

''' input으로 인해 스레드가 자동으로 안꺼짐 프로그램을 종료하면 demon에 의해 스레드도 종료되지만 처음으로 되돌아 갈때는 'q'를 입력하여 종료시켜야 함 '''

''' debuging'''
def threadRun(DCG_ins, severSock):  # DCG: DroneController_GUI 드론조종기GUI 객체 인스턴스, Serial: 시리얼 통신 객체 인스턴스
    scriptsCallback = {'takeoff': lambda: DC_scripts.takeoff(DCG_ins),
                       'goto': lambda: DC_scripts.goto(DCG_ins),
                       'left': lambda: DC_scripts.left(DCG_ins),
                       'right': lambda: DC_scripts.right(DCG_ins),
                       'landing': lambda: DC_scripts.landing(DCG_ins),
                       'emergency': lambda: DC_scripts.emergency(DCG_ins)
                       }

    control = 0  # 시나리오 생성기 제어변수 생성
    print("Debug: accept() waiting")
    connectionSock, addr = severSock.accept() # socket.accept() 대기
    print("Debug: Detect client's connection request")

    if addr[0] == '127.0.0.1':
        print("Message: Client connecting successful ")
        DCG_ins.takeoffStart.configure(state='normal') # 컴퓨터비전이 연결되어야 takeoff 활성
        connectionSock.settimeout(0.1) # 송수신 타임아웃 설정
        control = 1

    else:
        msg.showwarning("프로세스간 통신", "잘못된 접근의 IP 입니다.\n 프로세스를 종료합니다.")
        severSock.close()
        connectionSock.close()
        DCG_ins.btnOnClick_Exit() # 0으로 실행되면 메인 스레드가 종료, -1으로 실행되면 아래 while이 작동되지만 첫구문 if 에서 스레드가 종료된다.

    ''' 여기까지가 클라이언트와 네트워크 연결 '''

    while True:
        if DCG_ins.controllerAfterReturn == -1:  # 스레드 중복 생성 버그를 막기 위해 컨트롤러 종료 확인 절차를 제일 첫번째로 실행
            severSock.close()
            connectionSock.close()
            print("Debug: The main thread exits, terminating the thread.")
            break

        # 시나리오 생성기 실행 return: 스크립트 실행 키워드
        scenario, control = scenarioGenerator.scenarioMaker(DCG_ins, connectionSock, control)
        DCG_ins.scriptsMode.configure(text=scenario)

        # emergency 구문
        if scenario == "emergency":
            print("Message: Emergency Start")
            scriptsCallback.get("emergency", lambda: print("Message: Waiting for data to be received"))()  # Dictionary default 기능 추가
            scenario = None

        # control 0 구문
        if control == 0:
            print("Debug: ScenarioControl ordered to quit, terminating the thread")
            severSock.close()
            connectionSock.close()
            DCG_ins.btnOnClick_Exit()
            break

        # 딕셔너리 자료형 실행 -> 비행 스크립트 진행
        scriptsCallback.get(scenario, lambda: print("Message: Waiting for data to be received"))()  # Dictionary default 기능 추가


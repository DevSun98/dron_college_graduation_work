import droneController_GUI as DC_GUI
import serial_conn as SE_GUI
import threadScripts
import threading
import socket as S

''' ! 중요 ! 1113'''
''' 시리얼 인스턴스를 GUI 객체에 저장을 하였습니다. 따로 Result(Serial)인스를 파라미터로 연결하지 않아도 됩니다! 필수 참고 '''


if __name__ == '__main__':
    while True:
        Result = SE_GUI.serialCheckGUI() # 시리얼 통신 연결이 성공되면 serial 인스턴스 배출
        print("Message: Arduino connection complete")

        ''' 정상 코드 '''
        if type(Result) != int:
            # !& 소켓 생성
            serverSock = S.socket(S.AF_INET, S.SOCK_STREAM)
            serverSock.bind(('', 8080))
            serverSock.listen(1)

            droneController_GUI = DC_GUI.DroneController(Result)  # 드론 GUI 인스턴스 생성 및 시리얼 인스턴스 GUI 객체에 저장

            # 스레드 시작 (GUI 인스턴스, serverSocket 인스턴스) ... serial 인스턴스는 GUI 객체에서 저장하도록 설정하였음
            ''' debuging '''
            # AutoDroneProcess_thread = threading.Thread(name="AutoDroneProcess_thread", target=threadScripts.threadRun,
            #                                            args=(droneController_GUI, Result, serverSock)) # Result: serial 값 들어가야 됨
            AutoDroneProcess_thread = threading.Thread(name="AutoDroneProcess_thread", target=threadScripts.threadRun,
                                                       args=(droneController_GUI, serverSock,))  # Result: serial 값 들어가야 됨, severSock: 소켓 인스턴스

            AutoDroneProcess_thread.daemon = True # Main이 종료되면 스레드도 종료
            AutoDroneProcess_thread.start()

            # droneController GUI 시작
            Result = droneController_GUI.startGUI()

        # DroneController가 종료되면 GUI인스턴스와 스레드 종료
        if Result == 0:
            break

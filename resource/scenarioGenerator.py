import time
import socket as S


def scenarioMaker(DCG_ins, connectionSock, control):
    returnScenario = None

    if control == 1:  # 1번째 단계, takeoff 대기
        while True:
            if DCG_ins.takeoffTrigger == 1:
                returnScenario = "takeoff"
                control = 2
                break

            elif DCG_ins.takeoffTrigger == -1:
                returnScenario = None  # 필요 없을 것 같은데 일단 넣기
                control = 0
                break

    elif control == 2:  # 2번째 단계, takeoff, left, right가 실행된 후, 버퍼 비우기
        while True:
            try:
                connectionSock.recv(3)  # 버퍼 비우기

            except S.timeout:
                break

        DCG_ins.showEnterkey.configure(text="탐색")
        returnScenario = "goto"
        control = 3

    elif control == 3:  # 3번째 단계, 탐지 데이터 받기
        ''' 클라이언트로 부터 받는 데이터 유형은: '@n#' 1: 왼쪽, 2: 오른쪽, 3: 착륙  이다 '''
        try:
            data = connectionSock.recv(3)
            data = data.decode('utf-8')
            if len(data) == 3 and data[0] == '@' and data[2] == '#':  # 수신 데이터 검사
                # 데이터 유형에 따라 returnScenario = {left,right,land}결정 그리고 control 리턴 2 (버퍼 비우기 다시 시작)
                DCG_ins.showEnterkey.configure(text="감지")
                data = data[1]
                if data == '1':
                    returnScenario = "left"
                    control = 2
                elif data == '2':
                    returnScenario = "right"
                    control = 2
                elif data == '3':
                    returnScenario = "landing"
                    control = 4

            else:
                raise S.timeout  # 데이터 검사기에서 오류를 감지하면 timeout 예외처리로 except를 실행

        except S.timeout:
            returnScenario = None
            control = 3

        if DCG_ins.emergencyTrigger == 1:  # 비상 버튼 트리거 작동을 감지했을 경우
            print("Message: Emergency was detected")
            DCG_ins.showEnterkey.configure(text="비상")
            returnScenario = "emergency"
            control = 0

    elif control == 4:  # 4번째 단계, landing이 이루어졌으면 종료절차 실행
        returnScenario = None
        control = 0

    return returnScenario, control   # 시나리오, 시나리오 생성기 제어변수 리턴

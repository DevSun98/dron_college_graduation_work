import serial
import time


class SerialCOM:

    def __init__(self):
        self.serialInst = None

    def serialCreate(self, setPortName, setBaudRate):  # 시리얼 생성 begin
        if self.serialInst is not None:
            self.serialInst.__del__()
            self.serialInst = None

        try:
            self.serialInst = serial.Serial(port=setPortName, baudrate=setBaudRate, timeout=1)
            return True

        except serial.SerialException:
            return False

    def serialOutput(self, data):  # 시리얼 전송
        if self.serialInst is None:
            return False

        data = "#" + data + "@"

        try:
            self.serialInst.write(bytearray(data.encode()))
            return True

        except serial.SerialTimeoutException:
            print("송신 타임아웃")
            return False

    def Ard_BeginningState(self):
        time.sleep(1)  # 2초 딜레이
        self.serialOutput("000")  # 000 데이터 전송
        time.sleep(1)  # 1초 딜레이

        result = -1  # 함수 결과의 return 값 0: 실패, 1: 성공, -1: 오류
        max_time_end = time.time() + 3
        while True:
            print("루프중")
            if self.serialInst.readable():
                res = self.serialInst.readline().decode()
                self.serialInst.flush()
                res = res[0:5]

                if not len(res) != 5 or res[0] != '#' or res[4] != '@':  # 정상적으로 데이터가 들어왔을 경우
                    if res == "#111@":
                        result = 1
                    else:
                        result = 0
                    break

            if time.time() > max_time_end:
                break

        return result

    def serialDebugPrint(self):  # 아두이노 측에서 보내는 시리얼 받기
        if self.serialInst.readable():
            res = self.serialInst.readline()
            print(res.decode()[:len(res) - 1])
            self.serialInst.flush()

    def serialClose(self):  # 시리얼 객체 해제
        self.serialInst.__del__()
        self.serialInst = None

    def setSerialInst(self):  # 시리얼 객체 인스턴스 얻기 //근데 이거 쓸 이유가 없는거 같음
        return self.serialInst

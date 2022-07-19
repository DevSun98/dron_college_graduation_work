import serial
import time


class SerialCOM:

    def __init__(self):
        self.serialInst = None
        self.serialLidarInst = None

    def serialCreate(self, setPortName, setBaudRate):  # 시리얼 생성 begin
        if self.serialInst is not None:
            self.serialInst.__del__()
            self.serialInst = None

        try:
            self.serialInst = serial.Serial(port=setPortName, baudrate=setBaudRate, timeout=1)
            print("Message: ArduinoSerial connecting Successful")
            return True

        except serial.SerialException:
            return False

    def serialLidarCreate(self, setPortName, setBaudRate):  # Lidar 시리얼 생성 begin
        if self.serialLidarInst is not None:
            self.serialLidarInst.__del__()
            self.serialLidarInst = None

        try:
            self.serialLidarInst = serial.Serial(port=setPortName, baudrate=setBaudRate, timeout=1)
            self.serialLidarInst.close()
            print("Message: LidarSerial connecting Successful")
            return True

        except serial.SerialException:
            return False

    def serialLidarMakeDistance(self):  # 라이다 데이터 가져오기
        if not self.serialLidarInst.is_open:
            self.serialLidarInst.open()

        while True:
            try:  # timeout으로 인한 예외처리
                count = self.serialLidarInst.in_waiting
                if count > 10:
                    recv = self.serialLidarInst.read(9)
                    self.serialLidarInst.reset_input_buffer()

                    if recv[0] == 0x59 and recv[1] == 0x59:  # python3
                        distance = recv[2] + recv[3] * 256
                        self.serialLidarInst.reset_input_buffer()
                        if distance < 0:
                            distance = 0
                        break

            except serial.SerialTimeoutException:  # timeout
                distance = -1
                break
            except IndexError:  # timeout
                distance = -1
                break

        return distance

    def serialLidarClose(self):
        self.serialLidarInst.close()

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
            print("Loading")
            try:
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
            except serial.SerialTimeoutException:
                print("수신 타임아웃")
            except IndexError:  # 수신된 데이터가 없는 경우
                pass

        return result

    def serialDebugPrint(self):  # 아두이노 측에서 보내는 시리얼 받기
        if self.serialInst.readable():
            res = self.serialInst.readline()
            print(res.decode()[:len(res) - 1])
            self.serialInst.flush()

    def serialClose(self):  # 시리얼 객체 해제
        if self.serialInst is not None:
            self.serialInst.close()
            self.serialInst.__del__()
            self.serialInst = None

        if self.serialLidarInst is not None:
            self.serialLidarInst.close()
            self.serialLidarInst.__del__()
            self.serialLidarInst = None

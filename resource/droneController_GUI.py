import tkinter
import tkinter.font
import tkinter.messagebox as msg
from tkinter import *


class DroneController:

    def __init__(self, serial_ins):
        self.serial = serial_ins
        self.keyboardCharList = ['a', 'd', 'i', 'k', 'j', 'l']  # 키값 배열 생성
        self.keyboardBindEventSkipTriggerList = [1, 1, 1, 1, 1, 1]  # 키 반복 실행 방지 트리거 1 : 실행중이 아님, 0 : 실행중
        self.throttleScaleValue = 113  # 드론 시동걸때 스로틀 시작값을 113으로 지정함
        self.controllerAfterReturn = 0  # 프로그램 종료 분기 // 처음 시리얼 연결부터 진행하려면 -1, 프로그램을 종료하려면 0
        self.takeoffTrigger = 0
        self.emergencyTrigger = False

        '''GUI(tkinter) 객체 생성'''
        self.window = tkinter.Tk()
        self.window.title("드론 컨트롤")
        self.window.geometry("700x450")
        self.window.resizable(False, False)

        madeByName = tkinter.Label(self.window, text="Made By  대.영.선.순 Laboratory")  # 제작자 이름
        madeByName.place(x=0, y=0)

        self.distanceLabelF = Label(self.window, text="고도:", fg="#DDDDDD")
        self.distanceLabelF.place(x=275, y=70)
        self.distanceLabelS = Label(self.window, text="", fg="#DDDDDD")
        self.distanceLabelS.place(x=310, y=70)
        self.distanceLabelT = Label(self.window, text="M", fg="#DDDDDD")
        self.distanceLabelT.place(x=344, y=70)

        '''맨 위 시동과 비행모드 버튼의 프레임 생성'''
        buttonFrame = tkinter.Frame(self.window)
        buttonFrame.pack(side="top", pady=30, padx=(40, 40))

        fontVar = tkinter.font.Font(family="맑은 고딕", size=13)

        self.startButton = Label(buttonFrame, text="시동", font=fontVar, padx=5, pady=3)
        self.startButton.pack(side="left", padx=20)

        self.flightmode = Label(buttonFrame, text="비행모드1", font=fontVar)
        self.flightmode.pack(side="left", padx=20)

        self.scriptsMode = Label(buttonFrame, text="(대기중)", font=fontVar)
        self.scriptsMode.pack(side="left", padx=20)

        self.takeoffStart = Button(buttonFrame, text="Takeoff", font=tkinter.font.Font(family="맑은 고딕", size=10), command=self.btnOnClick_Takeoff)
        self.takeoffStart.configure(state='disable') # 컴퓨터비전이 연결되어야 takeoff 활성
        self.btnColor = self.takeoffStart.cget("background")
        self.takeoffStart.pack(side="left", padx=10)

        self.emergencyStart = Button(buttonFrame, text="Emergency", font=tkinter.font.Font(family="맑은 고딕", size=10), command=self.btnOnClick_Emergency)
        self.emergencyStart.configure(state='disable') # takeoff가 실행되어야 emergency 활성
        self.emergencyStart.pack(side="left", padx=20)

        '''입력키 출력, 조종값 출력 프레임 설정'''
        # ! 수정 -> 가운데에 크게 프레임을 잡고 거기서 또 두 구역으로 나누면 좋을 것 같음
        middleFrame = tkinter.Frame(self.window, width=610, height=300)
        middleFrame.pack()
        middleFrame.pack_propagate(0)  # ! 자식의 위젯을 관리할 때 부모가 자식의 위젯 크기를 제어하도록 tkinter에 지시하는 함수

        '''왼쪽 압력키 표시창과 과거 입력키 기록 출력 프레임 생성'''
        showEntryFrame = tkinter.Frame(middleFrame, width=100)
        showEntryFrame.pack(side="left", fill="both", padx=(0, 30))
        showEntryFrame.pack_propagate(0)

        self.showEnterkey = Label(showEntryFrame, text="대기", font=tkinter.font.Font(family="맑은 고딕", size=40))
        self.showEnterkey.pack(side="top", pady=(70, 105))  # ! pady, padx는 양쪽에 같은 같은 값으로 적용이 되어 각각 적용하려면 저렇게 지시하면 된다.

        debugLogtitle = Label(showEntryFrame, text="메모장", font=tkinter.font.Font(family="맑은 고딕", size=13))
        debugLogtitle.pack(side="top")

        '''조종값 출력 프레임 생성'''
        showSliderFrame = tkinter.Frame(middleFrame)
        showSliderFrame.pack(side="right", pady=(0, 100), padx=(0, 20))

        '''스로틀 min: 113, mid: 188, max: 253'''
        throttleFrame = tkinter.Frame(showSliderFrame, width=300)
        throttleFrame.grid(row=0, column=0, pady=(0, 35), padx=15)

        throttleLabel = Label(throttleFrame, text="스로틀 값")
        throttleLabel.pack(pady=5)
        throttleVar = tkinter.IntVar()  # 각각의 값을 저장할 변수가 따로 필요하기 때문에 스로틀, 피치, 롤, 요의 변수를 따로 만들어 줌 -> 스크롤의 변화에 따른 값을 넣는 변수
        self.throttleScale = Scale(throttleFrame, variable=throttleVar, orient="horizontal", from_=113, to=253,
                                   resolution=1, length=190)  # orient = 수평, 수직 // resolution = 값 표시 여부
        self.throttleScale.configure(state='disable')  # 스로틀 바 값으로 프로세싱 되므로 버그를 막고자 스케일 바 잠금
        self.throttleScale.pack()

        '''피치'''
        pitchFrame = tkinter.Frame(showSliderFrame, width=100)
        pitchFrame.grid(row=0, column=1, pady=(0, 35), padx=(15, 0))

        pitchLabel = Label(pitchFrame, text="피치 값")
        pitchLabel.pack(pady=5)
        pitchVar = tkinter.IntVar()
        self.pitchScale = Scale(pitchFrame, variable=pitchVar, orient="horizontal", from_=113, to=253, resolution=1,
                                length=190)
        self.pitchScale.set(188)
        self.pitchScale.pack()

        '''롤'''
        rollFrame = tkinter.Frame(showSliderFrame, width=100)
        rollFrame.grid(row=1, column=0, pady=20, padx=15)

        rollLabel = Label(rollFrame, text="롤 값")
        rollLabel.pack(pady=5)
        rollVar = tkinter.IntVar()
        self.rollScale = Scale(rollFrame, variable=rollVar, orient="horizontal", from_=113, to=253, resolution=1,
                               length=190)
        self.rollScale.set(188)
        self.rollScale.pack()

        '''요'''
        yawFrame = tkinter.Frame(showSliderFrame, width=100)
        yawFrame.grid(row=1, column=1, pady=20, padx=(15, 0))

        yawLabel = Label(yawFrame, text="요 값")
        yawLabel.pack(pady=5)
        yawVar = tkinter.IntVar()
        self.yawScale = Scale(yawFrame, variable=yawVar, orient="horizontal", from_=113, to=253, resolution=1,
                              length=190)
        self.yawScale.set(188)
        self.yawScale.pack()

        ''' 메모 텍스트 박스 '''
        memoFrame = tkinter.Frame(self.window)
        memoFrame.place(x=190, y=325)
        scrollbar = tkinter.Scrollbar(memoFrame)
        scrollbar.pack(side="right", fill="y")
        memoTextBox = tkinter.Text(memoFrame, height=6, width=62, yscrollcommand=scrollbar.set)
        memoTextBox.pack(side="right")
        scrollbar.configure(command=memoTextBox.yview)

        # SerialBotton = Button(centerFrame, text="연결", font=tkinter.font.Font(family="맑은 고딕", size=10),
        #                           command=lambda: onClick_serial(window))  # command=onClick_serial)
        exitBtn = Button(self.window, text="연결 종료", font=tkinter.font.Font(family="맑은 고딕", size=10),
                         command=self.btnOnClick_Exit)
        exitBtn.place(x=620, y=10)

        self.window.protocol("WM_DELETE_WINDOW", self.btnOnClick_Exit)  # GUI 창 'X'를 눌러 종료했을 경우의 콜백함수 사용 코드

    def btnOnClick_Exit(self):
        msgBox = msg.askquestion("연결창으로 돌아가기", "시리얼 통신 연결창으로 돌아가시겠습니까?\n\n(아니요 누를 시 프로그램이 종료됩니다.)")

        if msgBox == 'yes':
            self.controllerAfterReturn = -1

        else:
            self.controllerAfterReturn = 0

        ''' debuging '''
        self.serial.serialClose()
        self.takeoffTrigger = -1
        self.window.destroy()

    def btnOnClick_Takeoff(self):
        self.takeoffTrigger = 1
        self.takeoffStart.configure(bg="#FFFF95")
        self.takeoffStart.configure(state='disable')
        self.emergencyStart.configure(state='normal')

    def btnOnClick_Emergency(self):
        self.emergencyTrigger = 1
        self.emergencyStart.configure(bg="red")
        self.emergencyStart.configure(state='disable')
        self.takeoffStart.configure(bg="#DDDDDD")


    def getSerialIns(self):
        return self.serial

    def startGUI(self):
        self.window.mainloop()
        return self.controllerAfterReturn

    def getThrottleScale(self):
        return self.throttleScale

    def getPitchScale(self):
        return self.pitchScale

    def getYawScale(self):
        return self.yawScale

    def getRollScale(self):
        return self.rollScale

    def getStartButton(self):
        return self.startButton

    def getFlightmode(self):
        return self.flightmode

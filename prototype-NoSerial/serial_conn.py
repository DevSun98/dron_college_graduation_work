import tkinter
import tkinter.font
import tkinter.messagebox as msg
from tkinter import *
import serialCOM


def serialCheckGUI():
    serialAfterReturn = 1  # 우선적으로 오류로 처리 즉, 정상처리가 안 이루어지면 정상적으로 진행이 안되도록 설정  실패: 1, 성공: 시리얼객체인스턴스값, 종료: 0

    '''debuging'''
    def btnOnClick_serial():
        nonlocal serialAfterReturn
        msg.showinfo("시리얼 통신", "아두이노 포트와 연결되었습니다.")
        serialAfterReturn = 1.5  # debug 임시 설정
        window.destroy()  # GUI 인터페이스 삭제: GUI무한루프 종료 및 tk 객체 소멸

    # def btnOnClick_serial():
    #     nonlocal serialAfterReturn  # serial인스턴스를 전역변수로 선언
    #     serial = serialCOM.SerialCOM()  # 시리얼 통신 처리 객체 생성
    #
    #     if serial.serialCreate(SerialEntry.get(), 9600):  # 시리얼 포트 연결
    #         print("message: Serial connecting Successful")
    #         result = serial.Ard_BeginningState()
    #         print("debug: Serial communication check completed")
    #
    #         if result == 1:  # 아두이노가 처음 시작한 상태인지, 설명) 소프트웨어 적으로 초기화 하는 것 보다 물리적으로 초기화 하는 것이 좋다고 생각하여 아두이노 초기화 버튼을 눌렀는지에 대한 검사진행
    #             msg.showinfo("시리얼 통신", "아두이노 포트와 연결되었습니다.")
    #             serialAfterReturn = serial
    #             window.destroy()  # GUI 인터페이스 삭제: GUI무한루프 종료 및 tk 객체 소멸
    #
    #         elif result == -1:
    #             msg.showwarning("알 수 없는 오류", "시스템 오류입니다\n다시 시도해 주세요")
    #             serialAfterReturn = 1  # 실패 -> 무시
    #
    #         else:
    #             msg.showwarning("아두이노 재부팅 요청", "이전 시스템에서 사용됐던 아두이노 입니다\n아두이노의 Reset 버튼을 누르고 다시 시도해 주세요")
    #             serialAfterReturn = 1  # 실패 -> 무시
    #
    #     else:
    #         msg.showwarning("시리얼 통신", "아두이노 포트 연결에 실패하였습니다\n다시 시도해 주세요")
    #         serialAfterReturn = 1  # 실패 -> 무시


    def s_btnOnClick_Exit():
        nonlocal serialAfterReturn
        serialAfterReturn = 0  # 종료
        window.destroy()

    '''GUI(tkinter) 객체 생성'''
    window = tkinter.Tk()
    window.title("드론 연결")
    window.geometry("300x200")
    window.resizable(False, False)

    '''첫 화면 라벨'''
    SerialLabel = Label(window, text="포트 입력", font=tkinter.font.Font(family="맑은 고딕", size=20), pady=20)
    SerialLabel.pack(side="top")

    '''포트 입력창과 버튼을 하나로 묶기 위해 새로운 프레임 생성'''
    centerFrame = tkinter.Frame(window)
    centerFrame.pack(side="top", pady=15)

    '''포트 입력 엔트리'''
    SerialEntry = Entry(centerFrame, width=12)
    SerialEntry.pack(side="left", padx=10)

    '''포트 입력 후 전송 버튼'''
    SerialBotton = Button(centerFrame, text="연결", font=tkinter.font.Font(family="맑은 고딕", size=10),
                          command=btnOnClick_serial)  # command=onClick_serial)
    SerialBotton.pack(side="left")

    window.protocol("WM_DELETE_WINDOW", s_btnOnClick_Exit)  # GUI 창 'X'를 눌러 종료했을 경우의 콜백함수 사용 코드
    window.mainloop()

    ''' Tip(1) .destroy()를 실행하면서 발생되는 절차 
            .mainloop()를 통해 GUI가 실행되면서 게시하게 된다.
            그리고 mainloop()에서 무한루프가 진행되어 더이상 코드가 진행되지 않고 지정한 TK 객체의 GUI 시스템이 계속해서 실행된다.
            다음으로 destroy()가 실행되면 mainloop() 함수가 종료되고 다음 코드로 넘어간다.'''

    return serialAfterReturn

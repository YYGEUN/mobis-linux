import sys
from PyQt5 import QtWidgets #위젯들을 포함하는 클래스 
from PyQt5 import uic     # ui파일을 사용하기 위한 함수
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading, time
import socket #socket module

maxSpeed = 230
accValue = 3
brkValue = 3
ntValue = 1

doExit = False
doAcc = False
doBrk = False
curSpeed = 0

client_socket = None

sockMode = True

def client(form):
    HOST = '192.168.0.36' # loopback
    PORT = 9999
    global client_socket
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    bConnected = False
    while doExit == False:
        try:
            print("접속 시도")
            client_socket.connect((HOST, PORT))
            bConnected = True
            break
        except:
            print("exception socket.error")

    if bConnected == False:
        print("접속 실패 TH2 종료")
        return
    else:
        print("접속 완료")
        
    
    form.setMsg("server 접속 완료", True)

    msg = "conn_ui\x00"
    client_socket.send(msg.encode())
    
    while doExit == False:
        try:
            data = client_socket.recv(6)
            speed = data.decode()            
            print(data, speed, int(speed))
            form.setSpeedTarget(int(speed))
        except:
            print("except socket")
            break
            
    client_socket.close()
    print("TH2 종료")
    
def calcSpeed(form):
    global doAcc
    global doBrk
    global curSpeed
    while doExit == False:
        time.sleep(0.1)
        preSpeed = curSpeed
        if doAcc == True:
            if curSpeed < maxSpeed:
                curSpeed += accValue
        elif doBrk == True:
            if curSpeed > 0:
                curSpeed -= brkValue
        else:
            if curSpeed > 0:
                curSpeed -= ntValue
                
        if curSpeed < 0:
            curSpeed = 0
            
        if curSpeed > maxSpeed:
            curSpeed = maxSpeed
            
        if preSpeed != curSpeed:
            form.setSpeedTarget(curSpeed)
    
    print("TH1 종료")
    
class Form(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("cluster.ui", self)
        self.pixmap = QPixmap('back.png')
        self.pixmap = self.pixmap.scaledToWidth(300)
                
        self.rotatevalue = 0
        self.rotatetarget = 0
        self.timerPaint = QTimer(self)
        self.timerPaint.timeout.connect(self.update)
        self.timerPaint.start(30) # Only one timer is needed
        self.timerCalc = QTimer(self)
        self.timerCalc.timeout.connect(self.calcRotate)
        self.timerCalc.start(30) # Only one timer is needed
        self.ui.msg.setText("Turn ON 버튼을 눌러주세요.")
        self.ui.accel.setEnabled(False)
        self.ui.brake.setEnabled(False)

    def signalSet(self):        
        self.ui.system.clicked.connect(self.systembtn)
        self.ui.accel.pressed.connect(self.accelp)
        self.ui.accel.released.connect(self.accelr)
        self.ui.brake.pressed.connect(self.brakep)
        self.ui.brake.released.connect(self.braker)

    def calcRotate(self):
        if self.rotatevalue < self.rotatetarget:
            self.rotatevalue += 1;
        elif self.rotatevalue > self.rotatetarget:
            self.rotatevalue -= 1;

        if self.rotatevalue < 0:
            self.rotatevalue = 0
            
        if self.rotatevalue > maxSpeed:
            self.rotatevalue = maxSpeed
            
        self.ui.lcdNumber.display(self.rotatevalue)

    def setSpeedTarget(self, value):
        self.rotatetarget = value
        
    def setMsg(self, value, append):
        if append == True:
            self.ui.msg.setText(self.ui.msg.text() + "," + value)
        else:
            self.ui.msg.setText(value)
        
    def paintEvent(self, event):       
        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(0, 0, self.pixmap)
        qp.save()        
        qp.setPen(QPen(QColor(0, 0, 255), 3)) 
        qp.translate(150, 150)
        qp.rotate(self.rotatevalue - 200)
        qp.drawLine(QPoint(100, 0), QPoint(0, 0)) 
        qp.restore()
        qp.end()
        
    def showForm(self):
        self.ui.show()
        print("show")
        
    def systembtn(self):
        global client_socket
        print("systembtn clicked")
        if self.sender().isChecked() == True:
            self.ui.msg.setText("운행 시작.")
            self.ui.accel.setEnabled(True)
            self.ui.brake.setEnabled(True)
            msg = "turn_on\x00"
            client_socket.send(msg.encode())
            
        else:
            self.ui.msg.setText("운행 종료.")
            self.ui.accel.setEnabled(False)
            self.ui.brake.setEnabled(False)
            self.rotatetarget = 0
            msg = "turn_off\x00"
            client_socket.send(msg.encode())
        
    def accelp(self):
        print("accel on")
        if sockMode == True:
            msg = "acc_on\x00"
            client_socket.send(msg.encode())
        else :
            global doAcc
            doAcc = True
        
    def brakep(self):
        print("brake on")
        if sockMode == True:
            msg = "brk_on\x00"
            client_socket.send(msg.encode())
        else :
            global doBrk
            doBrk = True
        
    def accelr(self):
        print("accel off")
        if sockMode == True:
            msg = "acc_off\x00"
            client_socket.send(msg.encode())
        else :
            global doAcc
            doAcc = False
    def braker(self):
        print("brake off")
        if sockMode == True:
            msg = "brk_off\x00"
            client_socket.send(msg.encode())
        else :
            global doBrk
            doBrk = False

if __name__ == '__main__': 
    
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QtWidgets.QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = Form()
    myWindow.signalSet()
    myWindow.showForm()
    
    t1 = threading.Thread(target=calcSpeed, args=(myWindow,))
    t1.start()
    t2 = threading.Thread(target=client, args=(myWindow,))
    t2.start()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    print("종료")
    doExit = True

from PyQt5 import QtWidgets, uic, QtGui
import os
import sys
import time


def run(cmd):
    c = os.popen(cmd)
    return c.read()

def log():
    settings = run('warp-cli settings')
    status = run('warp-cli status')
    account = run('warp-cli account')
    return account + settings + status


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        self.setWindowIcon(QtGui.QIcon('./icons/logo.png'))
        self.conbtn = self.findChild(QtWidgets.QPushButton, 'con')
        self.label = self.findChild(QtWidgets.QLabel, 'status')
        self.pic = self.findChild(QtWidgets.QLabel, 'pic')
        self.dns = self.findChild(QtWidgets.QRadioButton, 'dns')
        self.warp = self.findChild(QtWidgets.QRadioButton, 'warp')
        self.status3 = self.findChild(QtWidgets.QLabel, 'status3')
        self.logging = self.findChild(QtWidgets.QPlainTextEdit, 'log')
        self.pic.setPixmap(QtGui.QPixmap(("./icons/online.png")))

        self.conbtn.clicked.connect(self.connect)
        self.dns.toggled.connect(self.setdns)
        self.warp.toggled.connect(self.setwarp)
        self.logging.setPlainText(log())


        #############
        s = run("warp-cli status")
        s = s.split("\n")[0]
        s = s.split(" ")
        s = s[2]
        self.label.setText(s)
        if s != "Connected":
            self.conbtn.setText("Connect")
            self.pic.setPixmap(QtGui.QPixmap("./icons/offline.png"))
            self.status3.setText("Disconnected")
            self.conbtn.show()
            self.label.setStyleSheet("color:red")
            self.label.setText("not private")
        else:
            self.conbtn.setText("Disconnect")
            self.pic.setPixmap(QtGui.QPixmap("./icons/online.png"))
            self.conbtn.show()
            self.label.setStyleSheet("color:#00b400")
            self.status3.setText("Connected")
            self.label.setText("private")
        s = run("warp-cli settings")
        s = s.split("\n")
        s = s[3]
        s = s.split(" ")
        s = s[1]
        if s == "Warp":
            self.warp.setChecked(True)
            self.dns.setChecked(False)
        else:
            self.warp.setChecked(False)
            self.dns.setChecked(True)
        self.show()
    ######################

    def setdns(self):
        if self.dns.isChecked():
            run("warp-cli set-mode doh")

    def setwarp(self):
        if self.warp.isChecked():
            run("warp-cli set-mode warp")



    def warpon(self):
        try:
            s = run("warp-cli status")
            s = s.split("\n")[0]
            s = s.split(" ")
            s = s[2]
            self.label.setText(s)
            if s == "Connected":
                return True
            else:
                return False
        except Exception as e:
            print(e)





    def connect(self):
        on = self.warpon()
        if on:
            p = run("warp-cli disconnect")
            time.sleep(0.1)
            if p == "Success\n":
                self.conbtn.setText("Connect")
                self.pic.setPixmap(QtGui.QPixmap("./icons/offline.png"))
                self.conbtn.show()
                self.label.setStyleSheet("color:red")
                self.status3.setText("Disconnected")
                self.label.setText("not private")
                self.logging.setPlainText(log())
            else:
                self.logging.setPlainText(p)
        elif not on:
            p = run("warp-cli connect")
            time.sleep(0.5)
            if p == "Success\n":
                self.conbtn.setText("Disconnect")
                self.pic.setPixmap(QtGui.QPixmap("./icons/online.png"))
                self.conbtn.show()
                self.label.setStyleSheet("color:#00b400")
                self.status3.setText("Connected")
                self.status3.setStyleSheet("color:green")
                self.label.setText("private")
                self.logging.setPlainText(log())
            else:
                self.logging.setPlainText(p)







app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

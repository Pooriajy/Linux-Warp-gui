from PyQt5 import QtWidgets, uic, QtGui
import os
import sys



def run(cmd):
    c = os.popen(cmd)
    return c.read()



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
        self.pic.setPixmap(QtGui.QPixmap(("./icons/online.png")))
        self.conbtn.clicked.connect(self.connect)
        self.dns.toggled.connect(self.setdns)
        self.warp.toggled.connect(self.setwarp)



        #############
        s = run("warp-cli status")
        s = s.split("\n")[0]
        s = s.split(" ")
        s = s[2]
        self.label.setText(s)
        if s != "Connected":
            self.conbtn.setText("Connect")
            self.pic.setPixmap(QtGui.QPixmap("./icons/offline.png"))
            self.conbtn.show()
            self.label.setStyleSheet("color:red")
            self.label.setText("not private")
        else:
            self.conbtn.setText("Disconnect")
            self.pic.setPixmap(QtGui.QPixmap("./icons/online.png"))
            self.conbtn.show()
            self.label.setStyleSheet("color:green")
            self.label.setText("private")

        self.show()

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
            if p == "Success\n":
                self.conbtn.setText("Connect")
                self.pic.setPixmap(QtGui.QPixmap("./icons/offline.png"))
                self.conbtn.show()
                self.label.setStyleSheet("color:red")
                self.label.setText("not private")
        elif not on:
            p = run("warp-cli connect")
            if p == "Success\n":
                self.conbtn.setText("Disconnect")
                self.pic.setPixmap(QtGui.QPixmap("./icons/online.png"))
                self.conbtn.show()
                self.label.setStyleSheet("color:green")
                self.label.setText("private")








app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random
import time
import threading

class Ui_MainWindow(QtWidgets.QMainWindow):
    def main(self):
        self.ctime = float(0)
        self.scramble = self.getscramble()
        global timerrun
        self.timerrun = False
        global start
        self.start = 0
        global defitem
        self.defitem = "ao5: 0.0 ; ao12: 0.0"
        global items
        self.items = []


        self.setupUi(self,self.scramble, self.ctime)
        self.pushButton_2.clicked.connect(self.setscramble)
        self.pushButton_3.clicked.connect(self.resettimes)
        self.pushButton.pressed.connect(self.startstoptimer)


    # Add new time to list
    def addtime(self,time):
        time = float(round(time, 1))  
        self.items.append(str(time))
        self.listWidget.clear()
        self.item = QtWidgets.QListWidgetItem()
        self.listWidget.addItems(list(self.items))


    # Reset times
    def resettimes(self):
        self.listWidget.clear()
        self.label_2.setText("ao5: 0.0 ao12: 0.0")
        self.lcdNumber.setProperty("value", "0.0")
        self.setscramble()
        self.items = []


    # Generate scramble
    def getscramble(self):
        self.turns = ["R","L","U","D","F","B"]
        self.lturn = str("")
        self.cturn = str("")
        self.scramble = []
        self.numturns = random.randint(14,18)
        for turn in range (0, self.numturns, +1):
            self.cturn = self.turns[random.randint(0,len(self.turns)-1)]
            while (self.lturn == self.cturn):
                self.cturn = self.turns[random.randint(0,len(self.turns)-1)]
            self.lturn = self.cturn
            if random.randint(0,12) == 0:
                self.cturn = self.cturn.casefold()
            if random.randint(0,2) == 0:
                self.cturn += "2"
            self.scramble.append(self.cturn)
        return (str(" ".join(self.scramble)))

    # Set average times
    def avgtimes(self):
        run = 0
        avg_tw = "0.0"
        avg_fi = "0.0"
        if len(self.items) > 11:
            ntimes = []
            for index in range (len(self.items)-12,len(self.items)-1,+1):
                ntimes.append(self.items[index])
            highest = 0
            lowest = 9999999
            for index in ntimes:
                index = float(index)
                if index > highest:
                    highest = index
                if index < lowest:
                    lowest = index
            ntimes.remove(str(lowest))
            ntimes.remove(str(highest))
            fnum = float(0)
            for index in ntimes:
                fnum += float(index)
            avg_tw = fnum/10
            avg_tw = float(round(avg_tw,1))
            avg_tw = str(avg_tw)
            run = 1
        if len(self.items) > 4:
            ntimes = []
            for index in range (len(self.items)-5,len(self.items)-1,+1):
                ntimes.append(self.items[index])
            highest = 0
            lowest = 9999999
            for index in ntimes:
                index = float(index)
                if index > highest:
                    highest = index
                if index < lowest:
                    lowest = index
            ntimes.remove(str(lowest))
            ntimes.remove(str(highest))
            fnum = float(0)
            for index in ntimes:
                fnum += float(index)
            avg_fi = fnum/3
            avg_fi = float(round(avg_fi,1))
            avg_fi = str(avg_fi)
            run = 1
        if run == 1:
            self.label_2.setText(f"ao5: {avg_fi} ao12: {avg_tw}")
        else:
            self.label_2.setText("ao5: 0.0 ao12: 0.0")

    # Set new random scramble
    def setscramble(self):
        self.scramble = self.getscramble()
        self.label.setText(self.scramble)

    # Thread that loops timer
    def timerloop(self):
        timer_thread = threading.Thread(target=self.settimer, name="Timer")
        timer_thread.start()

    # Set the timer to the current time
    def settimer(self):
        while self.timerrun == True:
            self.ctime = time.time() - self.start
            self.ctime = float(round(self.ctime, 1))            
            self.lcdNumber.setProperty("value", self.ctime)
            time.sleep(0.02)

    def startstoptimer(self):
        rstr = 0
        # Start button hit
        if (self.timerrun == False):
            self.start = time.time()
            run = "Stop"
            self.timerrun = True
            self.timerloop()
        # Stop button hit
        else:
            rstr = time.time() - self.start
            run = "Start"
            self.addtime(rstr)
            self.setscramble()
            self.avgtimes()
            self.timerrun = False
        self.pushButton.setText(run)

    def setupUi(self, MainWindow, scramble, ctime):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1136, 679)
        MainWindow.setMinimumSize(QtCore.QSize(1136, 679))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(60)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_5 = QtWidgets.QWidget(self.widget)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.listWidget = QtWidgets.QListWidget(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.verticalLayout_3.addWidget(self.listWidget)
        self.horizontalLayout_2.addWidget(self.widget_5)
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lcdNumber = QtWidgets.QLCDNumber(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
        self.lcdNumber.setSizePolicy(sizePolicy)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setProperty("value", 15.54684)
        self.lcdNumber.setProperty("value", ctime)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout_3.addWidget(self.lcdNumber)
        self.horizontalLayout_2.addWidget(self.widget_4)
        self.verticalLayout.addWidget(self.widget)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.widget_3)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.widget_3)
        MainWindow.setCentralWidget(self.centralwidget) 

        self.retranslateUi(MainWindow, scramble)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow, scramble):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Timer"))
        self.label.setText(_translate("MainWindow", scramble))
        self.label_2.setText(_translate("MainWindow", "ao5: 0.0 ao12: 0.0"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton_3.setText(_translate("MainWindow", "Reset"))
        self.pushButton_2.setText(_translate("MainWindow", "New scramble"))
        self.pushButton.setText(_translate("MainWindow", "Start"))

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.main()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = Ui_MainWindow()
    form.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

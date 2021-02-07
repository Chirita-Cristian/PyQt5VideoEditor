import time
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import QImage
import cv2, imutils
from numpy.ma.bench import timer


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(536, 571)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.horizontalLayout.addWidget(self.verticalSlider)
        self.verticalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.horizontalLayout.addWidget(self.verticalSlider_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_2.addWidget(self.playButton)
        self.pauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout_2.addWidget(self.pauseButton)
        self.fastForward = QtWidgets.QPushButton(self.centralwidget)
        self.fastForward.setObjectName("fastForward")
        self.horizontalLayout_2.addWidget(self.fastForward)
        self.fastBackward = QtWidgets.QPushButton(self.centralwidget)
        self.fastBackward.setObjectName("fastBackward")
        self.horizontalLayout_2.addWidget(self.fastBackward)
        self.writeText = QtWidgets.QPushButton(self.centralwidget)
        self.writeText.setObjectName("writeText")
        self.horizontalLayout_2.addWidget(self.writeText)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.videoSlider = QtWidgets.QSlider(self.centralwidget)
        self.videoSlider.setOrientation(QtCore.Qt.Horizontal)
        self.videoSlider.setObjectName("videoSlider")
        self.horizontalLayout_4.addWidget(self.videoSlider)
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.videoSlider.valueChanged['int'].connect(self.sliderFrame)
        self.verticalSlider.valueChanged['int'].connect(self.brightness_value)
        self.verticalSlider_2.valueChanged['int'].connect(self.blur_value)
        self.pushButton_2.clicked.connect(self.loadVideo)
        self.pushButton.clicked.connect(self.saveVideo)
        self.fastForward.clicked.connect(self.fastForwardVideo)
        self.fastBackward.clicked.connect(self.fastBackwardVideo)
        self.playButton.clicked.connect(self.playVideo)
        self.pauseButton.clicked.connect(self.pauseVideo)
        self.writeText.clicked.connect(self.writeOnFrames)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Added code here
        self.filename = None  # Will hold the video address location
        self.tmp = None  # Will hold the temporary image for display
        self.brightness_value_now = 0  # Updated brightness value
        self.blur_value_now = 0  # Updated blur value

    def loadVideo(self):
        self.filename = QFileDialog.getOpenFileName(filter="AVI(*.avi);;MOV(*.mov);;MP4(*.mp4)")[0]
        self.capture = cv2.VideoCapture(self.filename)
        ret, self.frame = self.capture.read()
        self.maximumSlider = self.capture.get(7)
        self.videoSlider.setMaximum(int(self.maximumSlider))
        self.setPhoto(self.frame)
        self.writenImage = [False] * int(self.capture.get(7))

    def playVideo(self):
        fps = self.capture.get(cv2.CAP_PROP_FPS)
        interval =int(500/fps)
        self.play = True
        ret = True
        frame_index = self.capture.get(cv2.CAP_PROP_FRAME_COUNT) -1
        if(int(self.capture.get(1))==int(self.capture.get(7))):
            self.capture.set(1,1)
        while (self.play and ret and frame_index>=0):
            try:
                # Capture frame-by-frame
                ret, self.frame = self.capture.read()
                # Our operations on the frame come here
                # Display the resulting frame
                self.videoSlider.blockSignals(True)
                self.videoSlider.setValue(int(self.capture.get(1)))
                self.videoSlider.blockSignals(False)
                if self.writenImage[int(self.capture.get(1))]:
                    cv2.putText(self.frame, self.text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)
                self.setPhoto(self.frame)
                self.update()
                last_frame = self.frame
                if cv2.waitKey(interval) & 0xFF == ord('q'):
                    break
            except:
                self.play = False
                self.frame = last_frame

    def pauseVideo(self):
        self.play = False
        self.playFF = False
        self.playFB = False

    def writeOnFrames(self):
        self.textWindow = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.textWindow)
        if(self.textWindow.exec() == QtWidgets.QDialog.Accepted):
            self.text = self.ui.textEdit.toPlainText()
            self.start = int(self.ui.spinBox.text())
            self.end = int(self.ui.spinBox_2.text())
            print(self.text)
            print(self.start)
            print(self.end)
            writeframe = self.start
            while writeframe >= self.start and writeframe<=self.end:
                self.writenImage[writeframe]= True
                writeframe +=1

    def fastForwardVideo(self):
        fps = self.capture.get(cv2.CAP_PROP_FPS)
        interval = int(100 /fps)
        self.playFF = True
        ret = True
        if (int(self.capture.get(1)) == int(self.capture.get(7))):
            self.capture.set(1, 1)
        frame_index = self.capture.get(cv2.CAP_PROP_FRAME_COUNT) - 1
        while (self.playFF and ret and frame_index >= 0):
            try:
                # Capture frame-by-frame
                ret, self.frame = self.capture.read()
                # Our operations on the frame come here
                # Display the resulting frame
                self.videoSlider.blockSignals(True)
                self.videoSlider.setValue(int(self.capture.get(1)))
                self.videoSlider.blockSignals(False)
                if self.writenImage[int(self.capture.get(1))]:
                    cv2.putText(self.frame, self.text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                                cv2.LINE_4)
                self.setPhoto(self.frame)
                last_frame = self.frame
                if cv2.waitKey(interval) & 0xFF == ord('q'):
                    break
            except:
                self.play = False
                self.frame = last_frame
    def fastBackwardVideo(self):
        fps = self.capture.get(cv2.CAP_PROP_FPS)
        interval = int(100 /fps)
        self.play = True
        ret = True
        frame_index = self.capture.get(1) - 1
        while (self.play and ret and frame_index >= 0):
            try:
                # Capture frame-by-frame
                self.capture.set(1,frame_index)
                ret, self.frame = self.capture.read()
                # Our operations on the frame come here
                # Display the resulting frame
                self.videoSlider.blockSignals(True)
                self.videoSlider.setValue(int(self.capture.get(1)))
                frame_index -=1
                self.videoSlider.blockSignals(False)
                if self.writenImage[int(self.capture.get(1))]:
                    cv2.putText(self.frame, self.text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                                cv2.LINE_4)
                self.setPhoto(self.frame)
                last_frame = self.frame
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except:
                self.play = False
                self.frame = last_frame
    def setPhoto(self, image):
        self.tmp = image
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
    def sliderFrame(self,value):
        self.play = False
        self.sliderFrame = value
        print(value)
        if(self.sliderFrame<self.maximumSlider):
            self.capture.set(1,value)
            ret, self.frame = self.capture.read()
            self.setPhoto(self.frame)
            last_frame = self.frame
    def brightness_value(self, value):
        self.brightness_value_now = value
        print('Brightness: ', value)
        self.update()

    def blur_value(self, value):
        self.blur_value_now = value
        print('Blur: ', value)
        self.update()

    def changeBrightness(self, img, value):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def changeBlur(self, img, value):
        kernel_size = (value + 1, value + 1)  # +1 is to avoid 0
        img = cv2.blur(img, kernel_size)
        return img

    def update(self):
        img = self.changeBrightness(self.frame, self.brightness_value_now)
        img = self.changeBlur(img, self.blur_value_now)
        self.setPhoto(img)

    def saveVideo(self):
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        filename = QFileDialog.getSaveFileName(filter="AVI(*.avi);;MOV(*.mov);;MP4(*.mp4)")[0]
        if(not filename):
            return
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))
        ret = True
        self.capture.set(1,0)
        frame= 0
        while (ret and frame < self.maximumSlider-2):
            ret, saveframe = self.capture.read()
            if(ret):
                frame = int(self.capture.get(1))
                saveframe = filters(saveframe,self.blur_value_now,self.brightness_value_now)
                if self.writenImage[frame]:
                    cv2.putText(saveframe, self.text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,cv2.LINE_4)
                out.write(saveframe)
                cv2.imshow("out",saveframe)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cv2.destroyAllWindows()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MiniVideo editor"))
        self.pushButton_2.setText(_translate("MainWindow", "Open"))
        self.pushButton.setText(_translate("MainWindow", "Save"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.pauseButton.setText(_translate("MainWindow", "Pause"))
        self.fastBackward.setText(_translate("MainWindow", "Backward"))
        self.fastForward.setText(_translate("MainWindow", "Forward"))
        self.writeText.setText(_translate("MainWindow", "Write"))






def filters(img, valueBlur, valueBrightness):
    kernel_size = (valueBlur + 1, valueBlur + 1)  # +1 is to avoid 0
    img = cv2.blur(img, kernel_size)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - valueBrightness
    v[v > lim] = 255
    v[v <= lim] += valueBrightness
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(530, 288)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(170, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 501, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_2.addWidget(self.spinBox, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_2.setMaximum(99999)
        self.spinBox.setMaximum(99999)
        self.gridLayout_2.addWidget(self.spinBox_2, 3, 1, 1, 1)
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_3.setText(_translate("Dialog", "End Fame"))
        self.label.setText(_translate("Dialog", "Write Text"))
        self.label_2.setText(_translate("Dialog", "Start Frame"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

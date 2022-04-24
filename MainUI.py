# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUI2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class MainUI_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1178, 788)
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(170, 610, 261, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(90, 600, 71, 41))
        self.spinBox.setObjectName("spinBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(510, 80, 512, 512))
        self.label.setMinimumSize(QtCore.QSize(512, 512))
        self.label.setMaximumSize(QtCore.QSize(512, 512))
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(720, 620, 83, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(820, 620, 83, 28))
        self.pushButton_2.setObjectName("pushButton2")
        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(80, 165, 100, 28))
        self.pushButton_7.setObjectName("pushButton7")  
        self.verticalSlider = QtWidgets.QSlider(Dialog)
        self.verticalSlider.setGeometry(QtCore.QRect(1060, 100, 22, 491))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.spinBox_2 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_2.setGeometry(QtCore.QRect(1060, 600, 51, 41))
        self.spinBox_2.setObjectName("spinBox_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 610, 58, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(1040, 80, 58, 15))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(70, 210, 391, 381))
        self.label_5.setMinimumSize(QtCore.QSize(256, 256))
        self.label_5.setMaximumSize(QtCore.QSize(512, 512))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Dialog)
        self.horizontalSlider.valueChanged['int'].connect(self.spinBox.setValue)
        self.verticalSlider.valueChanged['int'].connect(self.spinBox_2.setValue)
        self.spinBox.valueChanged['int'].connect(self.horizontalSlider.setValue)
        self.spinBox_2.valueChanged['int'].connect(self.verticalSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Liver Segment Version 1.0", "Liver Segment Version 1.0"))
        Dialog.setWindowIcon(QtGui.QIcon('Image/icon.jpg'))
        #Dialog.setWindowOpacity(0.9) # 設定視窗透明度 
        #Dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 設定視窗背景透明 
        #Dialog.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 隱藏邊框
        self.label.setText(_translate("Dialog", "DicomLabel"))
        self.pushButton.setText(_translate("Dialog", "Segment"))
        self.pushButton_2.setText(_translate("Dialog", "Multi"))
        self.pushButton_7.setText(_translate("Dialog", "Import"))
        self.pushButton_7.setObjectName("btn_chooseMutiFile")  
        self.label_2.setText(_translate("Dialog", "No."))
        self.label_3.setText(_translate("Dialog", "Threshold"))
        self.label_5.setText(_translate("Dialog", "OriginalLabel"))
        
    def slot_btn_chooseMutiFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File",
                self.xmlPath, "XML files (*.xml);;HTML files (*.html);;"
                "SVG files (*.svg);;User Interface files (*.ui)")

        if filePath:
            f = QFile(filePath)
            if f.open(QIODevice.ReadOnly):
                document = QDomDocument()
                if document.setContent(f):
                    newModel = DomModel(document, self)
                    self.view.setModel(newModel)
                    self.model = newModel
                    self.xmlPath = filePath

                f.close() 

class Multi_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1294, 767)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 60, 261, 291))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(390, 60, 261, 291))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(660, 60, 261, 291))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(930, 60, 261, 291))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(120, 390, 261, 291))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(390, 390, 261, 291))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(660, 390, 261, 291))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(930, 390, 261, 291))
        self.label_8.setObjectName("label_8")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(110, 40, 83, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(390, 40, 83, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_3.setGeometry(QtCore.QRect(660, 40, 83, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_4.setGeometry(QtCore.QRect(940, 40, 83, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_5.setGeometry(QtCore.QRect(110, 360, 83, 16))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_6.setGeometry(QtCore.QRect(390, 360, 83, 16))
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_7 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_7.setGeometry(QtCore.QRect(670, 360, 83, 16))
        self.radioButton_7.setObjectName("radioButton_7")
        self.radioButton_8 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_8.setGeometry(QtCore.QRect(950, 360, 83, 16))
        self.radioButton_8.setObjectName("radioButton_8")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(560, 710, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 710, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Image Processing ..."))
        self.label_2.setText(_translate("Dialog", "Image Processing ..."))
        self.label_3.setText(_translate("Dialog", "Image Processing ..."))
        self.label_4.setText(_translate("Dialog", "Image Processing ..."))
        self.label_5.setText(_translate("Dialog", "Image Processing ..."))
        self.label_6.setText(_translate("Dialog", "Image Processing ..."))
        self.label_7.setText(_translate("Dialog", "Image Processing ..."))
        self.label_8.setText(_translate("Dialog", "Image Processing ..."))
        self.radioButton.setText(_translate("Dialog", "RadioButton"))
        self.radioButton_2.setText(_translate("Dialog", "RadioButton"))
        self.radioButton_3.setText(_translate("Dialog", "RadioButton"))
        self.radioButton_4.setText(_translate("Dialog", "RadioButton"))
        self.radioButton_5.setText(_translate("Dialog", "RadioButton"))
        self.radioButton_6.setText(_translate("Dialog", "RadioButton"))
        self.radioButton_7.setText(_translate("Dialog", "RadioButton"))
        self.radioButton_8.setText(_translate("Dialog", "RadioButton"))
        self.pushButton.setText(_translate("Dialog", "Confirm"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))

class Reveal_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(512, 512)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 512, 512))
        self.label.setObjectName("label")
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Image Processing ..."))
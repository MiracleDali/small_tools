# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QStatusBar,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(703, 419)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formLayout = QFormLayout(self.centralwidget)
        self.formLayout.setObjectName(u"formLayout")
        self.textEdit_3 = QTextEdit(self.centralwidget)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setStyleSheet(u"QTextEdit {\n"
"    border: 1px solid #282c34;  /* \u84dd\u8272\u8fb9\u6846 */\n"
"    border-radius: 5px;         /* \u5706\u89d2 */\n"
"}")
        self.textEdit_3.setReadOnly(True)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.textEdit_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QSize(16777215, 35))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    /*background-color: #282c34;  /* \u80cc\u666f\u8272 */\n"
"    color: black;               /* \u5b57\u4f53\u989c\u8272 */\n"
"    border: 1px solid #282c34;  /* \u8fb9\u6846 */\n"
"    border-radius: 5px;         /* \u5706\u89d2 */\n"
"}\n"
"\n"
"QPushButton:hover { \n"
"    /*background-color: #3b414d;  /* \u9f20\u6807\u60ac\u505c\u65f6\u7684\u80cc\u666f\u8272 */\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #e5e5e5;  /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u8272 */\n"
"}")
        self.pushButton.setIconSize(QSize(21, 21))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeatDelay(300)

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMaximumSize(QSize(16777215, 35))
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    /*background-color: #282c34;  /* \u80cc\u666f\u8272 */\n"
"    color: black;               /* \u5b57\u4f53\u989c\u8272 */\n"
"    border: 1px solid #282c34;  /* \u8fb9\u6846 */\n"
"    border-radius: 5px;         /* \u5706\u89d2 */\n"
"}\n"
"\n"
"QPushButton:hover { \n"
"    /*background-color: #3b414d;  /* \u9f20\u6807\u60ac\u505c\u65f6\u7684\u80cc\u666f\u8272 */\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #e5e5e5;  /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u8272 */\n"
"}")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.WeatherShowers))
        self.pushButton_2.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.formLayout.setLayout(3, QFormLayout.SpanningRole, self.horizontalLayout_3)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(500, 150))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.lineEdit_2 = QLineEdit(self.frame)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(430, 110, 132, 20))
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.textEdit_2 = QTextEdit(self.frame)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(430, 21, 240, 81))
        self.radioButton_2 = QRadioButton(self.frame)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(345, 21, 79, 20))
        sizePolicy.setHeightForWidth(self.radioButton_2.sizePolicy().hasHeightForWidth())
        self.radioButton_2.setSizePolicy(sizePolicy)
        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(99, 21, 240, 81))
        self.textEdit.setStyleSheet(u"")
        self.radioButton = QRadioButton(self.frame)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(21, 21, 59, 20))
        sizePolicy.setHeightForWidth(self.radioButton.sizePolicy().hasHeightForWidth())
        self.radioButton.setSizePolicy(sizePolicy)
        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(345, 110, 72, 16))
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(99, 110, 132, 20))
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(21, 110, 72, 16))
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 703, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00   \u59cb", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u4fdd   \u5b58", None))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u65f6\u95f4\uff1a", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"MONKEY", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"MTBF", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u5f00\u59cb\u65f6\u95f4", None))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u65f6\u95f4\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u5f00\u59cb\u65f6\u95f4", None))
    # retranslateUi


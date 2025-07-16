from PySide6.QtCore import QThread, Signal, QMutex
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QComboBox,QLabel,QSpinBox, QGridLayout,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout,QCheckBox)
import pyautogui
from datetime import datetime
import time
import os
import random
from configparser import RawConfigParser


path = os.path.dirname(__file__)
app_start_file_path = os.path.join(path, 'app_path.ini')

def read_config(app_path):
    config = RawConfigParser()
    config.read(app_path, encoding='utf-8')
    return config['app启动路径']

# def write_config(app_path, app_path_dict):
#     config = RawConfigParser()
#     config.add_section('app启动路径')
#     for key, value in app_path_dict.items():
#         config.set('app启动路径', key, value)
#     with open(app_path, 'w') as f:
#         config.write(f)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 获取应用的启动程序路径
        start_path = read_config(app_start_file_path)

        # 设置窗口标题
        self.setWindowTitle("看!!!打工人来了")

        # 创建垂直布局
        v_layout = QVBoxLayout()

        # 创建标签
        self.label = QLabel('选择你要运行的程序')
        self.label.setStyleSheet("""
            QLabel {
                border: 1px solid gray;
                border-radius: 1px;
                padding: 2px;
                background-color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)

        # 添加标签到垂直布局
        v_layout.addWidget(self.label)


        # creation grid layout
        grid = QGridLayout()

        # 设置需要启动的应用选项
        self.open_music = QCheckBox('Open Music')
        self.open_music.setChecked(True)
        grid.addWidget(self.open_music, 0, 0)

        self.music_path = QLineEdit()
        self.music_path.setText(os.path.join(start_path['music']))
        grid.addWidget(self.music_path, 0, 1)

        self.open_idea = QCheckBox('open_idea')
        self.open_idea.setChecked(True)
        grid.addWidget(self.open_idea, 1, 0)

        self.open_idea = QLineEdit()
        self.open_idea.setText(os.path.join(start_path['open_idea']))
        grid.addWidget(self.open_idea, 1, 1)

        # 绑容定网格布局到垂直布局中
        v_layout.addLayout(grid)


        # 创建水平布局
        h_layout = QHBoxLayout()

        self.start_button = QPushButton('开始')
        # self.start_button.clicked.connect(self.start)
        h_layout.addWidget(self.start_button)

        self.pause_button = QPushButton('结束')
        # self.pause_button.clicked.connect(self.pause)
        h_layout.addWidget(self.pause_button)

        self.save_change_button = QPushButton('保存更改')
        # self.save_change_button.clicked.connect(self.reset)
        h_layout.addWidget(self.save_change_button)

        # 将水平布局添加到垂直布局
        v_layout.addLayout(h_layout)

        # 创建文本框_用于显示输出
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText('--> 按照提示输入网址和时间'
                                            '\n--> 输入时间(0-23)，用英文逗号分隔，如：16,21,6'
                                            '\n--> 默认每次执行时间间隔范围为 8-16分钟 不定时')
        v_layout.addWidget(self.output_text)


        # 创建容器
        container = QWidget()
        # 将垂直布局添加到容器中
        container.setLayout(v_layout)
        # 设置窗口的容器
        self.setCentralWidget(container)





if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
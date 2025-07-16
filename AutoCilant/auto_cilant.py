from PySide6.QtCore import QThread, Signal, QMutex
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QComboBox,QLabel,QSpinBox, QGridLayout,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout,QCheckBox)
import pyautogui
from datetime import datetime
import time
import os
import random


path = os.path.dirname(__file__)
photo_path = os.path.join(path, 'photo')



class WorkerThread(QThread):
    # 使用 Pyside6.QtCore.Signal 创建信号,用于向主线程发送消息
    message_signal = Signal(str)

    def __init__(self,
                 music: bool=None,
                 play_music: bool=None,
                 idea: bool=None,
                 translate: bool=None,
                 browser: bool=None,
                 ) -> None:
        super().__init__()
        self.music = music
        self.play_music = play_music
        self.idea = idea
        self.translate = translate
        self.browser = browser

        self.mutex = QMutex()
        self.is_running = True

    def back_home(self):
        """ 返回桌面 """
        self.message_signal.emit('即将返回桌面')
        time.sleep(2)
        self.mutex.lock()
        running = self.is_running
        self.mutex.unlock()
        if not running:
            return
        self.message_signal.emit('win + d 组合键被按下')
        pyautogui.hotkey('win', 'd')

    def is_exist(self, image_path):
        """ 判断图标是否存在并返回坐标值 """
        try:
            # 获取图片坐标
            coordinates = pyautogui.locateOnScreen(
                image_path,
                minSearchTime=2,
                confidence=0.97,
                grayscale=True
            )

            if coordinates:
                # 将 Box 转换为标准元组并确保使用 Python 原生 int
                box_tuple = (
                    int(coordinates.left),
                    int(coordinates.top),
                    int(coordinates.width),
                    int(coordinates.height)
                )
                return box_tuple
        except pyautogui.ImageNotFoundException as e:
            self.message_signal.emit(f'{e}')

    def open_software(self, picture_path, click):
        self.mutex.lock()
        running = self.is_running
        self.mutex.unlock()
        if not running:
            return

        try:
            pos_x_y = self.is_exist(picture_path)
            pyautogui.moveTo(pos_x_y, duration=0.2)
            pyautogui.click(clicks=click, interval=0.2)
            time.sleep(2)
            xx = random.randint(0, 1000)
            yy = random.randint(0, 1000)
            pyautogui.moveTo(x=xx, y=yy, duration=0.2)

        except Exception as e:
            self.message_signal.emit(f"[ERROR]: {e}")

    def run(self):
        """ 执行工作线程 """
        self.mutex.lock()
        running = self.is_running
        self.mutex.unlock()
        if not running:
            return

        self.back_home()

        if self.idea:
            self.message_signal.emit(f'正在打开idea')
            time.sleep(2)
            self.open_software(os.path.join(photo_path, 'idea.png'), 2)
            time.sleep(2)

        self.back_home()

        if self.translate:
            self.message_signal.emit(f'正在打开翻译软件')
            time.sleep(2)
            self.open_software(os.path.join(photo_path, 'translate.png'), 2)

        self.back_home()

        if self.browser:
            self.message_signal.emit(f'正在打开浏览器')
            time.sleep(2)
            self.open_software(os.path.join(photo_path, 'browser.png'), 2)

        self.back_home()

        if self.music:
            self.message_signal.emit(f'正在打开音乐软件')
            time.sleep(2)
            self.open_software(os.path.join(photo_path, 'Music.png'), 2)

        if self.play_music:
            self.message_signal.emit(f'准备播放音乐')
            time.sleep(6)
            self.open_software(os.path.join(photo_path, 'MusicPlay.png'), 1)
            time.sleep(2)



        self.mutex.lock()
        running = self.is_running
        self.mutex.unlock()
        if not running:
            return


        self.mutex.lock()
        running = self.is_running
        self.mutex.unlock()
        if not running:
            return

        self.message_signal.emit("任务完成")

    def stop(self):
        self.mutex.lock()
        self.is_running = False
        self.mutex.unlock()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle('看!!! 牛马来了')

        # 创建垂直布局
        v_layout = QVBoxLayout()

        self.label = QLabel("选择你要运行的程序和网页")
        self.label.setStyleSheet(""" 
            QLabel {
                border: 1px solid gray;
                border-radius: 1px;
                padding: 2px;
                background-color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        v_layout.addWidget(self.label)


        # 创建网格布局 -- 用来设置打开的应用和网页
        grid = QGridLayout()

        # 设置多选框 --
        self.open_music = QCheckBox('Open Music')
        self.open_music.setChecked(True)
        grid.addWidget(self.open_music, 0, 0)

        self.play_videos = QCheckBox('Paly')
        self.play_videos.setChecked(True)
        grid.addWidget(self.play_videos, 0, 1)

        self.open_idea = QCheckBox('Open idea')
        self.open_idea.setChecked(True)
        grid.addWidget(self.open_idea, 1, 0)

        self.open_browser = QCheckBox('Open Browser')
        self.open_browser.setChecked(True)
        grid.addWidget(self.open_browser, 2, 0)

        self.gitee = QCheckBox('Gitee')
        # self.gitee.setChecked(True)
        grid.addWidget(self.gitee, 2, 1)

        self.deepseek = QCheckBox('DS')
        # self.deepseek.setChecked(True)
        grid.addWidget(self.deepseek, 2, 2)

        self.nami = QCheckBox('NM')
        # self.nami.setChecked(True)
        grid.addWidget(self.nami, 2, 3)

        self.translate = QCheckBox('Translate')
        self.translate.setChecked(True)
        grid.addWidget(self.translate, 3, 0)

        # 绑定网格布局到容器
        grid_container = QWidget()
        grid_container.setLayout(grid)
        # 将网格布局添加到主布局 垂直布局
        v_layout.addWidget(grid_container)

        # 创建水平布局
        h_layout = QHBoxLayout()

        self.start_button = QPushButton('开始')
        self.start_button.clicked.connect(self.start)
        h_layout.addWidget(self.start_button)

        self.pause_button = QPushButton('结束')
        self.pause_button.clicked.connect(self.pause)
        h_layout.addWidget(self.pause_button)

        self.reset_button = QPushButton('清空输出')
        self.reset_button.clicked.connect(self.reset)
        h_layout.addWidget(self.reset_button)

        # 绑定布局到容器 -- 水平布局
        h_container = QWidget()
        h_container.setLayout(h_layout)

        # 将水平布局的控件添加到垂直布局
        v_layout.addWidget(h_container)

        # 创建文本框_用于显示输出
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText('--> 按照提示输入网址和时间'
                                            '\n--> 输入时间(0-23)，用英文逗号分隔，如：16,21,6'
                                            '\n--> 默认每次执行时间间隔范围为 8-16分钟 不定时')
        v_layout.addWidget(self.output_text)

        # 绑定布局到容器
        container = QWidget()
        container.setLayout(v_layout)
        self.setCentralWidget(container)

        # 创建成员变量，用来保持worker——thread线程
        self.worker_thread = None


    def start(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():

            music = self.open_music.isChecked()
            if music:
                self.output_text.append('# --> 待执行任务：打开音乐软件')
            play_music = self.play_videos.isChecked()
            if play_music:
                self.output_text.append('# --> 待执行任务：播放最近歌曲')
            idea = self.open_idea.isChecked()
            if idea:
                self.output_text.append('# --> 待执行任务：打开idea')
            translate = self.translate.isChecked()
            if translate:
                self.output_text.append('# --> 待执行任务：打开翻译软件翻译')
            browser = self.open_browser
            if browser.isChecked():
                self.output_text.append('# --> 待执行任务：打开浏览器')


            # 如果一个也没有选中的话会触发下面的条件
            if not music and not play_music and not idea and not browser and not translate:
                self.output_text.append('# --> 牛马: 快选择你要干的活')
            else:
                self.output_text.append('')
                self.output_text.append('# --> 牛马: 开始工作吧')

                self.worker_thread = WorkerThread(music, play_music, idea, translate, browser)
                self.worker_thread.message_signal.connect(self.update_output)
                self.worker_thread.start()

    def pause(self):
        if self.worker_thread is None:
            self.output_text.append('[WARNING]: 请先开始任务！！！')
            return

        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.output_text.append('[INFO]: 终止任务')

    def reset(self):
        self.output_text.clear()

    def update_output(self, message):
        self.output_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


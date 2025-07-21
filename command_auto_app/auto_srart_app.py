import subprocess
from PySide6.QtCore import QThread, Signal, QMutex
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QGridLayout,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout,QCheckBox)
import time
import os
from configparser import RawConfigParser


path = os.path.dirname(__file__)
app_config_file_path = os.path.join(path, 'app_path.ini')

def read_config(app_paths):
    """
    读取software的路径以供打开软件使用
    """
    config = RawConfigParser()
    config.read(app_paths, encoding='utf-8')
    return config


class WorkerThread(QThread):
    # 使用 pyside6.QrCore.Signal 创建线程 用于向主线程发送信号
    message_signal = Signal(str)

    def __init__(self, music_path=None, idea_path=None, translate_path=None):
        super().__init__()
        self.mutex = QMutex()
        self.is_running = True

        self.music_path = music_path
        self.idea_path = idea_path
        self.translate_path = translate_path



    def start_app(self, app_path, app_name):
        try:
            subprocess.Popen(app_path)
            self.message_signal.emit(f"{app_name}启动成功")
        except Exception as e:
            self.message_signal.emit(f"Error: {e},{app_name}路径是否正确: {app_path}")


    def run(self):
        """ 执行工作线程 """
        self.mutex.lock()
        running = self.is_running
        self.mutex.unlock()
        if not running:
            return

        if self.music_path:
            self.message_signal.emit(f'正在打开 music')
            self.start_app(self.music_path, "music")

        for _ in range(3):
            self.mutex.lock()
            running = self.is_running
            self.mutex.unlock()
            if not running:
                return
            time.sleep(1)

        if self.idea_path:
            self.message_signal.emit(f'正在打开 idea')
            self.start_app(self.idea_path, "idea")

        for _ in range(3):
            self.mutex.lock()
            running = self.is_running
            self.mutex.unlock()
            if not running:
                return
            time.sleep(1)

        if self.translate_path:
            self.message_signal.emit(f'正在打开 translate')
            self.start_app(self.translate_path, "translate")

        self.message_signal.emit(f'软件打开完成!!!')

    def stop(self):
        self.mutex.lock()
        self.is_running = False
        self.mutex.unlock()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 获取应用的启动程序路径和是否打开的default
        start_path = read_config(app_config_file_path)['app启动路径']
        default_status = read_config(app_config_file_path)['app是否默认启动']


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
        self.open_music.setChecked(True if default_status['music'] == 'True' else False)
        grid.addWidget(self.open_music, 0, 0)

        self.music_path = QLineEdit()
        self.music_path.setText(os.path.join(start_path['music']))
        grid.addWidget(self.music_path, 0, 1)

        self.open_idea = QCheckBox('open_idea')
        self.open_idea.setChecked(True if default_status['idea'] == 'True' else False)
        grid.addWidget(self.open_idea, 1, 0)

        self.idea_path  = QLineEdit()
        self.idea_path.setText(os.path.join(start_path['idea']))
        grid.addWidget(self.idea_path, 1, 1)

        self.open_translate = QCheckBox('open_translate')
        self.open_translate.setChecked(True if default_status['translate'] == 'True' else False)
        grid.addWidget(self.open_translate, 2, 0)

        self.translate_path = QLineEdit()
        self.translate_path.setText(os.path.join(start_path['translate']))
        grid.addWidget(self.translate_path, 2, 1)

        self.open_translate = QCheckBox('open_browse')
        self.open_translate.setChecked(True if default_status['browse'] == 'True' else False)
        grid.addWidget(self.open_translate, 3, 0)

        self.translate_path = QLineEdit()
        self.translate_path.setText(os.path.join(start_path['browse']))
        grid.addWidget(self.translate_path, 3, 1)

        # 绑容定网格布局到垂直布局中
        v_layout.addLayout(grid)


        # 创建水平布局
        h_layout = QHBoxLayout()

        self.start_button = QPushButton('开始')
        self.start_button.clicked.connect(self.start)
        h_layout.addWidget(self.start_button)

        self.pause_button = QPushButton('结束')
        self.pause_button.clicked.connect(self.pause)
        h_layout.addWidget(self.pause_button)

        self.save_change_button = QPushButton('保存更改')
        self.save_change_button.clicked.connect(self.save_change)
        h_layout.addWidget(self.save_change_button)

        # 将水平布局添加到垂直布局
        v_layout.addLayout(h_layout)

        # 创建文本框_用于显示输出
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText('--> 勾选需要启动的应用，该配置可保存'
                                            '\n--> 输入文件所在位置的正确路径'
                                            '\n--> 配置在保存后方可生效')
        v_layout.addWidget(self.output_text)


        # 创建容器
        container = QWidget()
        # 将垂直布局添加到容器中
        container.setLayout(v_layout)
        # 设置窗口的容器
        self.setCentralWidget(container)

        # 创建变量，用来保持 worker_thread 工作线程
        self.worker_thread = None

    def start(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():

            music_path = None
            if self.open_music.isChecked():
                self.output_text.append('# --> 待执行任务：打开音乐软件')
                music_path = self.music_path.text()

            idea_path = None
            if self.open_idea.isChecked():
                self.output_text.append('# --> 待执行任务：打开编译器')
                idea_path = self.idea_path.text()

            translate_path = None
            if self.open_translate.isChecked():
                self.output_text.append('# --> 待执行任务：打开翻译软件')
                translate_path = self.translate_path.text()


            if not music_path and not idea_path and not translate_path:
                self.output_text.append('# --> 错误：请选择要启动的程序')
                return
            else:
                self.worker_thread = WorkerThread(music_path, idea_path, translate_path)
                self.worker_thread.message_signal.connect(self.update_output)
                self.worker_thread.start()

    def pause(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():
            self.output_text.append('当前无任务运行！！！')
            return

        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.output_text.append('任务已经停止！！！')


    def write_config_path(self, name, app_path):
        """
        对修改的路径进行更改并保存到ini配置文件
        """
        config = RawConfigParser()
        config.read(app_config_file_path, encoding='utf-8')
        # 修改配置软件启动路径
        config.set('app启动路径', name, app_path)
        # 写入ini文件
        with open(app_config_file_path, 'w', encoding='utf-8') as f:
            config.write(f)
        self.output_text.append(f'软件：{name}, 路径{app_path}：保存成功')

    def write_config_default(self, name, default):
        """
        修改app是否默认开启或关闭
        """
        config = RawConfigParser()
        config.read(app_config_file_path, encoding='utf-8')
        config.set('app是否默认启动', name, default)
        with open(app_config_file_path, 'w', encoding='utf-8') as f:
            config.write(f)
        self.output_text.append(f'软件：{name}, 状态保存成功--{default}')

    def save_change(self):

        app_paths= {
                    'music': self.music_path.text(),
                    'idea': self.idea_path.text(),
                    'translate': self.translate_path.text()
                    }

        for key, value in app_paths.items():
            self.write_config_path(key, value)

        start_or_close = {
            'music': self.open_music.isChecked(),
            'idea': self.open_idea.isChecked(),
            'translate': self.open_translate.isChecked()
        }

        for key, value in start_or_close.items():
            self.write_config_default(key, value)


    def update_output(self, message):
        self.output_text.append(message)






if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

from PySide6.QtCore import QThread, Signal, QMutex
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QComboBox,QLabel,QSpinBox,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout)
from playwright.sync_api import sync_playwright
from datetime import datetime
import random
import time
import os



class WorkerThread(QThread):
    # 使用 Pyside6.QtCore.Signal 创建信号,用于向主线程发送消息
    message_signal = Signal(str)

    def __init__(self, url_list=None, hours_list=None, interval_1: int= None, interval_2: int=None):
        super().__init__()
        self.url = url_list if url_list else []
        self.hours = hours_list if hours_list else []

        self.interval_1 = interval_1
        self.interval_2 = interval_2

        self.mutex = QMutex()
        self.is_running = True


    def web_refresh(self):
        self.mutex.lock()
        running = self.is_running
        self.mutex.unlock()

        if not running:
            return

        try:
            with sync_playwright() as p:

                self.message_signal.emit(f"[INFO]: 启动浏览器")
                browser = p.chromium.launch(headless=False, slow_mo=1000)
                page = browser.new_page()

                self.message_signal.emit(f"[INFO]: 打开网页: {self.url[0]}")
                page.goto(self.url[0])
                page.wait_for_timeout(2000)

                for _ in range(3):
                    self.mutex.lock()
                    running = self.is_running
                    self.mutex.unlock()
                    if not running:
                        return
                    time.sleep(1)

                self.message_signal.emit(f"[INFO]: 刷新页面")
                page.reload()
                page.wait_for_timeout(2000)

                # 输入时间信息
                self.message_signal.emit(f"[INFO]: 输入搜索关键字")
                page.fill('input[class="s_ipt"]', f"TEST")
                time.sleep(2)

                # 点击回车
                self.message_signal.emit(f"[INFO]: 点击回车进入搜索内容页面")
                page.keyboard.press("Enter")
                page.wait_for_timeout(2000)
                time.sleep(2)

                for _ in range(2):
                    self.mutex.lock()
                    running = self.is_running
                    self.mutex.unlock()
                    if not running:
                        return
                    time.sleep(1)

                # 截图
                screenshot_path = os.path.join(os.getcwd(), f"screen_{datetime.now().strftime('%H_%M_%S')}.png")
                page.screenshot(path=screenshot_path, full_page=True)
                self.message_signal.emit(f"已保存截图到: {screenshot_path}")

                self.message_signal.emit(f"[INFO]: 刷新页面")
                page.reload()
                page.wait_for_timeout(2000)

                for _ in range(2):
                    self.mutex.lock()
                    running = self.is_running
                    self.mutex.unlock()
                    if not running:
                        return
                    time.sleep(1)

                self.message_signal.emit(f"[INFO]: 关闭浏览器")
                browser.close()
        except Exception as e:
            self.message_signal.emit(f"[ERROR]: {e}, {self.url}")


    def should_execute(self):
        current_hour = datetime.now().hour
        self.message_signal.emit(f"")
        self.message_signal.emit(f"#######################################")
        self.message_signal.emit(f"当前时间: {current_hour}点，允许执行时间: {self.hours}")
        return current_hour in self.hours

    def run(self):
        # 检查参数不能为空
        if len(self.url) == 0 or len(self.hours) == 0:
            return

        # 检查运行间隔时间1是否小于时间2
        if self.interval_1 >= self.interval_2:
            self.message_signal.emit(f"***时间间隔1应该小于时间间隔2，请检查！")
            return

        self.message_signal.emit(f"***待运行网址: {self.url}")
        self.message_signal.emit(f"***待运行时间: {self.hours}")
        self.message_signal.emit(f"***两次运行间隔时间范围: {self.interval_1}-{self.interval_2}")

        while True:
            self.mutex.lock()
            running = self.is_running
            self.mutex.unlock()
            if not running:
                break

            if self.should_execute():
                self.message_signal.emit(f"开始执行任务...")
                self.web_refresh()
            else:
                self.message_signal.emit(f"当前时间段不执行任务...")

            self.mutex.lock()
            running = self.is_running
            self.mutex.unlock()
            if not running:
                break

            random_time = random.randint(self.interval_1, self.interval_2)
            self.message_signal.emit(f"等待 {random_time} 分钟后再次检查...")

            for _ in range(random_time * 60):
                self.mutex.lock()
                running = self.is_running
                self.mutex.unlock()
                if not running:
                    break
                time.sleep(1)


            if not running:
                break


        self.message_signal.emit("任务已完全停止")

    def stop(self):
        self.mutex.lock()
        self.is_running = False
        self.mutex.unlock()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle('WuLin_vpn_Keep_Playwright')

        # 创建垂直布局
        v_layout = QVBoxLayout()

        # # 网址输入框
        # self.url_input = QLineEdit()
        # self.url_input.setPlaceholderText('请输入网址')
        # self.url_input.setText('https://www.baidu.com')
        # v_layout.addWidget(self.url_input)

        # 网址输入框
        self.url_input = QComboBox()
        self.url_input.setEditable(True)
        self.url_input.lineEdit().setPlaceholderText('请输入网址')
        # 添加历史网址记录
        self.url_input.addItems([
            "https://www.baidu.com",
            "https://www.bing.com"
        ])
        v_layout.addWidget(self.url_input)

        # 时间输入框
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("请输入时间(0-23)，用英文逗号分隔，如：16,21,6")
        self.time_input.setText('1,3,6,8,20,23')
        v_layout.addWidget(self.time_input)

        # 创建水平布局-不定时时长间隔
        h_layout_interval = QHBoxLayout()

        self.label = QLabel("间隔时长")
        self.label.setStyleSheet(""" 
            QLabel {
                border: 0.5px solid gray;
                border-radius: 5px;
                padding: 0.5px;
                background-color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        h_layout_interval.addWidget(self.label)

        self.time1_interval = QSpinBox()
        self.time1_interval.setRange(0, 29)
        self.time1_interval.setValue(8)
        h_layout_interval.addWidget(self.time1_interval)

        self.time2_interval = QSpinBox()
        self.time2_interval.setRange(0, 29)
        self.time2_interval.setValue(16)
        h_layout_interval.addWidget(self.time2_interval)

        h_layout_interval_container = QWidget()
        h_layout_interval_container.setLayout(h_layout_interval)

        v_layout.addWidget(h_layout_interval_container)

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

        # 绑定布局到容器
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

    def parse_url(self, url):
        """解析输入URL为字符串列表"""
        if not url:
            self.output_text.append('[WARNING]: 请输入URL！！！')
            return []
        url_s = [u for u in url.split(',')]
        return url_s

    def parse_hours(self, text):
        """解析输入时间为整数列表"""
        try:
            if not text:
                self.output_text.append('[WARNING]: 请输入时间！！！')
                return []
            hours_list = [int(h) for h in text.split(',')]
            return hours_list
        except ValueError as e:
            self.output_text.append(f'[WARNING]: 时间输入错误！！！ {e}')
            return []

    def start(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():

            url = self.url_input.lineEdit().text()
            url_list = self.parse_url(url)

            hours_text = self.time_input.text()
            hours_list = self.parse_hours(hours_text)

            time1 = int(self.time1_interval.text())
            time2 = int(self.time2_interval.text())

            self.worker_thread = WorkerThread(url_list, hours_list, time1, time2)
            self.worker_thread.message_signal.connect(self.update_output)
            self.worker_thread.start()

    def pause(self):
        if self.worker_thread is None:
            self.output_text.append('[WARNING]: 请先开始任务！！！')
            return

        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.output_text.append('[INFO]: 停止任务...')

    def reset(self):
        self.output_text.clear()

    def update_output(self, message):
        self.output_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


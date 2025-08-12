from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QThread, Signal, QMutex
from gui_get_mtbf_bug_info import GetBugInfo
from Ui_untitled import Ui_MainWindow
import yaml
import os

# 获取当前文件所在目录
base_path = os.path.dirname(__file__)
# print(base_path)

def read_yaml(file_path: str) -> dict:
    """
    读取yaml文件
    :param file_path: yaml文件地址
    :return: yaml文件内容 字典形式返回
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
        

class WorkerThread(QThread):
    """
    多线程类
    """
    message_signal = Signal(str)

    def __init__(self, url, date, file_name):
        super().__init__()
        self.mutex = QMutex()
        self.is_running = True

        self.url = url
        self.date = date
        self.file_name = file_name

    
    def run(self):
        self.mutex.lock()
        self.message_signal.emit("开始执行任务...")
        self.mutex.unlock()

        try:
            self.message_signal.emit(f"{self.url}")
            self.message_signal.emit(f"{self.date}")
            self.message_signal.emit(f"{self.file_name}")

            # 直接替换 get_url 调用，让它用 message_signal.emit 输出
            gb = GetBugInfo(self.url, self.date, self.file_name, log_func=self.message_signal.emit)
            gb.main()

            self.message_signal.emit(f"任务完成！")

        except Exception as e:
            self.message_signal.emit(f"任务执行出错：{str(e)}")


        self.mutex.lock()
        self.is_running = False
        self.mutex.unlock()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 创建UI实例对象
        self.ui = Ui_MainWindow()
        # 设置ui
        self.ui.setupUi(self)
 
        # yaml文件路径 
        self.yaml_file_path = os.path.join(base_path, 'config.yaml')


        self.data = read_yaml(self.yaml_file_path)
        # 设置默认值
        self.ui.textEdit.setText('\n'.join(self.data['mtbf_url']))
        self.ui.lineEdit.setText(str(self.data['mtbf_time']))
        self.ui.textEdit_2.setText('\n'.join(self.data['monkey_url']))
        self.ui.lineEdit_2.setText(str(self.data['monkey_time']))

        # 点击开始
        self.ui.pushButton.clicked.connect(self.start)

        # 保存配置
        self.ui.pushButton_2.clicked.connect(self.config_write_yaml)

        # 创建变量，用来保持 worker_thread 工作线程
        self.worker_thread = None

    
    def start(self):
        """ 调用WorkerThread类,开始任务 """

        if self.worker_thread is None or not self.worker_thread.isRunning():
            # 执行 mbbf 任务
            if self.ui.radioButton.isChecked():
                self.worker_thread = WorkerThread(self.data['mtbf_url'], self.data['mtbf_time'], 'MTBF')
                self.worker_thread.message_signal.connect(self.add_output_massage)
                self.worker_thread.start()
            # 执行 monkey 任务
            elif self.ui.radioButton_2.isChecked():
                self.worker_thread = WorkerThread(self.data['monkey_url'], self.data['monkey_time'], 'Monkey')
                self.worker_thread.message_signal.connect(self.add_output_massage)
                self.worker_thread.start()
            else:
                self.add_output_massage('请选择测试类型[ MONKEY / MTBF ]')

        else:
            self.add_output_massage('任务正在执行中...请勿重复点击开始按钮')


    def config_write_yaml(self):
        """
        写入yaml文件
        """
        self.add_output_massage(f'')
        mtbf_url = self.ui.textEdit.toPlainText().split('\n')
        self.add_output_massage(f'当前MTBF结果地址为\n{mtbf_url}')
        monkey_url = self.ui.textEdit_2.toPlainText().split('\n')
        self.add_output_massage(f'当前Monkey结果地址为\n{monkey_url}')

        self.add_output_massage(f'')

        mtbf_time = self.ui.lineEdit.text()
        monkey_time = self.ui.lineEdit_2.text()

        if len(mtbf_time) != 14 or len(monkey_time) != 14:
            self.add_output_massage('时间格式错误! 请输入14位时间戳')
            self.add_output_massage('YYYYMMDDhhmmss')
            return
        
        self.add_output_massage(f'当前MTBF任务开始时间为: {mtbf_time}')
        self.add_output_massage(f'当前MonKey任务开始时间为: {monkey_time}')
        
        config = { 'mtbf_url': mtbf_url,
                'mtbf_time': int(mtbf_time),
                'monkey_url': monkey_url,
                'monkey_time': int(monkey_time)
                }
        # print(config)

        with open(self.yaml_file_path, "w", encoding="utf-8") as f:
            yaml.dump(data=config, stream=f, allow_unicode=True)


        self.add_output_massage(f'')
        self.add_output_massage('配置保存成功！')

    def add_output_massage(self, message):
        """ 添加日志 """
        self.ui.textEdit_3.append(message)





if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

    # data = read_yaml(r'D:\1_172-25-193-21-GIT\mtbf_result_check\config.yaml')
    # print(data['mtbf_time'])
    # print(type(data['mtbf_time']))



    
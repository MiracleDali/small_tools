"""
获取mtbf测试期间bug的详细信息
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import tempfile
import argparse
import os
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

def get_result_url(func):
    def wrapper(*args, **kwargs):
        
        url_list = []
        ip, date = args
        result = func(*args, **kwargs)

        for url in result:
            # print(url)
            response = requests.get(url)
            response.raise_for_status()  # 检查HTTP响应
            soup = BeautifulSoup(response.text, 'html.parser')

            count = 1
            for row in soup.find_all('a'):
                if 'soc' in row.text:
                    row = url + '/' + row.get('href')[:-1]
                    day = row.split('/')[-1].split('_')[-3]
                    hour = row.split('/')[-1].split('_')[-2]
                    day_hour = day + hour
                    if int(day_hour) >= date:
                        print(count,'\t', row)
                        count += 1
                        url_list.append(row)

        return url_list
    return wrapper

# @get_result_url
def get_url(ip: list[str], date: int, log_func=None) -> list[str]:
    """
    获取MTBF运行结果的URL
    
    参数:
        ip: 包含基础URL的字符串列表 
        date: 日期阈值格式为YYYYMMDDHH的整数,例如2025081116
    
    返回:
        满足条件的结果URL列表 
    """
    url_list = []
    
    for base_url in ip:
        try:
            if log_func:
                log_func(f"获取到{base_url}的URL...")
            else:
                print(f"获取到{base_url}的URL...")
            response = requests.get(base_url) 
            response.raise_for_status()   # 检查HTTP错误 
            soup = BeautifulSoup(response.text,  'html.parser') 
 
            count = 1
            for row in soup.find_all('a'): 
                if 'soc' in row.text: 
                    full_url = f"{base_url}/{row.get('href')[:-1]}" 
                    parts = full_url.split('/')[-1].split('_') 
                    day_hour = parts[-3] + parts[-2]  # 组合日期和小时 
                    
                    if int(day_hour) >= date:
                        msg = f"{count}\t{full_url}"
                        if log_func: # 有回调就用回调
                            log_func(msg)
                        else: # 没有回调就用print
                            print(msg)
                        count += 1 
                        url_list.append(full_url) 
                        
        except requests.exceptions.RequestException  as e:
            print(f"请求失败: {base_url}, 错误: {e}")
    
    return url_list 

    # return [
    #     'http://172.25.193.45/report/spec/soc_logcat_monitor_Result_20250707_173104_919871217',
    #     'http://172.25.193.44/report/spec/soc_logcat_monitor_Result_20250707_173852_740093479',
    #     'http://172.25.193.17/report/spec/soc_logcat_monitor_Result_20250707_171558_202841948',
    #     'http://172.25.193.46/report/spec/soc_logcat_monitor_Result_20250707_173219_195943846'
    # ]

class BaseInfoCreate(object):
    """
    获取mtbf运行结果url和创建excel数据表
    """
    def __init__(self, ip: list[str], date: int, file_name: str, log_func):
        self.url = get_url(ip, date, log_func)
        self.file_name = file_name


    def create_excel(self) -> str:
        """
        创建存储bug信息的表格
        :return: excel表格的名字
        """
        if not os.path.exists("result_check"):
            os.makedirs("result_check")
            # print("创建文件夹成功succeed")

        data = ['Url', 'Date', 'Number', 'Package', 'ANR', 'ForceClose', 'Tombstone', 'WatchDog', 'Sum', 'Reboot']
        df = pd.DataFrame(columns=data)

        date = time.strftime('%Y%m%d%H%M', time.localtime())

        result_file = os.path.join("result_check", f"{self.file_name}_result_{date}.xlsx")
        df.to_excel(result_file, index=False, sheet_name='Sheet1')
        return result_file


class GetBugInfo(BaseInfoCreate):
    """
    bug信息进行落表操作
    """
    def __init__(self, ip: list[str], date: int, file_name: str, log_func):
        super().__init__(ip, date, file_name, log_func)
        self.log_func = log_func
        self.report_time = None
        self.reboot_row = None
        self.table = self.create_excel()

    def bug_info(self) -> list[list[str]]:
        """ 获取详细的bug信息 """
        table_data = []
        for url in self.url:

            if self.log_func:
                self.log_func(f"正在获取{url}的bug信息...")
            else:
                print(f"正在获取{url}的bug信息...")

            self.report_time = url.split('/')[-1].split('_')[-3]           # .split('_')[-3]
            # http://172.25.192.226/report/spec/soc_logcat_monitor_Result_20250610_174055_346806676

            response = requests.get(url)
            response.raise_for_status()  # 检查HTTP响应
            soup = BeautifulSoup(response.text, 'lxml')

            # 获取 reboot 次数
            for row in soup.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) > 0 and cells[0].text.strip() == 'Reboot':
                    self.reboot_row = row.text.strip().split('\n')[-1]
                    # print(self.reboot_row)

            # 获取所有tbody元素
            all_tbodies = soup.find_all('tbody')

            # 提取第二个tbody（索引为1）
            if len(all_tbodies) > 1:
                second_tbody = all_tbodies[1]

                # 提取表格数据
                for row in second_tbody.find_all('tr'):
                    row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
                    row_data = [url, self.report_time] + row_data + [self.reboot_row]
                    table_data.append(row_data)
            else:
                print(f"未找到第二个tbody, bug统计信息，{url}")

        if self.log_func: 
            self.log_func(f"所用bug信息获取完毕...")
        else: 
            print(f"所用bug信息获取完毕...")

        return table_data


    def write_excel_sheet1(self):
        """ 落表-->sheet1 """
        # 根据 def bug_info(self) 获取到的数据 """
        bug_info =pd.DataFrame(self.bug_info())
        # 读取上一步创建的excel，并完成数据合并
        table = pd.read_excel(self.table)
        bug_info.columns = table.columns
        table = pd.concat([table, bug_info], ignore_index=True)  # 垂直合并
        # 数据类型转换
        cols_to_convert = ['Date', 'Number', 'ANR', 'ForceClose', 'Tombstone', 'WatchDog', 'Sum']
        table[cols_to_convert] = table[cols_to_convert].astype(int)
        table.to_excel(self.table, index=False, sheet_name='Sheet1', engine='openpyxl')

    def write_excel_sheet2(self):
        """ 落表-->sheet2 -- 根据package进行重新排序"""
        sheet_1 = pd.read_excel(self.table, sheet_name='Sheet1')
        package_list = []
        for pk in sheet_1['Package'].unique():
            group_df = sheet_1[sheet_1['Package'] == pk].copy()
            group_df['Package_Group'] = pk
            package_list.append(group_df)

        # 合并列表内的多个dataframe
        combined_df = pd.concat(package_list, ignore_index=False)
        # 写入到excel——sheet2
        with pd.ExcelWriter(self.table, engine='openpyxl', mode='a') as writer:
            combined_df.to_excel(writer, sheet_name='Sheet2', index=False)

    def plot_excel(self):
        """ 绘制bug数量折线图 """
        file_path = self.table
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        # 按日期和包分组，统计问题总数
        grouped = df.groupby(['Date', 'Package'])['Sum'].sum().unstack()
        # 对比不同包的不同问题类型数量
        issue_types = ['ANR', 'ForceClose', 'Tombstone', 'WatchDog']
        package_issues = df.groupby('Package')[issue_types].sum()

        # 创建临时目录存放图片
        with tempfile.TemporaryDirectory() as tmpdir:
            # 绘制第一个图表：问题总数统计
            fig1 = plt.figure(figsize=(10, 6))
            ax1 = fig1.add_subplot(111)
            bars1 = grouped.plot(kind='bar', ax=ax1)
            plt.title('Total Issues per Package per Date')
            plt.xlabel('Date')
            plt.ylabel('Total Issues')
            plt.xticks(rotation=45)
            plt.legend(title='Package')
            plt.tight_layout()
            
            # 添加数据标签
            for container in bars1.containers:
                ax1.bar_label(container, fontsize=8)
            
            # 保存第一个图表到临时文件
            chart1_path = os.path.join(tmpdir, 'chart1.png')
            fig1.savefig(chart1_path, dpi=300, bbox_inches='tight')
            plt.close(fig1)
            
            # 绘制第二个图表：问题类型分布
            fig2 = plt.figure(figsize=(10, 6))
            ax2 = fig2.add_subplot(111)
            bars2 = package_issues.plot(kind='bar', stacked=True, ax=ax2)
            plt.title('Issue Types per Package')
            plt.xlabel('Package')
            plt.ylabel('Number of Issues')
            plt.xticks(rotation=45)
            plt.legend(title='Issue Type')
            plt.tight_layout()
            
            # 添加数据标签
            for container in bars2.containers:
                ax2.bar_label(container, fontsize=8)
            
            # 保存第二个图表到临时文件
            chart2_path = os.path.join(tmpdir, 'chart2.png')
            fig2.savefig(chart2_path, dpi=300, bbox_inches='tight')
            plt.close(fig2)
            
            # 使用openpyxl操作Excel
            wb = load_workbook(file_path)
            try:
                sheet1 = wb['Sheet1']
                sheet2 = wb['Sheet2']
            except KeyError as e:
                print(f"错误：{e}")
                print("请确保文件包含Sheet1和Sheet2工作表")
                return
            
            # 插入图表到Sheet1
            img1 = Image(chart1_path)
            img1.width = 800
            img1.height = 500
            sheet1.add_image(img1, 'M1')
            
            # 插入图表到Sheet2
            img2 = Image(chart2_path)
            img2.width = 800
            img2.height = 500
            sheet2.add_image(img2, 'O1')
            
            # 保存工作簿
            wb.save(file_path)

    def at_last_result(self):
        """ 统计每个进程在测试期间一共出现的问题 """
        sheet_2 = pd.read_excel(self.table, sheet_name='Sheet2')
        packages = sheet_2['Package'].unique()
        bug_collect = []

        for i in packages:
            single_package_info = sheet_2[sheet_2['Package'] == i]
            bug_total = (single_package_info['ANR'].sum() +
                         single_package_info['ForceClose'].sum() +
                         single_package_info['Tombstone'].sum() +
                         single_package_info['WatchDog'].sum())

            collect = pd.DataFrame({
                'Package': [i],
                'Bug_total': [bug_total],
                'ANR': [single_package_info['ANR'].sum()],
                'ForceClose': [single_package_info['ForceClose'].sum()],
                'Tombstone': [single_package_info['Tombstone'].sum()],
                'WatchDog': [single_package_info['WatchDog'].sum()],
                'url': [single_package_info['Url'].unique()]
            })
            bug_collect.append(collect)
        total = pd.concat(bug_collect, ignore_index=True)

        with pd.ExcelWriter(self.table, engine='openpyxl', mode='a') as writer:
            total.to_excel(writer, sheet_name='Sheet3', index=False)


    def main(self):
        self.write_excel_sheet1()
        self.write_excel_sheet2()
        self.at_last_result()
        self.plot_excel()
        # self.at_last_result()



arg = argparse.ArgumentParser()  # 创建一个解析器对象
arg.add_argument('-ip', '--ip_list',
                 nargs='+',
                 default=[
                          'http://172.25.193.45/report/spec/',
                          'http://172.25.193.44/report/spec/',
                          'http://172.25.193.17/report/spec/',
                          'http://172.25.193.46/report/spec/',
                          
                          # monkey ip
                        #   'http://172.25.192.226/report/spec/',
                        #   'http://172.25.192.128/report/spec/',
                          ],
                #  type=str,
                 help='ip地址, 如[http://172.25.192.226/report/spec]')

arg.add_argument('-d', '--date',
                 
                 default=20250804010101,

                #  default=20250808010101,

                 type=int,
                 help='测试开始时间,如[20250804010101]')

arg.add_argument('-n', '--name',
                 
                 default='mtbf',
                #  default='monkey',

                 type=str,
                 help='设置文件名')

if __name__ == '__main__':
    args = arg.parse_args()
    gb = GetBugInfo(args.ip_list, args.date, args.name, log_func=None)
    gb.main()

    # url_list = get_url(args.ip_list)
    # print(666, url_list)



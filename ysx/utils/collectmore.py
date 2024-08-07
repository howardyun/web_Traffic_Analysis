import subprocess
import os
import time
import pandas as pd
from selenium import webdriver
# website = 'http://www.baidu.com'
# website = 'https://www.sina.com.cn'
# website = 'https://bilibili.com'

saveUrl = '../try/'



if not os.path.exists(saveUrl):
    os.makedirs(saveUrl)


def start_capture(interface='WLAN', output_file=saveUrl + 'morecatch1.pcap'):
    """启动 tshark 捕获进程"""
    command = ['tshark', '-i', interface, '-f','tcp port 443','-w', output_file]
    process = subprocess.Popen(command)
    return process


def stop_capture(process):
    """停止 tshark 捕获进程"""
    process.terminate()
    process.wait()


def convert_pcap_to_json(pcap_file, json_file):
    """将 pcap 文件转换为 json 格式"""
    command = ['tshark', '-r', pcap_file, '-T', 'json']
    with open(json_file, 'w') as out_file:
        subprocess.run(command, stdout=out_file)


def main():
    print("Save URL:", saveUrl)

    dicwebsite_df = pd.read_csv('dicweb.csv', header=None, names=['Dicwebsite'])
    # 设置 ChromeDriver 和 Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # 开始捕获
    capture_process = start_capture()

    try:
        for index,row in dicwebsite_df.iterrows():
            dicewebsite = row ['Dicwebsite']
            website =f'http://{dicewebsite}'
            print(f"visiting : {website}")
            # 打开网页
            driver.get(website)
        # 假设留出一些时间让页面加载和数据捕获
            time.sleep(2)
    finally:
        # 结束捕获和关闭浏览器
        stop_capture(capture_process)
        driver.quit()

    # 转换捕获数据为 JSON
    convert_pcap_to_json(saveUrl + 'morecatch.pcap', saveUrl + 'morecatch.json')


if __name__ == '__main__':
    main()

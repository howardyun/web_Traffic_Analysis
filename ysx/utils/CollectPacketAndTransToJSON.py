import subprocess
import time
from selenium import webdriver

# website = 'http://www.baidu.com'
# website = 'https://www.sina.com.cn'
website = 'https://bilibili.com'

saveUrl = '../collectData/'


def start_capture(interface='en0', output_file=saveUrl + 'capture_bilibili.pcap'):
    """启动 tshark 捕获进程"""
    command = ['tshark', '-i', interface, '-f', 'tcp port 443', '-w', output_file]
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
    # 设置 ChromeDriver 和 Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # 开始捕获
    capture_process = start_capture()

    try:
        # 打开网页
        driver.get(website)
        # 假设留出一些时间让页面加载和数据捕获
        time.sleep(2)
    finally:
        # 结束捕获和关闭浏览器
        stop_capture(capture_process)
        driver.quit()

    # 转换捕获数据为 JSON
    convert_pcap_to_json(saveUrl + 'capture_bilibili.pcap', saveUrl + 'capture_bilibili.json')


if __name__ == '__main__':
    main()

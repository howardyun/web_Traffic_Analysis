import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
def start_tshark():
    # 指定Tshark的输出文件
    output_file = "DatawithTor/captured_traffic.pcap"
    # 启动Tshark进程，捕获特定端口的流量，这里假设使用的是Tor默认的9150端口
    tshark_cmd = [
        "tshark",
        "-i", "lo",  # lo是本地环回接口，也可能需要更改为您的网络接口，如 eth0
        "-f", "tcp port 9150",  # 仅捕获通过Tor端口的流量
        "-w", output_file
    ]
    return subprocess.Popen(tshark_cmd), output_file

def stop_tshark(tshark_process):
    tshark_process.terminate()
    tshark_process.wait()
    print("Tshark process has been stopped.")

# 设置 Firefox 以及 Tor 代理
options = Options()
options.headless = True  # 无头模式
options.set_preference("network.proxy.type", 1)
options.set_preference("network.proxy.socks", "127.0.0.1")
options.set_preference("network.proxy.socks_port", 9150)  # 确保端口与您的 Tor 配置匹配
options.set_preference("network.proxy.socks_remote_dns", True)

# 启动 Tshark
tshark_process, output_file = start_tshark()

driver = webdriver.Firefox(options=options)
try:
    # 这个是Tor测试的网站，可以看到Tor是否可以正常启用，我不确定之后是否每次都需要加上这个地方
    driver.get("https://check.torproject.org/")
    time.sleep(10)  # 延时以确保页面充分加载
    header = driver.find_element(By.TAG_NAME, "h1")
    if "Congratulations" in header.text:
        print("Tor is working correctly")
    else:
        print("Tor is not working")
finally:
    driver.quit()
    stop_tshark(tshark_process)
    print(f"Traffic data saved in {output_file}")


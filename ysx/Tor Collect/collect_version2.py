from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

# 设置 Firefox 选项
options = Options()
options.headless = True  # 使用无头模式，根据需要开启或关闭
options.set_preference("network.proxy.type", 1)
options.set_preference("network.proxy.socks", "127.0.0.1")
options.set_preference("network.proxy.socks_port", 9150)  # 确保端口与您的 Tor 配置匹配
options.set_preference("network.proxy.socks_remote_dns", True)

driver = webdriver.Firefox(options=options)

try:
    driver.get("https://check.torproject.org/")
    time.sleep(5)  # 等待页面加载
    # 检查 Tor 是否工作
    header = driver.find_element(By.TAG_NAME, "h1")
    if "Congratulations" in header.text:
        print("Tor is working correctly")
    else:
        print("Tor is not working")
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()

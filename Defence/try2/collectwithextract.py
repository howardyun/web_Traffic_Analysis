# import subprocess
# import os
# import time
# import pandas as pd
# from selenium import webdriver
# import socket
# import json
#
# saveDir_pcap = '../try2data/pcap/'
# saveDir_json = '../try2data/json/'
#
# if not os.path.exists(saveDir_pcap):
#     os.makedirs(saveDir_pcap)
#
# if not os.path.exists(saveDir_json):
#     os.makedirs(saveDir_json)
#
# def start_capture(interface='WLAN', output_file='', pcap_output_dir=''):
#     """启动 tshark 捕获进程"""
#     command = ['tshark', '-i', interface, '-f','tcp port 443','-w', os.path.join(pcap_output_dir, output_file)]
#     process = subprocess.Popen(command)
#     return process
#
# def stop_capture(process):
#     """停止 tshark 捕获进程"""
#     process.terminate()
#     process.wait()
#
# def convert_pcap_to_json(pcap_file, json_file, json_output_dir=''):
#     """将 pcap 文件转换为 json 格式"""
#     command = ['tshark', '-r', pcap_file, '-T', 'json']
#     with open(os.path.join(json_output_dir, json_file), 'w') as out_file:
#         subprocess.run(command, stdout=out_file)
#
# def catch(dicewebsite):
#     true_website = f'http://{dicewebsite}'
#     print("Save URL:", true_website)
#     # 设置 ChromeDriver 和 Selenium
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(options=options)
#
#
#     # 开始捕获
#     capture_process = start_capture(output_file=os.path.join(saveDir_pcap, f'{dicewebsite}_more.pcap'))
#
#     try:
#         # 打开网页
#         driver.get(true_website)
#         # 假设留出一些时间让页面加载和数据捕获
#         time.sleep(2)
#     finally:
#         # 结束捕获和关闭浏览器
#         stop_capture(capture_process)
#         driver.quit()
#
#     # 转换捕获数据为 JSON
#     convert_pcap_to_json(os.path.join(saveDir_pcap, f'{dicewebsite}_more.pcap'),  os.path.join(saveDir_json , f'{dicewebsite}_more.json'))
#
#
#
# def extract_packet_info(json_file):
#     """从 JSON 文件中提取每个数据包的详细信息，包括尽可能多的应用层协议类型"""
#     with open(json_file, 'r',encoding='utf-8') as file:
#         data = json.load(file)
#
#     packet_info_list = []
#
#     for packet in data:
#         try:
#             # 时间戳
#             timestamp = packet['_source']['layers']['frame']['frame.time_epoch']
#             # 数据包大小
#             packet_size = packet['_source']['layers']['frame']['frame.len']
#             # 源 IP 和目的 IP
#             src_ip = packet['_source']['layers']['ip']['ip.src']
#             dst_ip = packet['_source']['layers']['ip']['ip.dst']
#
#             # 传输层协议
#             protocol = packet['_source']['layers'].get('ip', {}).get('ip.proto', 'Unknown')
#
#             # 上层协议，如 TCP 或 UDP
#             if 'tcp' in packet['_source']['layers']:
#                 sub_protocol = 'TCP'
#             elif 'udp' in packet['_source']['layers']:
#                 sub_protocol = 'UDP'
#             else:
#                 sub_protocol = 'Unknown'
#
#             # 应用层协议检测
#             app_protocol = 'Unknown'
#             layer_keys = packet['_source']['layers'].keys()
#             if 'http' in layer_keys:
#                 app_protocol = 'HTTP'
#             elif 'tls' in layer_keys:
#                 app_protocol = 'TLS'
#             elif 'ftp' in layer_keys:
#                 app_protocol = 'FTP'
#             elif 'smtp' in layer_keys:
#                 app_protocol = 'SMTP'
#             elif 'dns' in layer_keys:
#                 app_protocol = 'DNS'
#             elif 'ssh' in layer_keys:
#                 app_protocol = 'SSH'
#             elif 'smb' in layer_keys or 'smb2' in layer_keys:
#                 app_protocol = 'SMB'
#             elif 'dhcp' in layer_keys:
#                 app_protocol = 'DHCP'
#             elif 'sip' in layer_keys:
#                 app_protocol = 'SIP'
#             elif 'rtsp' in layer_keys:
#                 app_protocol = 'RTSP'
#             elif 'icmp' in layer_keys:
#                 app_protocol = 'ICMP'
#             # 更多协议可以继续添加
#
#             packet_info_list.append({
#                 'timestamp': timestamp,
#                 'size': packet_size,
#                 'src_ip': src_ip,
#                 'dst_ip': dst_ip,
#                 'protocol': protocol,
#                 'sub_protocol': sub_protocol,
#                 'app_protocol': app_protocol
#             })
#         except KeyError as e:
#             print(f"Error processing packet: {e}")
#
#     return packet_info_list
#
# def get_local_ip():
#     # 创建一个 UDP 套接字
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         # 连接到一个外部 IP 地址，以便获取本地 IP 地址
#         s.connect(('8.8.8.8', 80))
#         local_ip = s.getsockname()[0]
#     except socket.error:
#         local_ip = '无法获取本地 IP 地址'
#     finally:
#         s.close()
#     return local_ip
#
# def main():
#     dicwebsite_df = pd.read_csv('dicwebmore.csv', header=None, names=['Dicwebsite'])
#
#     for index, row in dicwebsite_df.iterrows():
#         dicewebsite = row['Dicwebsite']
#         website = f'http://{dicewebsite}'
#         print(f"Visiting: {website}")
#         catch(dicewebsite)
#         local_ip = get_local_ip()
#         print("local ip:",local_ip)
#         packets = extract_packet_info(os.path.join(saveDir_json , f'{dicewebsite}_more.json')) # 传递完整的文件路径
#         for packet in packets:
#             if packet['src_ip'] == local_ip:
#                 print(f"+,{packet['size']}")
#             elif packet['dst_ip'] == local_ip:
#                 print(f"-,{packet['size']}")
#
#
# if __name__ == '__main__':
#     main()
import subprocess
import os
import time
import pandas as pd
from selenium import webdriver
import socket
import json
from datetime import datetime

saveDir_pcap = '../try2data/pcap/'
saveDir_json = '../try2data/json/'

if not os.path.exists(saveDir_pcap):
    os.makedirs(saveDir_pcap)

if not os.path.exists(saveDir_json):
    os.makedirs(saveDir_json)

def start_capture(interface='en0', output_file='', pcap_output_dir=''):
    """启动 tshark 捕获进程"""
    command = ['tshark', '-i', interface, '-f','tcp port 443','-w', os.path.join(pcap_output_dir, output_file)]
    process = subprocess.Popen(command)
    return process

def stop_capture(process):
    """停止 tshark 捕获进程"""
    process.terminate()
    process.wait()

def convert_pcap_to_json(pcap_file, json_file, json_output_dir=''):
    """将 pcap 文件转换为 json 格式"""
    command = ['tshark', '-r', pcap_file, '-T', 'json']
    with open(os.path.join(json_output_dir, json_file), 'w') as out_file:
        subprocess.run(command, stdout=out_file)

def catch(dicewebsite):
    true_website = f'https://{dicewebsite}'
    print("Save URL:", true_website)
    # 设置 ChromeDriver 和 Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # 记录开始时间戳
    start_time = datetime.now()
    print(f"Capture started at: {start_time}")

    # 开始捕获
    capture_process = start_capture(output_file=os.path.join(saveDir_pcap, f'{dicewebsite}_more.pcap'))

    try:
        # 打开网页
        driver.get(true_website)
        # 假设留出一些时间让页面加载和数据捕获
        time.sleep(2)
    finally:
        # 结束捕获和关闭浏览器
        stop_capture(capture_process)
        driver.quit()

    # 记录结束时间戳
    end_time = datetime.now()
    print(f"Capture ended at: {end_time}")

    # 转换捕获数据为 JSON
    convert_pcap_to_json(os.path.join(saveDir_pcap, f'{dicewebsite}_more.pcap'),  os.path.join(saveDir_json , f'{dicewebsite}_more.json'))

    return start_time, end_time

def extract_packet_info(json_file):
    """从 JSON 文件中提取每个数据包的详细信息，包括尽可能多的应用层协议类型"""
    with open(json_file, 'r',encoding='utf-8') as file:
        data = json.load(file)

    packet_info_list = []

    for packet in data:
        try:
            # 时间戳
            timestamp = packet['_source']['layers']['frame']['frame.time_epoch']
            # 数据包大小
            packet_size = packet['_source']['layers']['frame']['frame.len']
            # 源 IP 和目的 IP
            src_ip = packet['_source']['layers']['ip']['ip.src']
            dst_ip = packet['_source']['layers']['ip']['ip.dst']

            # 传输层协议
            protocol = packet['_source']['layers'].get('ip', {}).get('ip.proto', 'Unknown')

            # 上层协议，如 TCP 或 UDP
            if 'tcp' in packet['_source']['layers']:
                sub_protocol = 'TCP'
            elif 'udp' in packet['_source']['layers']:
                sub_protocol = 'UDP'
            else:
                sub_protocol = 'Unknown'

            # 应用层协议检测
            app_protocol = 'Unknown'
            layer_keys = packet['_source']['layers'].keys()
            if 'http' in layer_keys:
                app_protocol = 'HTTP'
            elif 'tls' in layer_keys:
                app_protocol = 'TLS'
            elif 'ftp' in layer_keys:
                app_protocol = 'FTP'
            elif 'smtp' in layer_keys:
                app_protocol = 'SMTP'
            elif 'dns' in layer_keys:
                app_protocol = 'DNS'
            elif 'ssh' in layer_keys:
                app_protocol = 'SSH'
            elif 'smb' in layer_keys or 'smb2' in layer_keys:
                app_protocol = 'SMB'
            elif 'dhcp' in layer_keys:
                app_protocol = 'DHCP'
            elif 'sip' in layer_keys:
                app_protocol = 'SIP'
            elif 'rtsp' in layer_keys:
                app_protocol = 'RTSP'
            elif 'icmp' in layer_keys:
                app_protocol = 'ICMP'
            # 更多协议可以继续添加

            packet_info_list.append({
                'timestamp': timestamp,
                'size': packet_size,
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'protocol': protocol,
                'sub_protocol': sub_protocol,
                'app_protocol': app_protocol
            })
        except KeyError as e:
            print(f"Error processing packet: {e}")

    return packet_info_list

def get_local_ip():
    # 创建一个 UDP 套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到一个外部 IP 地址，以便获取本地 IP 地址
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except socket.error:
        local_ip = '无法获取本地 IP 地址'
    finally:
        s.close()
    return local_ip

def main():
    dicwebsite_df = pd.read_csv('../../ysx/dicwebmore.csv', header=None, names=['Dicwebsite'])
    i = 0
    for index, row in dicwebsite_df.iterrows():

        dicewebsite = row['Dicwebsite']
        website = f'https://{dicewebsite}'
        print(f"Visiting: {website}")
        start_time, end_time = catch(dicewebsite)
        local_ip = get_local_ip()
        print("local ip:",local_ip)
        packets = extract_packet_info(os.path.join(saveDir_json , f'{dicewebsite}_more.json')) # 传递完整的文件路径


        # for packet in packets:
        #     if packet['src_ip'] == local_ip:
        #         print(f"+,{packet['size']}")
        #     elif packet['dst_ip'] == local_ip:
        #         print(f"-,{packet['size']}")

        i = i+1

if __name__ == '__main__':
    main()

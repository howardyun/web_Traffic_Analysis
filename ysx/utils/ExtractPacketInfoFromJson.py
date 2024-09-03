import json

saveUrl = '../collectData/'

import json

import json


def extract_packet_info(json_file):
    """从 JSON 文件中提取每个数据包的详细信息，包括尽可能多的应用层协议类型"""
    with open(json_file, 'r') as file:
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


def main():
    packets = extract_packet_info(saveUrl + 'capture_bilibili.json')

    for packet in packets:
        print(f"Time: {packet['timestamp']}, Size: {packet['size']}, Src IP: {packet['src_ip']}, "
              f"Dst IP: {packet['dst_ip']}, Protocol: {packet['protocol']}, Sub-Protocol: {packet['sub_protocol']}, "
              f"App-Protocol: {packet['app_protocol']}")
    print(len(packets))


if __name__ == '__main__':
    main()

import socket
import concurrent.futures
import time
import requests
from urllib.parse import urlparse

def scan_port(ip, port, timeout=1.0):
    """尝试连接指定端口并返回详细结果"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            start_time = time.time()
            result = s.connect_ex((ip, port))
            elapsed = time.time() - start_time
            
            if result == 0:
                return port, "开放", elapsed
            else:
                return port, "关闭", elapsed
    except socket.timeout:
        return port, "超时", timeout
    except Exception as e:
        return port, f"错误: {str(e)}", 0

def check_http_service(ip, port, timeout=2.0):
    """检查端口是否运行HTTP服务"""
    try:
        url = f"http://{ip}:{port}"
        response = requests.get(url, timeout=timeout, allow_redirects=False)
        
        # 检查是否是HTTP服务
        if 200 <= response.status_code < 400:
            return True, response.status_code
        
        # 检查重定向
        if 300 <= response.status_code < 400:
            location = response.headers.get('Location', '')
            if location.startswith('http'):
                return True, f"重定向到: {location}"
    
    except requests.exceptions.RequestException as e:
        return False, f"HTTP错误: {str(e)}"
    
    return False, "无HTTP响应"

def main():
    target_ip = "202.192.143.133"
    start_port = 1
    end_port = 65535
    timeout = 1.0  # 连接超时时间（秒）
    max_workers = 100  # 最大并发线程数
    
    print(f"开始扫描 {target_ip} 的端口范围: {start_port}-{end_port}")
    print("正在实时扫描每个端口...")
    
    open_ports = []
    http_ports = []
    start_time = time.time()
    scanned_count = 0
    
    # 使用线程池加速扫描
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 创建所有端口的扫描任务
        futures = {executor.submit(scan_port, target_ip, port, timeout): port 
                  for port in range(start_port, end_port + 1)}
        
        # 实时处理结果
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            try:
                port_num, status, response_time = future.result()
                scanned_count += 1
                
                # 实时打印每个端口的结果
                print(f"端口 {port_num}: {status} (响应时间: {response_time:.4f}s)")
                
                # 如果端口开放，记录并检查HTTP服务
                if status == "开放":
                    open_ports.append(port_num)
                    print(f"  [+] 发现开放端口: {port_num}")
                    
                    # 检查HTTP服务
                    is_http, http_details = check_http_service(target_ip, port_num)
                    if is_http:
                        http_ports.append((port_num, http_details))
                        print(f"  [HTTP] 发现HTTP服务: {http_details}")
                    else:
                        print(f"  [HTTP] 无HTTP服务: {http_details}")
                
                # 每扫描100个端口显示一次进度
                if scanned_count % 100 == 0:
                    elapsed = time.time() - start_time
                    print(f"\n已扫描 {scanned_count} 个端口 ({scanned_count/(end_port-start_port+1)*100:.1f}%)")
                    print(f"发现开放端口: {len(open_ports)}个")
                    print(f"当前速度: {scanned_count/elapsed:.1f} 端口/秒\n")
                    
            except Exception as e:
                print(f"端口 {port} 扫描异常: {str(e)}")
    
    # 输出最终结果
    elapsed_time = time.time() - start_time
    print(f"\n扫描完成! 耗时: {elapsed_time:.2f}秒")
    print(f"总扫描端口数: {scanned_count}")
    print(f"发现开放端口总数: {len(open_ports)}")
    
    if http_ports:
        print("\n[+] 发现HTTP服务在以下端口:")
        for port, details in http_ports:
            print(f"  端口 {port}: {details}")
            print(f"  访问地址: http://{target_ip}:{port}")
    else:
        print("\n[-] 未发现HTTP服务")

if __name__ == "__main__":
    main()
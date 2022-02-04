import socket
import time
import sys
import os
def sendServerIP():
    # UDP传输
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        # 获取本机IP
        IP = socket.gethostbyname(socket.gethostname())
        # 255表示广播地址
        IP = IP[:IP.rindex('.')]+'.255'
        # 发送信息
        sock.sendto('ServerIP'.encode(), (IP, 5080))
        time.sleep(1)


print('Server started...')
sendServerIP()

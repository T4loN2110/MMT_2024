import pickle
import selectors
import socket
import os
import sys
import threading
import time
HOST = ""
PORT = 54321

# Đọc file_list
def readFileList():
    file_list = []
    try:
        with open('file_list.txt', 'r') as file:
            for line in file:
                temp = line.strip().split(' ')
                if len(temp) == 2:
                    name, size = temp
                    file_path = os.path.join('files', name)
                    file_size = os.path.getsize(file_path)
                    file_list.append((name, file_size))
        return file_list
    except FileNotFoundError:
        print('File not found')
        return file_list
def getDownloadFiles(socket):
    listFile=dict()
    while True:
        msg=""
        while True:
            d = socket.recv(1).decode()
            if(not d):
                print("Client disconnected")
                socket.close()
                sys.exit()
            if d == '\n':
                break
            msg += d
        if(msg=='Start Download'):
            return listFile
        
        download_file,prio = msg.split(' ')
        if not download_file:
            return listFile
        file_path = os.path.join('files', download_file)
        if not os.path.exists(file_path):
            socket.send('File not found'.encode())
        if (prio=="NORMAL"):
            listFile[download_file]=1
        elif prio=="HIGH":
            listFile[download_file]=4
        elif prio=="CRITICAL":
            listFile[download_file]=10
def processFile(socket,file,prio):
    file_path = os.path.join('files', file)
    sendContent=str("S@").encode()
    with open(file_path, 'rb') as f:
        content = f.read(1024*prio)
        if not content:
            return
        sendContent+=str(file+"@"+str(len(content))+"\n").encode()
        sendContent+=content
        socket.sendall(sendContent)
        while True:
            content = f.read(1024*prio)
            if not content:
                break
            if(len(content)<1024*prio):
                sendContent=str("E@").encode()
            else:
                sendContent=str("M@").encode()
            sendContent+=str(file+"@"+str(len(content))+"\n").encode()
            sendContent+=content
            socket.sendall(sendContent)
            #time.sleep(0.01)
        
    return           
# Xử lý kết nối và yêu cầu từ client
def handleClient(socket):
    file_list = readFileList()
    # Gửi thông tin các file hiện có cho client
    file_data = '\n'.join([f'{name} {size}' for name, size in file_list])
    socket.sendall(file_data.encode() + b'\n')
    # Chờ client kết nối
    while True:
        fileList=getDownloadFiles(socket)
        if(len(fileList)>0):
            for file,prio in fileList.items():
                threading.Thread(target=processFile,args=(socket,file,prio)).start()
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print("Waiting for Client")
    try:
        while True:
            conn, addr = s.accept()
            print('Connected successfully!')
            print(addr)
            thread=threading.Thread(target=handleClient, args=(conn, ))
            thread.start()
    except KeyboardInterrupt:
        print('Server closed.')
    finally:
        s.close()

if __name__ == '__main__':
    main()
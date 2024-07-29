import socket
import os
import threading
import time
HOST = "127.0.0.1"
PORT = 54321

# Đọc file input
def readInputFile():
    input_file = []
    try:
        with open('input.txt', 'r') as file:
            input_file = file.read().splitlines()
    except FileNotFoundError:
        return input_file
    return input_file

def receiveFileList(socket):
    temp = b''
    res=dict()
    while True:
        data = socket.recv(1024)
        if not data:
            break
        temp += data
        if b'\n' in temp:
            break

    file_data = temp.decode().strip()
    file_list = file_data.splitlines()
    for file in file_list:
        name,size=file.split()
        res[name]=int(size)
    return res

def downloadFile(socket, fileList,totalByte:dict):
    dowloadedByte=dict()
    for file in fileList:
    # Gửi tên file cần tải cho server
        socket.send(file.encode())
        socket.send("\n".encode())
        dowloadedByte[file.split()[0]]=0
    socket.send("Start Download\n".encode())
    finished=0
    num=len(fileList)
    while True:
        header = ""
        while True:
            d = socket.recv(1).decode()
            if d == '\n':
                break
            header += d
            
        flag="".join(header.split('@')[0])
        filename = "".join(header.split('@')[1])
        chunkSize= int(header.split('@')[2])
        mode=''
        if(flag=="S"):
            mode='w+b'
        else:
            mode='ab'
        with open(os.path.join('output', filename), mode) as f:
            try:
                content=socket.recv(chunkSize)
                f.write(content)
                dowloadedByte[filename] += len(content)
                for file in fileList:
                    name=file.split()[0]
                    percent_complete = (dowloadedByte[name] / totalByte[name]) * 100
                    print(f"Downloading {name} ... {percent_complete:.2f}%")
                print("\033["+str(num)+"A", end="")
            except KeyboardInterrupt: 
                print('Stop downloading')
                return
        if(dowloadedByte==totalByte):
            break
def main():
    host=input("Enter host ip:")
    port=int(input("Enter port:"))
    server_address = (host, port)
    downloaded_files = set()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'Connecting to {server_address}')
    client.connect(server_address)
    file_list = receiveFileList(client)
    if not file_list:
        print('No files received from server')
        client.close()
    print('Available file on server:')
    for (file,size) in file_list.items():
        print(file+" "+str(int(size/1024/1024))+"MB")
    while True:
        try:
            totalByte=dict()
            download_files = readInputFile()
            download_files = [f for f in download_files if f not in downloaded_files]
            for file in download_files.copy():
                fileName=file.split()[0]
                if(os.path.isfile(os.path.join('output', fileName))):
                    downloaded_files.add(fileName)
                    download_files.remove(file)
                else:
                    totalByte[fileName]=file_list[fileName]
            if(len(download_files)>0):
                threading.Thread(target=downloadFile,args=(client,download_files,totalByte)).start()
            time.sleep(2)
        except KeyboardInterrupt:
            print('\nClosed client')
            client.close()
            break

if __name__ == '__main__':
    main()
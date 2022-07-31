
import socket
import os
import sys

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST_ADDR = 'localhost'
HOST_PORT = 8080
BUFF_SIZE = 4096

server_addr = (HOST_ADDR, HOST_PORT)

#controlla la risposta del server
def checkResponse(data):
    check = data.decode('utf8') == '500_Internal_Server_Error'
    return check
    
while True:
    
    while True:
        print("1) get file list")
        print("2) download a file")
        print("3) upload a file")
        print("4) exit")
        response = input("choise -> ")
        
        #mostra a video una di lista di file presenti nel server
        if response == '1':
            msg = 'LIST'
            sk.sendto(msg.encode('utf8'), server_addr)
            data, server = sk.recvfrom(BUFF_SIZE)
            if checkResponse(data):
                continue
            numberFiles = int(data.decode('utf8'))
            print('\n')
            for i in range(0, numberFiles):
                data, server = sk.recvfrom(BUFF_SIZE)
                if checkResponse(data):
                    break
                print(data.decode('utf8'))
            data, server = sk.recvfrom(BUFF_SIZE)
            if checkResponse(data):
                continue
            print('\n' + data.decode('utf8') + '\n')
            
        #scarica un file
        elif response == '2':
            fileName = input("type the name of the file: ")
            msg = 'GET'
            sk.sendto(msg.encode('utf8'), server_addr)
            sk.sendto(fileName.encode('utf8'), server_addr)
            data, server = sk.recvfrom(BUFF_SIZE)
            if checkResponse(data):
                continue
            msg = data.decode('utf8')
            if msg == '401_File_Not_Found':
                print(msg)
                continue
            dirPath = os.path.join(os.getcwd(), 'download')
            filePath = os.path.join(dirPath, fileName)
            f = open(filePath, 'w')
            data, server = sk.recvfrom(BUFF_SIZE)
            if checkResponse(data):
                continue
            f.write(data.decode('utf8'))
            f.close()
            print(data.decode('utf8'))
            
        #carica file
        elif response == '3':
            fileName = input("type the name of the file (firstly put the file in the upload dir): ")
            dirPath = os.path.join(os.getcwd(), 'upload')
            filePath = os.path.join(dirPath, fileName)
            if os.path.exists(filePath):
                msg = 'POST'
                sk.sendto(msg.encode('utf8'), server_addr)
                f = open(filePath,'r+')
                fileContent = f.read()
                sk.sendto(fileName.encode('utf8'), server_addr)
                sk.sendto(fileContent.encode('utf8'), server_addr)
                f.close()
            else:
                print('the file doesn\'t exists in the upload dir')
            data, server = sk.recvfrom(BUFF_SIZE)
            print(data.decode('utf8'))
        
        #chiudi il client
        elif response == '4':
            sk.close()
            sys.exit()
            break

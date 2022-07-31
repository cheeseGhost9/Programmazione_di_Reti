
import socket
import os

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST_ADDR = 'localhost'
HOST_PORT = 8080
BUFF_SIZE = 4096
address = ''

def serverResponse(msg):
    sk.sendto(msg.encode(), address)
        
def success():
    msg = '200_Ok'
    serverResponse(msg)

server_addr = (HOST_ADDR, HOST_PORT)
print ('\n\r server starting up on %s port %s' % server_addr)
sk.bind(server_addr)

while True:
    data, address = sk.recvfrom(BUFF_SIZE)
    request = data.decode('utf8')
    
    try:
        
        if request == 'LIST':
            dirPath = os.path.join(os.getcwd(), 'content')
            fileList = os.listdir(dirPath)
            numberFiles = len(fileList)
            sk.sendto(str(numberFiles).encode('utf8'), address)
            for i in range (0, numberFiles):
                sk.sendto(fileList[i].encode('utf8'), address)
            success()
        
        elif request == 'GET':
            data, address = sk.recvfrom(BUFF_SIZE)
            dirPath = os.path.join(os.getcwd(), 'content')
            filePath = os.path.join(dirPath, data.decode('utf8'))
            if os.path.exists(filePath):
                f = open(filePath,'r+')
                fileContent = f.read()
                sk.sendto(fileContent.encode('utf8'), address)
                f.close()
                success()
            else:
                msg = '401_File_Not_Found'
                serverResponse(msg)
        
        elif request == 'POST':
            data, address = sk.recvfrom(BUFF_SIZE)
            fileName = data.decode('utf8')
            dirPath = os.path.join(os.getcwd(), 'content')
            filePath = os.path.join(dirPath, fileName)
            f = open(filePath, 'w')
            data, address = sk.recvfrom(BUFF_SIZE)
            f.write(data.decode('utf8'))
            f.close()
            success()
        
        else:
            msg = '400_Bad_Request'
            serverResponse(msg)
        
    except Exception:
        msg = '500_Internal_Server_Error'
        serverResponse(msg)
        sk.close()
    
sk.close()
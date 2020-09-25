# Author: Walber C J Rocha
# University: Universidade Federal do Recôncavo da Bahia

import os, pickle, socket, sys

BUFFER_SIZE = 1024

def list_cache_request(s, request):
    s.send(request.encode())
    files_in_cache = s.recv(BUFFER_SIZE)
    print(pickle.loads(files_in_cache))

def file_request(directory, s, request):
    os.chdir(directory)
    s.send(request.encode())

    with open(request, 'wb') as file:
        have = True
        while True:
            data = s.recv(BUFFER_SIZE)
            if(data == b'File does not exist'):
                print('File does not exist')
                os.remove(request)
                have = False
                break
            if not data:
                break
            file.write(data)
    file.close()
    if(have):
        print(f'File {request} saved')
    s.close()

if __name__ == "__main__":
    
    HOST = sys.argv[1]
    PORT = sys.argv[2]
    request = sys.argv[3]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, int(PORT)))

    if(request == 'list'):
        list_cache_request(s, request)
    else:
        DIRECTORY = sys.argv[4]
        file_request(DIRECTORY, s, request)
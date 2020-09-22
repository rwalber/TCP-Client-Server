# Author: Walber C J Rocha
# University: Universidade Federal do Recôncavo da Bahia

import socket, pickle, os

BUFFER_SIZE = 1024

if __name__ == "__main__":
    # host = input('Host: ')
    # port = input('Port: ')

    host = 'localhost'
    port = 3333

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))

    request = input('Request file: ')
    s.send(request.encode())

    if(request == 'cache'):
        files_in_cache = s.recv(BUFFER_SIZE)
        print(pickle.loads(files_in_cache))
        
    else:
        with open(request, 'wb') as file:
            while True:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                # if(pickle.loads(data) == 'The file does not exist on the server'):
                #     print('The file does not exist on the server')
                #     os.remove(request)
                #     break
                file.write(data)
        file.close()
    
    s.close()
    print('Transfer Completed')
# Author: Walber C J Rocha
# University: Universidade Federal do Recôncavo da Bahia

import socket, pickle

if __name__ == "__main__":
    # host = input('Host: ')
    # port = input('Port: ')

    host = 'localhost'
    port = 3333

    s = socket.socket()
    s.connect((host, int(port)))

    request = input('Request file: ')
    s.send(request.encode())
    
    file_receive = b''
    while True:
        data = s.recv(4096)
        if not data:
            break
        file_receive += data
    
    payload_file = pickle.loads(file_receive)

    if(request == 'cache'):
        print(payload_file)
        s.close()

    else:
        if(payload_file != 'The file does not exist on the server'):
            with open(request, 'wb') as file:
                file.write(payload_file)
                file.close()
            print('Transfer Completed')
            s.close()
        else:
            print('The file does not exist on the server')
            s.close()
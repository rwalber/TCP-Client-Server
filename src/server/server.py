# Author: Walber C J Rocha
# University: Universidade Federal do Recôncavo da Bahia

import socket, os, pickle, math

MAX_CACHE_SIZE = 15.3*(10**6)

BUFFER_SIZE = 1024

CACHE_SIZE = 0

def remove_element_cache(self, CACHE_SIZE, size_file):
   size_to_remove = 0
   key_to_remove = ''
   count = 0
   for key in self:
      file = self.get(key)
      current_key = key
      current_size = file['size']
      if(file['size'] >= size_file):
         size_to_remove = current_size
         key_to_remove = current_key
         break
      else:
         if(size_to_remove >= count):
            count = current_size
            size_to_remove = count
            key_to_remove = current_key
   
   self.pop(key_to_remove)
   return (CACHE_SIZE - size_to_remove)

def get_cache_files(self):
   list = [] 
   for key in self.keys(): 
      list.append(key) 
   return list

if __name__ == "__main__":
   # host = input('Host: ')
   # port = input('Port: ')

   host = 'localhost'
   port = 3333
   
   CACHE = { }
   
   s = socket.socket()
   s.bind((host, int(port)))
   s.listen()
   
   while True:
      conn, addr = s.accept()
      print('Client connect, wait request')

      request = conn.recv(BUFFER_SIZE).decode()
      
      if(request == 'cache'):
         print('Cache request')
         conn.send(pickle.dumps(get_cache_files(CACHE)))
         conn.close()
         print('Transfer completed, closed connection')

      else:

         if(CACHE.get(str(request))):
            print('Cache hit, sending, wait')
            payload_file = CACHE.get(str(request))
            data = payload_file['data']
            conn.send(data)
            conn.close()
            print('Transfer completed, closed connection')

         else:
            if(os.path.isfile(request)):
               print('Cache miss, send file, please, wait')
               payload_file = b''
               file = open(request, 'rb')
               file_size = os.path.getsize(request)
               file_load = file.read()
               
               while(file_load):
                  serialize = pickle.dumps(file_load)
                  payload_file += serialize
                  conn.send(serialize)
                  file_load = file.read()
               
               file.close()
               
               if(file_size <= MAX_CACHE_SIZE):
                  while(CACHE_SIZE+file_size > MAX_CACHE_SIZE):
                     CACHE_SIZE = remove_element_cache(CACHE, CACHE_SIZE, file_size)
                     
                  to_cache = {str(request): {'size': file_size, 'data': payload_file}}
                  CACHE_SIZE += file_size
                  CACHE.update(to_cache)

               print('Transfer completed, closed connection')
               conn.close()
            else:
               conn.send(pickle.dumps('The file does not exist on the server'))
               conn.close()
               print('Closed connection')

   # to_cache = {'f1': {'size': 100, 'data': 'payload_file'},
   # 'f2': {'size': 300, 'data': 'payload_file'},
   # 'f3': {'size': 130, 'data': 'payload_file'}}

   # to_cache2 = {'f4': {'size': 700, 'data': 'payload_file'},
   # 'f5': {'size': 200, 'data': 'payload_file'},
   # 'f6': {'size': 4, 'data': 'payload_file'}}

   # CACHE.update(to_cache)
   # CACHE.update(to_cache2)
   # teste = get_cache_files(CACHE)
   # print(teste)
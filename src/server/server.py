# Author: Walber C J Rocha
# University: Universidade Federal do Recôncavo da Bahia

import os, pickle, socket, sys, threading

# Global variables
MB = 64
MAX_CACHE_SIZE = MB*(10**6)

BUFFER_SIZE = 1024

CACHE_SIZE = 0

CACHE = { }
# -----------------

def remove_element_cache(size_file):
   size_to_remove = 0
   key_to_remove = ''
   count = 0
   for key in CACHE:
      file = CACHE.get(key)
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
   CACHE.pop(key_to_remove)
   return (CACHE_SIZE - size_to_remove)

def get_cache_files():
   list = []
   for key in CACHE.keys(): 
      list.append(key) 
   return list

def client_connect(directory, conn, addr, lock):
   global CACHE
   global CACHE_SIZE
   
   os.chdir(directory)

   request = conn.recv(BUFFER_SIZE).decode()
   
   print(f'Client {addr} is requesting file {request}')

   if(request == 'list-cache'):
      conn.send(pickle.dumps(get_cache_files()))
      conn.close()
      print('Cache request sent to the client')
   
   else:
      if(CACHE.get(str(request))):
         print(f'Cache hit. File {request} sent to the client.')
         payload_file = CACHE.get(str(request))
         data = pickle.loads(payload_file['data'])
         conn.send(data)
         conn.close()
         lock.release()

      else:
         if(os.path.isfile(request)):        
            with open(request, 'rb') as file:
               file_size = os.path.getsize(request)
               payload_file = file.read()
               if(file_size <= MAX_CACHE_SIZE):
                  
                  lock.acquire()
                  payload_to_cache = b''
                  while(payload_file):
                     conn.send(payload_file)
                     payload_to_cache += payload_file
                     payload_file = file.read(BUFFER_SIZE)
                  
                  payload_serialize = pickle.dumps(payload_to_cache)
                  while(CACHE_SIZE+file_size > MAX_CACHE_SIZE):
                     CACHE_SIZE = remove_element_cache(file_size)
                  
                  to_cache = {str(request): {'size': file_size, 'data': payload_serialize}}
                  CACHE_SIZE += file_size
                  CACHE.update(to_cache)
                  
                  lock.release()
                  
               else:
                  while(payload_file):
                     conn.send(payload_file)
                     payload_file = file.read(BUFFER_SIZE)
            file.close()
            conn.close()
            print(f'Cache miss. File {request} sent to the client')
         
         else:
            conn.send(b'File does not exist')
            conn.close()
            print(f'File {request} does not exist')

if __name__ == "__main__":

   HOST = sys.argv[1]
   PORT = sys.argv[2]
   DIRECTORY = sys.argv[3]

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((HOST, int(PORT)))

   while True:
      s.listen()
      conn, addr = s.accept()
      lock = threading.Semaphore()
      new_client = threading.Thread(target=client_connect, args=(DIRECTORY, conn, addr, lock))
      new_client.start()
   
   s.close()
# Author: Walber C J Rocha
# University: Universidade Federal do Recôncavo da Bahia

import os, pickle, socket, threading, time

# Global variables
MB = 20
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

def ClientConnect(conn, addr, lock):

   global CACHE
   global CACHE_SIZE

   print('Client connect, wait request')
   request = conn.recv(BUFFER_SIZE).decode()

   if(request == 'cache'):
      print('Cache request')
      conn.send(pickle.dumps(get_cache_files()))
      conn.close()
      print('Transfer completed, closed connection')
   else:
      if(CACHE.get(str(request))):
         print('Cache hit, sending, wait')
         timeInit = time.time()
         lock.acquire()
         payload_file = CACHE.get(str(request))
         data = pickle.loads(payload_file['data'])
         conn.send(data)
         conn.close()
         lock.release()
         timeFinal = time.time()-timeInit
         print('Tempo: '+str(timeFinal))
         print('Transfer completed, closed connection')
      else:
         if(os.path.isfile(request)):        
            with open(request, 'rb') as file:
               file_size = os.path.getsize(request)
               payload_file = file.read()
               if(file_size <= MAX_CACHE_SIZE):
                  timeInit = time.time()
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
                  time.sleep(5)
                  lock.release()
                  timeFinal = time.time()-timeInit
                  print('Tempo: '+str(timeFinal))
               else:
                  while(payload_file):
                     conn.send(payload_file)
                     payload_file = file.read(BUFFER_SIZE)
            file.close()
            conn.close()
            print('Transfer completed, closed connection')
         else:
            conn.send(pickle.dumps('The file requested does not exist on the server'))
            conn.close()
            print('The file requested does not exist on the server, closed connection')

if __name__ == "__main__":
   
   # HOST = input('Host: ')
   # PORT = input('Port: ')
   HOST = 'localhost'
   PORT = 3333

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((HOST, int(PORT)))

   while True:
      s.listen()
      conn, addr = s.accept()
      lock = threading.Semaphore()
      new_client = threading.Thread(target=ClientConnect, args=(conn, addr, lock))
      new_client.start()

      for thread in threading.enumerate():
         print(thread)
   
   s.close() 
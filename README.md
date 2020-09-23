<br />

<h3 align="center">Implementation of a TCP client and server, to retrieve files and a TCP server to serve the requested files</h3>

  <p align="center">
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    ·
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Project Description</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Run Project</a>
     ·
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

### Overview

This project consists of the implementation of a TCP client-server. In it we find the TCP client, which can request the files located in the directory of the TCP server, which serves the requested files.

The client, after establishing a connection with the server, sends the requested file name. The server, upon receiving the request, looks for the file in its cache memory or in its predefined directory. If the file is found in either location, the server then transmits the file's content to the client over the same connection.

####  · Client

The client presents the implementation of a TCP-client. Client requests take 4 parameters - the server name, the server port, the file to be requested and the directory location where you want to save the file. Can make the following requests to the server:

1. Files allocated in cache memory

To request the list of files in the cache memory, the client provides the following entry:
```sh
python3 client.py host port list-cache directory
```


2. File present in the server directory

To order the files, the customer provides the following entry:
```sh
python3 client.py host port file-name directory
```

If the file is not present in the server's directory, the following result is expected:


####  · Server

The server consists of a server-TCP Multi-Thread implementation, in which, for each connected client, a Thread is created, executing the flow of its requests in parallel, with concurrent control over the read / write in the cache memory.

The cache memory is implemented as a hash table, in which the registry key for each element is the name of the file, and the properties, file_size: containing the file size and date: payload of the file. Example:

```python
CACHE = {
	file_name = {file_size: 'Size', data: 'Payload file'},
	.
	.
	.
}
```
##### Features
When establishing the connection with the client, the server starts to wait for your request, which can be:

1. List of files present in the server's cache

Upon receiving this request, the server sends the client a list with the name of the files that are allocated in the cache memory of the server, afterwards it closes the connection.

2. Request for files located in the server directory

File requests follow the following flows:

Initially the server checks whether the requested file is allocated in its cache memory. If so, the file's payload goes through the deserialization process, followed by sending it to the client. When finished, the connection is ended.
If the requested file is not in the cache memory of the server, the following are the flows:

```python
if The file exists on the server {
  Check if the file size is bigger than the cache memory size {
	  The server sends the file to the client, followed by the connection termination
  } 
  else {
	The server opens the file, followed by sending, according to the size specified for the buffer. At the end of the sending, the server serializes the payload of the file and stores it in the cache memory, in order to provide the file more quickly in the next requests.
  }
} 
else {
	The server sends a message to the client stating that the file does not exist in its current directory.
} 
```
In the stage of storing the payload of the file, a check is made of the available space in the cache memory, which has a size limitation of 64 MB. If the size of the file in question exceeds the limit value of the cache memory, there is a process of reallocation of the files present in the cache.

The strategy used for the relocation process is to check if there are any files in cache memory, which are larger in size than the file being requested, so remove this file and store the new one.
If none of the files are larger than the requested file, a cycle of removing the files follows until the cache has enough space to allocate the new file.

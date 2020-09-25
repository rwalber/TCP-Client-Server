<br />

<h2 align="center">Implementation of a TCP client-server. Where the client requests files from a TCP server, which serves the requested files.</h2>

<br />
<br />

* [About the Project](#about-the-project)
  * [Overview](#overview)
  * [Client](#client)
  * [Server](#server)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Execution](#execution)
* [Contact](#contact)
* [License](#license)

<br />

## About The Project

### Overview
<p align="justify">
This project consists of the implementation of a TCP client-server. In it we find the TCP client, which can request the files located in the directory of the TCP server, which serves the requested files.

The client, after establishing a connection with the server, sends the requested file name. The server, upon receiving the request, looks for the file in its cache memory or in its predefined directory. If the file is found in either location, the server then transmits the file's content to the client over the same connection.

</p>

#### Client

The client presents the implementation of a TCP-client. Client requests take 4 parameters - the server name, the server port, the file to be requested and the directory location where you want to save the file. Can make the following requests to the server:

1. File present in the server directory

To order the files, the customer provides the following entry:
```sh
python3 client.py host port file-name directory
```

<p align="center">
  <img src="assets/file-request.gif" />
</p>

If the file is not present in the server's directory, the following result is expected:

<p align="center">
  <img src="assets/file-not.gif" />
</p>

2. Files allocated in cache memory

To request the list of files in the cache memory, the client provides the following entry:
```sh
python3 client.py host port list
```

<p align="center">
  <img src="assets/list.gif" />
</p>

#### Server

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
	The server opens the file, followed by sending, according to the size specified for the buffer. 
	At the end of the sending, the server serializes the payload of the file and stores it in the cache 
	memory, in order to provide the file more quickly in the next requests.
  }
} 
else {
	The server sends a message to the client stating that the file does not exist in its current directory.
} 
```
In the stage of storing the payload of the file, a check is made of the available space in the cache memory, which has a size limitation of 64 MB. If the size of the file in question exceeds the limit value of the cache memory, there is a process of reallocation of the files present in the cache.

The strategy used for the relocation process is to check if there are any files in cache memory, which are larger in size than the file being requested, so remove this file and store the new one.
If none of the files are larger than the requested file, a cycle of removing the files follows until the cache has enough space to allocate the new file.

<p align="center">
  <img src="assets/server-actions.gif" />
</p>

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

1. ##### Windows
	**Install Python3 or higher**
	[Python Releases](https://www.python.org/downloads/windows/)
	
	* To manage packages in Python3
		Download  [get-pip.py](https://bootstrap.pypa.io/get-pip.py)  to a folder on your computer.
		Open a command prompt and navigate to the folder containing the get-pip.py installer.
		Run the following command:

	```sh
		python get-pip.py
	```
	* Packages needed
		```sh
			pip3 install os, pickle, socket, sys, threading
		```
2. ##### Linux Systems
	**Install Python3 or higher**
	```sh
		sudo apt-get install python3.6
	```

	* Update your system
	```sh
		sudo apt update
		sudo apt -y upgrade
	```

	* To manage packages in Python3
	```sh
		sudo apt install -y python3-pip
	```

	* Packages needed
	```sh
		pip3 install os, pickle, socket, sys, threading
	```

### Execution

* Server
	```sh
		python3 server.py port_to_listen directory
	```

* Client
	```sh
		python3 client.py host_server server_port_listen file_name directory #for file request
		   or
		python3 client.py host_server server_port_listen list #for information on files in cache memory
	```
	

## Contact

Walber Conceição de Jesus Rocha <br />
Bachelor of Exact and Technological Sciences - UFRB <br />
Graduating in Computer Engineering - UFRB <br />
E-mail: walber_jesus@hotmail.com

Project Link: [TCP-Client-Server](https://github.com/rwalber/TCP-Client-Server)

## License

Distributed under the MIT License. See `LICENSE` for more information.

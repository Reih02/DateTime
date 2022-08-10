import sys
from socket import *

def client(request_type, address, port_num):
    if request_type != "date" and request_type != "time":
        sys.exit("Request type invalid")

    try:
        address = getaddrinfo(address, port_num)[0][4][0]
    except:
        sys.exit("Supplied address invalid")

    if port_num < 1024 or port_num > 64000:
        # checks if any port values are less than 1024 or greater than 64000
        sys.exit("Port number must be between 1024 and 64000!")

    serverAddress = (address, port_num)

    #client_socket




print(client("date", "learn.canterbury.ac.nz", 3000))

request_type = input("Please enter 'date' to request the current date, or 'time' to request the current time from the server: ")
address = input("Please enter the address of the server (decimal or host-name): ")
port_num = int(input("Please enter the port number you wish to use on the server: "))

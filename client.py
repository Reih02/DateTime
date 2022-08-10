import sys
from socket import *

MAGICNO = 0x497E

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

    server_address = (address, port_num)

    # opens client socket
    client_socket = socket.socket(AF_INET, SOCK_DGRAM)

    # prepares and sends DT-Request packet to server
    if request_type == "date":
        request_type = 0x0001
    elif request_type == "time":
        request_type = 0x0002

    magic_number = MAGICNO.to_bytes(2, 'big')
    packet_type = 0x0001.to_bytes(2, 'big')
    request_type = request_type.to_bytes(2, 'big')

    bytes = magic_number + packet_type + request_type

    request_packet = bytearray(list(bytes))

    client_socket.sendto(request_packet, server_address)







print(client("date", "learn.canterbury.ac.nz", 3000))

request_type = input("Please enter 'date' to request the current date, or 'time' to request the current time from the server: ")
address = input("Please enter the address of the server (decimal or host-name): ")
port_num = int(input("Please enter the port number you wish to use on the server: "))

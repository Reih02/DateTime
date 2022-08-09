import select
import time
from datetime import date
from socket import *

def server(port_1, port_2, port_3):
    port_vars = [port_1, port_2, port_3]
    if len(set(port_vars)) != len(port_vars):
        # not all unique port values
        print("All port numbers must be unique!")
        quit()
    elif not all(x >= 1024 and x <= 64000 for x in port_vars):
        # checks if any port values are less than 1024 or greater than 64000
        print("All port numbers must be between 1024 and 64000!")
        quit()

    try:
        # creates three UDP sockets using IPv4
        server_socket_1 = socket(AF_INET, SOCK_DGRAM)
        server_socket_2 = socket(AF_INET, SOCK_DGRAM)
        server_socket_3 = socket(AF_INET, SOCK_DGRAM)

        # binds said sockets to the three port numbers
        server_socket_1.bind(('localhost', port_1))
        server_socket_2.bind(('localhost', port_2))
        server_socket_3.bind(('localhost', port_3))
    except:
        print("Socket binding failed.")
        quit()

    # listen for incoming packets on the sockets
    input_sockets = [server_socket_1, server_socket_2, server_socket_3]
    while True:
        # listen over sockets
        readable, writable, error_sockets = select.select(input_sockets, [], [])
        for r in readable:
            # incoming data on socket
            if r in input_sockets:
                # packet received
                receiving_socket = r # used for knowing which language client wants
                client_packet = r.recvfrom(1024) # receives packet with buffer size of 1024
                message, client_address = client_packet
                received_packet = bytearray(message)
                print(received_packet)

                # packet checks
                if len(received_packet) != 6:
                    print("Length of packet not 6 bytes")
                    break
                if ((received_packet[0] << 8) + received_packet[1]) != 0x497E:
                    print("MagicNo field incorrect")
                    break
                if ((received_packet[2] << 8) + received_packet[3]) != 0x0001:
                    print("PacketType field incorrect")
                    break
                if ((received_packet[4] << 8) + received_packet[5]) != 0x0001 \
                and ((received_packet[4] << 8) + received_packet[5]) != 0x0002:
                    print("RequestType field incorrect")
                    break
                # packet accepted

                # checks whether client wants current date or current time
                if ((received_packet[4] << 8) + received_packet[5]) == 0x0001:
                    request_type = "date"
                elif ((received_packet[4] << 8) + received_packet[5]) == 0x0002:
                    request_type = "time"

                curr_date = date.today().strftime("%Y : %m : %d")
                curr_time = time.strftime("%H : %M") 





print(server(1890, 1510, 6390))

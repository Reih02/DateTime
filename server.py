import select
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
    output_sockets = []
    while True:
        readable, writable, exceptional = select.select(input_sockets, output_sockets, input_sockets)
        for r in readable:
            if r in input_sockets:
                # packet received
                receiving_socket = r # used for knowing which language client wants
                conn, client_addr = r.accept()
                print(client_addr)
                # receives packet with buffer size of 1024
                client_packet = r.recvfrom(1024)
                received_packet = bytearray(client_packet)
                print(received_packet)

                ### Need to store IP addr and port num of client.

                # packet checks
                if len(received_packet) != 6:
                    print("Length of packet not 6 bytes")
                    break
                if 



print(server(1890, 1510, 6390))

import sys
import select
from socket import *

MAGICNO = 0x497E

def client(request_type, address, port_num):
    if request_type != "date" and request_type != "time":
        sys.exit("Request type invalid")

    try:
        # converts hostname into decimal format address
        address = getaddrinfo(address, port_num)[0][4][0]
    except:
        sys.exit("Supplied address invalid")

    if port_num < 1024 or port_num > 64000:
        # checks if any port values are less than 1024 or greater than 64000
        sys.exit("Port number must be between 1024 and 64000!")

    server_address = (address, port_num)

    # opens client socket
    client_socket = socket(AF_INET, SOCK_DGRAM)

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

    readable, writable, error_sockets = select.select([client_socket],
                                                       [], [], 1.0)
    if len(readable) == 0 and len(writable) == 0 and len(error_sockets) == 0:
        # timeout reached
        sys.exit("Timed out waiting for response packet")
    else:
        for r in readable:
            server_packet = r.recvfrom(1024)
            message, server_address = server_packet
            received_packet = bytearray(message)

            # define each field for use in packet checks and printing
            # contents of the packet

            magic_number = (received_packet[0] << 8) + received_packet[1]
            packet_type = (received_packet[2] << 8) + received_packet[3]
            language_code = (received_packet[4] << 8) + received_packet[5]
            year = (received_packet[6] << 8) + received_packet[7]
            month = received_packet[8]
            day = received_packet[9]
            hour = received_packet[10]
            minute = received_packet[11]
            length = received_packet[12]
            text = received_packet[13:]


            # packet checks
            if len(received_packet < 13):
                    sys.exit("Some header fields not present")

            if magic_number != MAGICNO:
                sys.exit("MagicNo field incorrect")

            if packet_type != 0x0002:
                sys.exit("PacketType field incorrect")

            if language_code != 0x0001 \
            and language_code != 0x0002 \
            and language_code != 0x0003:
                sys.exit("LanguageCode field incorrect")

            if year >= 2100:
                sys.exit("Year value too large")

            if month < 1 or month > 12:
                sys.exit("Month value not within parameters")

            if day < 1 or day > 31:
                sys.exit("Day value not within parameters")

            if hour < 0 or hour > 23:
                sys.exit("Hour value not within parameters")

            if minute < 0 or minute > 59:
                sys.exit("Minute value not within parameters")

            if length != 13 + len(text)
                sys.exit("Length value incorrect")

            # decode text from packet
            text_bytes = received_packet[13:]
            text = text_bytes.decode('utf-8')

            # print contents of packet
            print("Magic number: {}".format(magic_number))
            print("Packet type: DT-Response ({})".format(packet_type))
            print("Language code: {}".format(language_code))
            print("Date info (year:month:day:hour:minute):", \
                  " {}:{}:{}:{}:{}".format(year, month, day, hour, minute))
            print("Length: {}".format(length))
            print("Text:\n" + text)












print(client("date", "learn.canterbury.ac.nz", 3000))

request_type = input("Please enter 'date' to request the current date, or 'time' to request the current time from the server: ")
address = input("Please enter the address of the server (decimal or host-name): ")
port_num = int(input("Please enter the port number you wish to use on the server: "))

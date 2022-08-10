import select
import time
from socket import *

MAGICNO = 0x497E

def server(port_1, port_2, port_3):
    '''Main server function'''
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
        server_socket_1.bind((INADDR ANY, port_1))
        server_socket_2.bind((INADDR ANY, port_2))
        server_socket_3.bind((INADDR ANY, port_3))
    except:
        print("Socket binding failed.")
        quit()

    print("Socket binding successful")

    # listen for incoming packets on the sockets
    input_sockets = [server_socket_1, server_socket_2, server_socket_3]
    while True:
        print("Listening over sockets...")
        # listen over sockets
        readable, writable, error_sockets = select.select(input_sockets, [], [])
        for r in readable:
            # incoming data on socket
            if r in input_sockets:
                # packet received
                receiving_socket = input_sockets.index(r) + 1 # used for knowing which language client wants
                client_packet = r.recvfrom(1024) # receives packet with buffer size of 1024
                message, client_address = client_packet
                received_packet = bytearray(message)

                # packet checks
                if len(received_packet) != 6:
                    print("Length of packet not 6 bytes")
                    break
                if ((received_packet[0] << 8) + received_packet[1]) != MAGICNO:
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

                if receiving_socket == 1:
                    chosen_language = "english"
                    language_code = 0x0001
                elif receiving_socket == 2:
                    chosen_language = "maori"
                    language_code = 0x0002
                elif receiving_socket == 3:
                    chosen_language = "german"
                    language_code = 0x0003

                # prepare DT-Response packet
                text = textual_repr(chosen_language, request_type)
                if len(text) > 255:
                    print("Text too long")
                    break

                # initialise all current date/time values
                year, month, day, hour, minute = date_time_info()

                ### maybe need a buffer?? ###

                # put values into corresponding amount of bytes for packet
                magic_number = MAGICNO.to_bytes(2, 'big')
                packet_type = 0x0002.to_bytes(2, 'big')
                language_code = language_code.to_bytes(2, 'big')
                year = year.to_bytes(2, 'big')
                month = month.to_bytes(1, 'big')
                day = day.to_bytes(1, 'big')
                hour = hour.to_bytes(1, 'big')
                minute = minute.to_bytes(1, 'big')
                length = len(text).to_bytes(1, 'big')
                text = text.to_bytes((text.bit_length() + 7) // 8, 'big')

                bytes = magic_number + packet_type + language_code + \
                        year + month + day + hour + minute + length + text

                # create response packet as a bytearray from bytes
                response_packet = bytearray(list(bytes))

                # send response packet back to client on receiving socket
                r.sendto(response_packet, client_address)




def textual_repr(language, request_type):
    '''Gets appropriate textual representation for corresponding language
       and request type'''

    months = {"January": ("Kohitatea", "Januar"),
              "February": ("Hui-tanguru", "Februar"),
              "March": ("Poutu-te-rangi", "März"),
              "April": ("Paenga-whawha", "April"),
              "May": ("Haratua", "Mai"),
              "June": ("Pipiri", "Juni"),
              "July": ("Hongongoi", "Juli"),
              "August": ("Here-turi-koka", "August"),
              "September": ("Mahuru", "September"),
              "October": ("Whiringa-a-nuku", "Oktober"),
              "November": ("Whiringa-a-rangi", "November"),
              "December": ("Hakihea", "Dezember")}

    if language == "english":
        if request_type == "date":
            text = time.strftime("Today's date is %B %d, %Y")

        elif request_type == "time":
            text = time.strftime("The current time is %H:%M")

    elif language == "maori":
        if request_type == "date":
            eng_month = time.strftime("%B")
            text = time.strftime("Ko te ra o tenei ra ko {} %d, %Y").format(months[eng_month][0])

        elif request_type == "time":
            text = time.strftime("Ko te wa o tenei wa %H:%M")

    elif language == "german":
        if request_type == "date":
            eng_month = time.strftime("%B")
            text = time.strftime("Heute ist der %d. {} %Y").format(months[eng_month][1])

        elif request_type == "time":
            text = time.strftime("Die Uhrzeit ist %H:%M")

    return bytearray(text.encode('utf-8'))


def date_time_info():
    '''gets current date/time values and converts into integers for use in
       response packet'''

    year = int(time.strftime("%Y"))
    month = time.strftime("%m")
    if month[0] == '0':
        month = month[1:]
    month = int(month)

    day = time.strftime("%d")
    if day[0] == '0':
        day = day[1:]
    day = int(day)

    hour = time.strftime("%H")
    if hour[0] == '0':
        hour = hour[1:]
    hour = int(hour)

    minute = time.strftime("%M")
    if minute[0] == '0':
        minute = minute[1:]
    minute = int(minute)

    return (year, month, day, hour, minute)

print("Please specify the three ports the server should operate on:")
print("NOTE: Port numbers must be between 1024 and 64000")
port1 = int(input("Port 1: "))
port2 = int(input("Port 2: "))
port3 = int(input("Port 3: "))
server(port1, port2, port3)

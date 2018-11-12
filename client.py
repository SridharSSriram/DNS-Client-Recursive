import threading
import socket as mysoc
import sys


def client():
    # setting up the RS socket
    try:
        rs_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client RS socket created\n")
    except mysoc.error as err:
        print('{} \n'.format("RS socket open error ", err))

    # using command line args to set the host as the same as RS server
    passed_in_host = sys.argv[1]
    host = passed_in_host

    print("[S]: Server host name is: ", host)
    rs_ip_addr = mysoc.gethostbyname(host)
    rs_server_binding = (rs_ip_addr, 55555)
    rs_socket.connect(rs_server_binding)

    # creating the file descriptor
    written_file = open("RESOLVED.txt","a")

    hostname_file_name = sys.argv[2]
    with open(hostname_file_name) as hostname_file:
        for line in hostname_file:
            # runs .rstrip() to remove trailing and leading whitespace
            hostname = line.rstrip()

            # test for empty strings
            if not hostname:
                continue
            rs_socket.send(hostname.encode('utf-8'))

            # received RS message
            rs_response = rs_socket.recv(100)
            rs_tuple = rs_response.decode('utf-8').split()
            written_file.write(rs_response.decode('utf-8'))
            written_file.write("\n")

    # final signal indicating the transaction is over
    rs_socket.send("PROJ2-HNS.txt EOF reached".encode('utf-8'))
    rs_socket.close()
    exit()


client_thread = threading.Thread(name='client', target=client)
client_thread.start()

input("Hit ENTER  to exit\n")

exit()



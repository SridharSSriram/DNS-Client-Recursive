import threading
import time
import random
import socket as mysoc
import sys


def server():
    # client connection
    try:
        server_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[RS]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    server_binding = ('', 55555)
    server_socket.bind(server_binding)
    server_socket.listen(1)

    # ******* setting up the TSCOM connection *******
    try:
        ts_com_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[com]: TS COM socket created\n")
    except mysoc.error as err:
        print('{} \n'.format("TS socket open error ", err))

    ts_com_ip_addr = mysoc.gethostbyname(sys.argv[1])
    ts_com_server_binding = (ts_com_ip_addr, 40007)
    ts_com_socket.connect(ts_com_server_binding)

    # ******* setting up the TSEDU connection *******
    try:
        ts_edu_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[edu]: TS EDU socket created\n")
    except mysoc.error as err:
        print('{} \n'.format("TS socket open error ", err))

    ts_edu_ip_addr = mysoc.gethostbyname(sys.argv[2])
    ts_edu_server_binding = (ts_edu_ip_addr, 50007)
    ts_edu_socket.connect(ts_edu_server_binding)

    host = "grep.cs.rutgers.edu"
    print("[RS]: Server host name is: ", host)

    host_ip = (mysoc.gethostbyname(host))
    print("[RS]: Server IP address is  ", host_ip)

    dns_map = create_dns_map()

    print(dns_map)
    clientsockid, addr = server_socket.accept()

    # continually accepts connections until the end of file is reached, then breaks out of loop
    while True:
        received_hostname = clientsockid.recv(100).decode('utf-8')

        if received_hostname is "PROJ2-HNS.txt EOF reached":
            goodbye = "PROJ2-HNS.txt EOF reached"
            ts_edu_socket.send(goodbye.encode('utf-8'))
            ts_com_socket.send(goodbye.encode('utf-8'))
            break

        returned_tuple = []
        # conditional check
        if dns_map.get(received_hostname) is None:

            # <string>[-3:] accesses last three characters of a string
            if received_hostname[-3:] == "edu":
                # connect to TS EDU
                ts_edu_socket.send(received_hostname.encode('utf-8'))
                returned_edu_tuple = ts_edu_socket.recv(100).decode('utf-8')
                returned_tuple.append(returned_edu_tuple)
            elif received_hostname[-3:] == "com":
                # connect to TS COM
                ts_com_socket.send(received_hostname.encode('utf-8'))
                returned_com_tuple = ts_com_socket.recv(100).decode('utf-8')
                returned_tuple.append(returned_com_tuple)
            else:
                # hostname doesn't exist in DNS table && doesn't end in .edu or .com
                returned_tuple.append(received_hostname)
                returned_tuple.append("-")
                returned_tuple.append("Error:HOST NOT FOUND")

        else:
            # generates the string "<hostname> <IP> <flag>"
            returned_tuple.append(received_hostname)
            returned_tuple.append(dns_map[received_hostname][0])
            returned_tuple.append(dns_map[received_hostname][1])

        returned_string = " ".join(returned_tuple)
        clientsockid.send(returned_string.encode('utf-8'))

    # Close the server socket
    clientsockid.close()
    server_socket.close()
    exit()


def create_dns_map():
    rs_dns_map = dict()

    rs_file_name = sys.argv[3]
    with open(rs_file_name) as ts_map:
        for line in ts_map:
            # runs .rstrip() to remove trailing and leading whitespace
            string_read_from_file = line.rstrip()
            # test for empty strings
            if not string_read_from_file:
                continue
            # generating tuple from file line
            generated_tuple = line.split()

            key_hostname =""
            value_ip_flag =""
            # checking to see entry for TS server hostname
            if generated_tuple[2] == "NS":
                continue
            else:
                # key in map is the hostname
                key_hostname = generated_tuple[0]
                # value in map is tuple of ip address and flag
                value_ip_flag=generated_tuple[1::]

            rs_dns_map[key_hostname] = value_ip_flag
        rs_dns_map["com"] = sys.argv[1]
        rs_dns_map["edu"] = sys.argv[2]
    return rs_dns_map


rs_serv = threading.Thread(name='rsserver', target=server)
rs_serv.start()
time.sleep(random.random() * 5)



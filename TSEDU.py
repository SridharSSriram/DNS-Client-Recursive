import threading
import time
import random
import socket as mysoc
import sys


def server():
    # setting up the socket to begin connections
    try:
        server_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TS EDU]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    server_binding = ('', 50007)
    server_socket.bind(server_binding)
    server_socket.listen(1)

    host = "ilab2.cs.rutgers.edu"
    print("[TS EDU]: Server host name is: ", host)

    host_ip = (mysoc.gethostbyname(host))
    print("[TS EDU]: Server IP address is  ", host_ip)

    dns_edu_map = create_dns_map()

    rs_sock_id, addr = server_socket.accept()

    # continually accepts connections until the end of file is reached, then breaks out of loop
    while True:
        received_hostname = rs_sock_id.recv(100).decode('utf-8')
        # checking for terminating message
        if received_hostname is "PROJ2-HNS.txt EOF reached":
            break
        returned_tuple = []
        if dns_edu_map.get(received_hostname) is None:
            # generates the string "<hostname> - Error: HOST NOT FOUND"
            returned_tuple.append(received_hostname)
            returned_tuple.append("-")
            returned_tuple.append("Error:HOST NOT FOUND")
        else:
            # generates the string "<hostname> <IP> <flag>"
            returned_tuple.append(received_hostname)
            returned_tuple.append(dns_edu_map[received_hostname][0])
            returned_tuple.append(dns_edu_map[received_hostname][1])

        returned_string = " ".join(returned_tuple)
        rs_sock_id.send(returned_string.encode('utf-8'))

    # Close the server socket
    server_socket.close()
    exit()


def create_dns_map():
    ts_edu_map = dict()
    ts_edu_table_name = sys.argv[1]
    with open(ts_edu_table_name) as ts_map:
        for line in ts_map:
            # runs .rstrip() to remove trailing and leading whitespace
            string_read_from_file = line.rstrip()
            # test for empty strings
            if not string_read_from_file:
                continue
            # generating tuple from file line
            generated_tuple = line.split()
            # key in map is the hostname
            key_hostname = generated_tuple[0]
            # value in map is tuple of ip address and flag
            value_ip_flag = generated_tuple[1::]

            ts_edu_map[key_hostname] = value_ip_flag

    return ts_edu_map


ts_edu_serv = threading.Thread(name='tseduserver', target=server)
ts_edu_serv.start()
time.sleep(random.random() * 5)

input("Hit ENTER to exit")
exit()
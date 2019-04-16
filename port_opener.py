

import socket
import sys

def port_opener(ports):

    sockets = None
    
    for a_port in (ports)

        in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        in_socket.setblocking(0)
        in_socket.bind('localhost', a_port)
        
        print ("Opened port, ", in_socket)

        sockets.append(in_socket)

    return (sockets)

if __name__ == "__main__":

    ports = (3001, 4001, 5001)
    port_opener(ports)

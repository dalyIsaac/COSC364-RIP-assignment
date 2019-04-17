#########################################################
#
# A function to open / bind ports to sockets
#
# Version 01: March 2019
#   First pass
#
# Version 02: 17 April 2019
#   change to match output port with destination router
#   ID
#
# Version 03:
#   updated to take in the complete "output_list" tuple
#   check if id is null:
#   YES => return tuple of sockets (input ports)
#   NO => return tuple of sockets (output ports) and
#   destination router ID
#
# Version 04:
#   need a try catch exception handler, in case a port
#   did not open/bind which returns an error code so
#   main can close everything and exit
#
#########################################################

import socket

# import sys


def port_opener(output_ports):

    socket_list = []

    try:
        if output_ports[2] is None:
            for a_port, a_cost, an_id in output_ports:

                new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # new_socket.setblocking(0)
                new_socket.bind(("localhost", a_port))

                print("Opened socket / port, ", new_socket, "/", a_port)

                socket_list.append((new_socket))

            return socket_list

        else:
            for a_port, a_cost, an_id in output_ports:

                new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # new_socket.setblocking(0)
                new_socket.bind(("localhost", a_port))

                print(
                    "Opened socket / port / ID, ",
                    new_socket,
                    "/",
                    a_port,
                    "/",
                    an_id,
                )

                socket_list.append((new_socket, an_id))

            return socket_list
    except (Exception):
        return 1


if __name__ == "__main__":

    # output ports, cost, destination id
    output_ports = ((3001, 4001, 5001), (1, 2, 3), (3, 4, 5))
    port_opener(output_ports)

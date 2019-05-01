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
# Version 05: 18 April 2019
#   Removed the output ports - as these are not actually
#   needed, as we send routing info to the input port of
#   the destination router
#
#########################################################

import socket
from port_closer import port_closer

from routerbase import logger


def port_opener(input_ports):

    socket_list = []

    a_port = None

    try:
        for a_port in input_ports:

            new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # new_socket.setblocking(0)
            new_socket.bind(("localhost", a_port))

            logger("Opened socket / port, ", new_socket, "/", a_port)

            socket_list.append(new_socket)

        return socket_list

    except OSError:
        logger(f"The port {a_port} is already in use. Please pick another one.")
        port_closer(socket_list)
        return None


if __name__ == "__main__":

    # input ports
    input_ports = (3001, 4001, 5001)
    socket_list = port_opener(input_ports)
    logger(socket_list)

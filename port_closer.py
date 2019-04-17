#########################################################
#
# A function to close ports / sockets
#
# Version 01: 17 April 2019
#   First pass
#  
# Version 02:
#   Return codes:
#   1 => error closing input ports
#   2 => error closing output ports
#   3 => error closing input and output ports
#                                         
#########################################################

import socket
import sys

ERROR_CODE = 0

def port_closer(input_sockets, output_sockets):

        
    for a_socket, in input_sockets:
        try:
            a_socket.close()
        except:
            ERROR_CODE = 1

    for a_socket,an_id in output_sockets:
        try:
            a_socket.close()
        except:
            if (ERROR_CODE == 1):
                ERROR_CODE = 3
            else
                ERROR_CODE = 2

    return(ERROR_CODE)


if __name__ == "__main__":

    # input ports
    input_ports (1033,1044,1055)
    # output ports, cost, destination id
    output_ports = ( (3001, 4001, 5001),(1,2,3),(3,4,5) )

    port_closer(input_ports,output_ports)
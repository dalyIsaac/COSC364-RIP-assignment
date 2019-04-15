#########################################################
#                                                       #
# A function to validate that the data from the config  #
#   config file is valid. Will print an error message   #
#   and exit program                                    #
#                                                       #
# Version 01 16 April 2019                              #
#   First pass                                          #
#   Help from ID for the checking a set length idea     #
#   Needs checking output ports, metric                 #
#########################################################

import sys
import os

def validate_data(router_id, input_ports, output_ports, timers)

    #Router ID limits
    MIN_ID = 1
    MAX_ID = 64000
    ID_ERROR = 0

    #Input / Output port limits
    MIN_PORT = 1024
    MAX_PORT = 64000
    INPUT_PORT_ERROR = 0

    #Metric limits
    MIN_METRIC = 1
    MAX_METRIC = 15
    INFINITY = 16
    METRIC_ERROR = 0

    #Timer ratios
    PERIODIC_DEAD_RATIO = 6
    PERIODIC_GARBAGE_RATIO = 4
    TIMERS_ERROR = 0

    #Check Router ID
    temp_ID_set = set()
    for an_id in (router_id)
        if (an_id < MIN_ID) or (an_id > MAX_ID)
            ID_ERROR = 1
            break
        temp_ID_set.add(an_id)
    if (len(temp_ID_set) != len(router_id))
        ID_ERROR = 1

    if (ID_ERROR == 1)
        sys.exit("Router ID Configuration Error")

    #Check input ports
    temp_input_set = set()
    for a_port in (input_ports)
        if (a_port < MIN_PORT) or (a_port > MAX_PORT)
            INPUT_PORT_ERROR = 1
            break
        temp_input_set.add(a_port)                        #add port to a temporary list
    if (len(temp_input_set) != len(input_ports))          #error if length temporary list
        INPUT_PORT_ERROR = 1                              #   not same as length port list 

    if (INPUT_PORT_ERROR == 1)
        sys.exit("Input Ports Configuration Error")

    #Check output ports


    #Check Timers
    if ( (timers(1) / timers(0) != PERIODIC_DEAD_RATIO)
        TIMERS_ERROR = 1
    if ( (timers(2) / timers(0) != PERIODIC_GARBAGE_RATIO)
        TIMERS_ERROR = 1

    if (TIMERS_ERROR == 1)
        sys.exit("Timers Configuration Error")



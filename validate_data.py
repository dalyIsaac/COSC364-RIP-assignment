#########################################################
#
# A function to validate that the data from the config
#   config file is valid. Will print an error message
#   and exit program
#
# Version 01 16 April 2019
#   First pass
#   Help from ID for the checking a set length idea
#   Needs checking output ports, metric
#   Design decision to seperate the config file parser
#    and validation of the read data
#
# Version 02
#   reference material https://www.programiz.com/
# python-programming/methods/set/isdisjoint                                                    #
#########################################################

import sys
import os


def validate_data(router_id, input_ports, output_ports, timers):

    # Router ID limits
    MIN_ID = 1
    MAX_ID = 64000
    ID_ERROR = 0

    # Input / Output port limits
    MIN_PORT = 1024
    MAX_PORT = 64000
    INPUT_PORT_ERROR = 0
    OUTPUT_PORT_ERROR = 0

    # Metric limits
    MIN_METRIC = 1
    MAX_METRIC = 15
    INFINITY = 16
    METRIC_ERROR = 0

    # Timer ratios
    PERIODIC_DEAD_RATIO = 6
    PERIODIC_GARBAGE_RATIO = 4
    TIMERS_ERROR = 0

    # Check Router ID
    temp_ID_set = set()
    for an_id in router_id:
        if (an_id < MIN_ID) or (an_id > MAX_ID):
            ID_ERROR = 1
            break
        temp_ID_set.add(an_id)
    if len(temp_ID_set) != len(router_id):
        ID_ERROR = 1

    if ID_ERROR == 1:
        print("Router ID Configuration Error")
        return 1

    # Check input ports
    temp_input_set = set()
    for a_port in input_ports:
        if (a_port < MIN_PORT) or (a_port > MAX_PORT):
            INPUT_PORT_ERROR = 1
            break
        temp_input_set.add(a_port)  # add port to a temporary list
    if len(temp_input_set) != len(input_ports):  # error if length temporary list
        INPUT_PORT_ERROR = 1  #   not same as length port list

    if INPUT_PORT_ERROR == 1:
        print("Input Ports Configuration Error")
        return 1

    # Check output ports
    temp_output_set = set()
    temp_metric_set = set()
    temp_id_set = set()

    # item 0 is list of output ports
    for a_port in output_ports(0):
        if (a_port < MIN_PORT) or (a_port > MAX_PORT):
            OUTPUT_PORT_ERROR = 1
            break
        temp_output_set.add(a_port)
    if len(temp_output_set) != len(output_ports(0)):
        OUTPUT_PORT_ERROR = 1

    # check the set of output ports with set of input ports, if they
    # are not disjoint (i.e. element(s) in common) we have error
    if temp_output_set.isdisjoint(temp_input_set) == False:
        OUTPUT_PORT_ERROR = 1

    if OUTPUT_PORT_ERROR == 1:
        print("Output Ports Configuration Error")
        return 1

    # item 1 is list of costs or metrics
    for a_metric in output_ports(1):
        if (a_metric < MIN_METRIC) or (a_metric > MAX_METRIC):
            METRIC_ERROR = 1
            break
        temp_metric_set.add(a_metric)
    if len(temp_metric_set) != len(output_ports(1)):
        METRIC_ERROR = 1

    if METRIC_ERROR == 1:
        print("Cost / Metric Configuration Error")
        return 1

    # item 2 is list of destinaton router ID's

    # Check Timers
    if (timers(1) / timers(0)) != PERIODIC_DEAD_RATIO:
        TIMERS_ERROR = 1
    if (timers(2) / timers(0)) != PERIODIC_GARBAGE_RATIO:
        TIMERS_ERROR = 1

    if TIMERS_ERROR == 1:
        print("Timers Configuration Error")
        return 1


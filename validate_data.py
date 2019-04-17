#########################################################
#
# A function to validate that the data from the config
#   file is valid. Will print an error message,
#   and return an error code to calling program
#
# Version 01; 16 April 2019
#   First pass
#   Help from ID for the checking a set length idea
#   Needs checking output ports, metric
#   Design decision to seperate the config file parser
#    and validation of the read data
#
# Version 02;
#   reference material https://www.programiz.com/
# python-programming/methods/set/isdisjoint
#   Fixed a bunch of for and if statement format errors
#
# Version 03: 17April 2019
#   more tidy up
#
# Version 04: 18 April 2019
#   work on addtional validation
#   changed error constants to variables - they are not
#   constants, just variables and initialisation, and
#   moved into module defintition
#
#########################################################

# import sys
# import os

# Router ID limits
MIN_ID = 1
MAX_ID = 64000

# Input / Output port limits
MIN_PORT = 1024
MAX_PORT = 64000

# Metric limits
MIN_METRIC = 1
MAX_METRIC = 15
INFINITY = 16

# Timer ratios
PERIODIC_DEAD_RATIO = 6
PERIODIC_GARBAGE_RATIO = 4


def validate_data(router_id, input_ports, output_ports, timers):

    id_error = 0
    input_port_error = 0
    output_port_error = 0
    metric_error = 0
    timers_error = 0

    # Check Router ID
    temp_ID_set = set()
    for an_id in router_id:
        if (an_id < MIN_ID) or (an_id > MAX_ID):
            id_error = 1
            break
        temp_ID_set.add(an_id)
    if len(temp_ID_set) != len(router_id):
        id_error = 1

    if id_error == 1:
        print("Router ID Configuration Error")
        return 1

    # Check input ports
    temp_input_set = set()
    for a_port in input_ports:
        if (a_port < MIN_PORT) or (a_port > MAX_PORT):
            input_port_error = 1
            break
        temp_input_set.add(a_port)  # add port to a temporary list

    # set error error if the length of temporary list
    #   is not the same as length of original port list
    if len(temp_input_set) is not len(input_ports):
        input_port_error = 1

    if input_port_error == 1:
        print("Input Ports Configuration Error")
        return 1

    # Check output ports
    temp_output_set = set()
    temp_metric_set = set()
    temp_id_set = set()

    # item(0) is list of output ports
    for a_port in output_ports(0):
        if (a_port < MIN_PORT) or (a_port > MAX_PORT):
            output_port_error = 1
            break
        temp_output_set.add(a_port)
    if len(temp_output_set) != len(output_ports(0)):
        output_port_error = 1

    # check the set of output ports with set of input ports, if they
    # are not disjoint (i.e. element(s) in common) we have error
    if (temp_output_set.isdisjoint(temp_input_set)) is False:
        output_port_error = 1

    if output_port_error == 1:
        print("Output Ports: Port re-use Configuration Error")
        return 1

    # item(1) is list of costs or metrics
    for a_metric in output_ports(1):
        if (a_metric < MIN_METRIC) or (a_metric > MAX_METRIC):
            metric_error = 1
            break
        temp_metric_set.add(a_metric)
    if len(temp_metric_set) != len(output_ports(1)):
        metric_error = 1

    if metric_error == 1:
        print("Output Ports: Cost / Metric Configuration Error")
        return 1

    # item(2) is list of destinaton router ID's
    for an_id in output_ports(2):
        if (an_id < MIN_ID) or (an_id > MAX_ID):
            id_error = 1
            break
        temp_id_set.add(an_id)
    if len(temp_metric_set) != len(output_ports(2)):
        id_error = 1

    if id_error == 1:
        print("Output Ports: ID Configuration Error")
        return 1

    # Check Timers
    if (timers(1) / timers(0)) != PERIODIC_DEAD_RATIO:
        timers_error = 1
    if (timers(2) / timers(0)) != PERIODIC_GARBAGE_RATIO:
        timers_error = 1

    if timers_error == 1:
        print("Timers Configuration Error")
        return 1

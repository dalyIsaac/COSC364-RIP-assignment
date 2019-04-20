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
# Version 03: 17 April 2019
#   more tidy up
#
# Version 04: 18 April 2019
#   work on addtional validation
#   changed error constants to variables - they are not
#   constants, just variables and initialisation, and
#   moved into module defintition
#
#  Version 05:
#   Adding doc tests:
#   Router ID = sort of OK
#   Moved the output-ports checking (port, metric, id)
#   into signle for loop
#
# Version 06: 19 April 2019
#   Removed the metric set (since we can have the same
#   metric more than once) and checkng of it. All we
#   need to check is the metric range is 1-15.
#   Fixed issue with timer checking.
#   Move the port reuse error code check to after the
#   metric and id error code checks. (When break out of
#   the for loop, the sets do not match)
#   Need to check for empty lists being passed in
#
# Version 07: 19 April 2019:
#   Switched to returning Boolean values
#
# Version 08: 20 April 2019:
#   Moved doctests to their own unit test module
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
INFINITY = 16
MIN_METRIC = 1
MAX_METRIC = INFINITY

# Timer ratios
PERIODIC_DEAD_RATIO = 6
PERIODIC_GARBAGE_RATIO = 4


def validate_data(router_id, input_ports, output_ports, timers):
    id_error = 0
    input_port_error = 0
    output_port_error = 0
    metric_error = 0
    timers_error = 0
    # temp_metric_list = None
    # temp_id_list = None
    # temp_metric_list = None

    #
    # Check Router ID
    if router_id is None:
        id_error = 1
    else:
        if (router_id < MIN_ID) or (router_id > MAX_ID):
            id_error = 1

        if id_error == 1:
            print("Router ID Configuration Error")
            return False

    # Check input ports
    temp_input_set = set()
    if input_ports is None:
        input_port_error = 1
    else:
        for a_port in input_ports:
            if (a_port < MIN_PORT) or (a_port > MAX_PORT):
                input_port_error = 1
                break
            temp_input_set.add(a_port)  # add port to a temporary list

    # set error error if the length of temporary list
    #   is not the same as length of original port list
    if len(temp_input_set) != len(input_ports):
        input_port_error = 1

    if input_port_error == 1:
        print("Input Ports Configuration Error")
        return False

    #
    # Check output ports
    temp_output_port_set = set()
    temp_id_set = set()
    # temp_metric_set = set()

    if output_ports is None:
        print("Output Ports Configuration Error: No output ports were given")
        return False
    else:
        # an_item is (output port,metric,id)
        for an_item in output_ports:

            # check port range
            if (an_item[0] < MIN_PORT) or (an_item[0] > MAX_PORT):
                print("Output Ports Configuration Error: Port out of range")
                return False
                break
            temp_output_port_set.add(an_item[0])

            # check metric
            if (an_item[1] < MIN_METRIC) or (an_item[1] > MAX_METRIC):
                metric_error = 1
                break
            # temp_metric_set.add(an_item[1])

            # check id
            if (an_item[2] < MIN_ID) or (an_item[2] > MAX_ID):
                id_error = 1
                break
            temp_id_set.add(an_item[2])

    # if length of set of ports not same as the length of output-ports, hv error
    if len(temp_output_port_set) != len(output_ports):
        output_port_error = 1

    # check the set of output ports with set of input ports, if they
    # are not disjoint (i.e. element(s) in common) we have error
    if (temp_output_port_set.isdisjoint(temp_input_set)) is False:
        output_port_error = 1

    if metric_error == 1:
        print("Output Ports Configuration Error: Cost / Metric")
        return False

    # we might need this i.e. check if a cost / metric is missing?
    # if len(temp_metric_set) != len(output_ports(2)):
    # id_error = 1

    # do we need a check for missing ID?
    if id_error == 1:
        print("Output Ports Configuration Error: ID")
        return False

    if output_port_error == 1:
        print("Output Ports Configuration Error: Port number re-use")
        return False

    #
    # Check Timers
    if len(timers) != 3:
        timers_error = 1
    else:
        if (timers[1] / timers[0]) != PERIODIC_DEAD_RATIO:
            timers_error = 1
        if (timers[2] / timers[0]) != PERIODIC_GARBAGE_RATIO:
            timers_error = 1

    if timers_error == 1:
        print("Timers Configuration Error")
        return False

    # All good, yay! return a zero
    return True

################################################################################
# 2019_03_06
# Manu Hamblyn
# 95140875
# my_starter.py
# code to parse a text configuration file and put contents into a Dict
#
# v0_1
# Very simple test program to get to grips with Python text parsing
# Initial test code derived from:
# https://stackabuse.com/read-a-file-line-by-line-in-python/
# and
# https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
# and
# https://stackoverflow.com/questions/1706198/python-how-to-ignore-comment-lines-when-reading-in-a-file
#
# v0_2
# getting required data need to remove newline characters and put data into
#  variables (ID and timers,
#  list for input, table/dict for output)
# https://stackoverflow.com/questions/6213063/python-read-next
#
# v0_3
# poc_parser.py
# Guidance, support and sample code provided by jps111.
# Reads complete config file since size is small.
# Uses join and split operations on lines.
#
# v04: 18 April 2019
# Fixed some linting errors
#
# v05: 19 April 2019
# Bug fix: Changed id = int(cost) to id = int(id)
#
# v06: 20 April 2019
# Made pyright happy by changing variable names, thus fixing typing inference
################################################################################

from routerbase import logger


def read_config(filename):
    f = open(filename)
    router_id = None
    input_ports = None
    output_ports = None
    timers = None

    # read whole line
    for line in f.readlines():  # iterate through the lines in file
        option = line.split(" ")[
            0
        ].strip()  # if line starts with whitespce strip line
        values = " ".join(
            line.split(" ")[1:]
        )  # join lines togther to just have text
        if option == "router-id":
            if router_id is not None:
                logger("multiple router-id lines")
                break

            router_id = int(values.strip())

        elif option == "input-ports":
            # check if we have already set input-ports
            if input_ports is not None:
                logger("multiple input-ports lines")
                break

            input_ports = []
            parts = values.split(
                ","
            )  # seperate the line into parts, using comma
            for port_str in parts:  # iterate through the parts
                port = int(port_str.strip())  # remove whitespace
                input_ports.append(port)  # append to list

        elif option == "output-ports":
            if output_ports is not None:
                logger("multiple output-ports lines")
                break

            output_ports = []
            parts = values.split(",")
            for part in parts:
                part = part.strip()
                (port_str, cost, curr_id) = part.split(
                    "-"
                )  # further split by hyphen
                port_str = int(port_str)
                cost = int(cost)
                curr_id = int(curr_id)  # fixed error here
                output_ports.append((port_str, cost, curr_id))
        elif option == "timers":
            if timers is not None:
                logger("multiple timers lines")
                break

            timers = []
            parts = values.split(",")
            for port_str in parts:
                port = int(port_str.strip())
                timers.append(port)
    f.close()
    return (router_id, input_ports, output_ports, timers)


if __name__ == "__main__":

    try:
        (router_id, input_ports, output_ports, timers) = read_config("R2.cfg")
        logger("router-id", router_id)
        logger("input-ports", input_ports)
        logger("output-ports", output_ports)
        logger("timers", timers)
    except (Exception):
        logger("An error occurred")

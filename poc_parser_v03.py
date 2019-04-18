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
# Grateful for help from jps111
# Reads complete config file since size is small
# Uses join and split operations on lines
#
# v04: 18 April 2019
# Fixed some linting errors
#
################################################################################


def read_config(filename):
    f = open(filename)
    router_id = None
    input_ports = None
    output_ports = None
    timers = None

    for line in f.readlines():
        option = line.split(" ")[0].strip()
        values = " ".join(line.split(" ")[1:])
        if option == "router-id":
            if router_id is not None:
                print("multiple router-id lines")
                break

            router_id = int(values[0].strip())

        elif option == "input-ports":
            # check if we have already set input-ports
            if input_ports is not None:
                print("multiple input-ports lines")
                break

            input_ports = []
            parts = values.split(",")
            for port in parts:
                port = int(port.strip())
                input_ports.append(port)

        elif option == "output-ports":
            if output_ports is not None:
                print("multiple output-ports lines")
                break

            output_ports = []
            parts = values.split(",")
            for part in parts:
                part = part.strip()
                (port, cost, id) = part.split("-")
                port = int(port)
                cost = int(cost)
                id = int(cost)
                output_ports.append((port, cost, id))
        elif option == "timers":
            if timers is not None:
                print("multiple timers lines")
                break

            timers = []
            parts = values.split(",")
            for port in parts:
                port = int(port.strip())
                timers.append(port)
    f.close()
    return (router_id, input_ports, output_ports, timers)


if __name__ == "__main__":

    try:
        (router_id, input_ports, output_ports, timers) = read_config("R2.cfg")
        print("router-id", router_id)
        print("input-ports", input_ports)
        print("output-ports", output_ports)
        print("timers", timers)
    except (Exception):
        print("An error occurred")

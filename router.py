import sys
from datetime import datetime
from socket import socket
from typing import List, Tuple

import routerbase
from input_processing import input_processing
from output_processing import deletion_process, send_response, send_responses
from packet import construct_packets
from poc_parser_v03 import read_config
from port_closer import port_closer
from port_opener import port_opener
from routingtable import RoutingTable
from validate_data import validate_data


def daemon(table: RoutingTable, sockets: List[socket], output_sock: socket):
    """Main body of the router."""
    while True:
        while table.sched_update_time > datetime.now():
            input_processing(table, sockets)

        send_responses(table, output_sock)
        table.update_sched_update_time()

        deletion_process(table, output_sock)


def create_table(
    router_id: int,
    sockets: List[socket],
    output_ports: List[Tuple[int, int, int]],
    timers: List[int],
):
    """
    Creates the routing table, and saves the information from the config file,
    so that it can be easily be accessed later from a single place.
    """
    update_time, timeout_time, gc_time, *extra = timers
    table = RoutingTable(router_id, update_time, timeout_time, gc_time)

    for port, cost, neighbour_router_id in output_ports:
        table.add_config_data(neighbour_router_id, port, cost)

    return table


def startup(table: RoutingTable, output_sock: socket):
    """Upon startup, it immediately sends out packets to neighbours."""
    routerbase.logger("Starting up...")
    for router_id in table.config_table:
        packets = construct_packets(table, router_id)
        for packet in packets:
            port = table.config_table[router_id].port
            send_response(output_sock, port, packet)


def get_params():
    """Gets the filename and logging level from the command line arguments."""
    if len(sys.argv) < 2:
        raise IndexError
    filename = sys.argv[1]
    is_debug = False
    if len(sys.argv) >= 3 and sys.argv[2].lower() == "debug":
        is_debug = True
    return filename, is_debug


def main():
    sockets: List[socket] = []
    try:
        filename, is_debug = get_params()
        routerbase.DEBUG_MODE = is_debug

        (router_id, input_ports, output_ports, timers) = read_config(filename)
        if not validate_data(router_id, input_ports, output_ports, timers):
            return

        result = port_opener(input_ports)

        if result is None:
            return
        else:
            sockets = result

        if len(sockets) == 0:
            routerbase.logger("No sockets were opened.")
            return

        # first open socket is chosen to be the output socket
        output_sock: socket = sockets[0]

        table = create_table(router_id, sockets, output_ports, timers)
        startup(table, output_sock)
        daemon(table, sockets, output_sock)

    except IndexError:
        routerbase.logger("Please give a filename. Correct")
    except FileNotFoundError:
        routerbase.logger("Please give a valid filename")
    except KeyboardInterrupt:
        routerbase.logger("\nKeyboard interrupt detected.")
    except Exception:
        routerbase.logger("Something bad happened.")
    finally:
        routerbase.logger("Router shutting down.")
        port_closer(sockets)
        routerbase.logger("Bye!")


if __name__ == "__main__":
    main()

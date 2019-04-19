import sys
from datetime import datetime
from socket import socket
from typing import List, Tuple

from input_processing import input_processing
from output_processing import deletion_process, send_responses
from poc_parser_v03 import read_config
from port_closer import port_closer
from port_opener import port_opener
from routeentry import RouteEntry
from routingtable import RoutingTable
from validate_data import validate_data


def daemon(table: RoutingTable, sockets: List[socket]):
    """Main body of the router."""
    if len(sockets) == 0:
        print("No sockets were opened.")
        return

    # first open socket is chosen to be the output socket
    output_sock: socket = sockets[0]

    while True:
        while table.sched_update_time < datetime.now():
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
    update_time, timeout_time, gc_time = timers
    table = RoutingTable(router_id, update_time, timeout_time, gc_time)

    for port, cost, neighbour_router_id in output_ports:
        route = RouteEntry(port, cost, neighbour_router_id, timeout_time)
        table.add_route(neighbour_router_id, route)

    return table


def main():
    sockets: List[socket] = []
    try:
        filename = sys.argv[1]
        (router_id, input_ports, output_ports, timers) = read_config(filename)
        if not validate_data(router_id, input_ports, output_ports, timers):
            return

        result = port_opener(input_ports)

        if result is None:
            return

        table = create_table(router_id, sockets, output_ports, timers)
        daemon(table, sockets)

    except IndexError:
        print("Please give a filename.")
    except FileNotFoundError:
        print("Please give a valid filename")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected.")
    except OSError:
        print("")
    finally:
        print("Router shutting down.")
        port_closer(sockets)
        print("Bye!")
    # sys.exit()


if __name__ == "__main__":
    main()

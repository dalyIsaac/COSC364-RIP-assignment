from datetime import datetime
from socket import socket
import sys
from typing import List

from input_processing import input_processing
from output_processing import deletion_process, send_responses
from port_closer import port_closer
from routingtable import RoutingTable


def daemon(table: RoutingTable, sockets: List[socket]):
    """Main body of the router."""
    try:
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
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected.")
    finally:
        print("Router shutting down.")
        port_closer(sockets)
        print("Bye!")
        sys.exit()

from datetime import datetime
from socket import socket
from typing import List

from input_processing import input_processing
from output_processing import deletion_process, send_responses
from routingtable import RoutingTable


def daemon(table: RoutingTable, sockets: List[socket]):
    """Main body of the router."""
    while True:
        while table.sched_update_time < datetime.now():
            input_processing(table, sockets)

        send_responses(table)
        table.update_sched_update_time()

        deletion_process(table)

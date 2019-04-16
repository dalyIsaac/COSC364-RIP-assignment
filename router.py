from routingtable import RoutingTable
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from packet import construct_packets


def deletion_process():
    """
    Handles the timeout and garbage collection timer processing for the
    routing table
    """
    # TODO
    pass


def send_response(table: RoutingTable, router_id: int, packet: bytearray):
    """
    Sends a `Response` packet to the given `router_id`.
    """
    # TODO
    pass


def send_responses(table: RoutingTable):
    """
    Sends unsolicited `Response` messages containing the entire routing
    table to every neighbouring router.
    """
    for router_id in table:
        packets = construct_packets(table, router_id)
        for packet in packets:
            send_response(table, router_id, packet)


def daemon(table: RoutingTable):
    """Main body of the router."""
    pool = ThreadPoolExecutor()

    while True:
        while table.sched_update_time < datetime.now():
            # TODO: input processing here
            pass 

        pool.submit(send_responses, (table))
        table.update_sched_update_time()

        # TODO: deletion processing here

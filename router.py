from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from packet import construct_packets
from routingtable import RoutingTable
from routeentry import RouteEntry
from validate_data import INFINITY

pool = ThreadPoolExecutor()


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


def triggered_update():
    """Sends a triggered update."""
    # TODO
    pass


def timeout_processing(table: RoutingTable, entry: RouteEntry):
    """Starts processing for the timeout timer."""
    entry.set_garbage_collection_time(table.gc_delta)
    entry.metric = INFINITY
    entry.flag = True

    now = datetime.now()
    can_update = table.set_triggered_update_time(now)

    # Suppresses the update if another triggered update has been sent
    if can_update:
        # Send triggered updates
        triggered_update()


def deletion_process(table: RoutingTable):
    """
    Handles the timeout and garbage collection timer processing for the
    routing table.
    """
    now = datetime.now()  # Only calling it once minimises system time
    for router_id in table:
        entry: RouteEntry = table[router_id]
        if entry.timeout_time <= now:
            pool.submit(timeout_processing, (entry))
        elif entry.gc_time is not None and entry.gc_time <= now:
            # TODO: garbage collection processing
            pass


def daemon(table: RoutingTable):
    """Main body of the router."""
    while True:
        while table.sched_update_time < datetime.now():
            # TODO: input processing here
            pass

        pool.submit(send_responses, (table))
        table.update_sched_update_time()

        deletion_process(table)

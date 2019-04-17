from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from packet import construct_packets
from routeentry import RouteEntry
from routingtable import RoutingTable
from validate_data import INFINITY

pool = ThreadPoolExecutor()


def send_response(table: RoutingTable, router_id: int, packet: bytearray):
    """
    Sends a `Response` packet to the given `router_id`.
    """
    # TODO
    pass


def _send_responses(table: RoutingTable):
    for router_id in table:
        packets = construct_packets(table, router_id)
        for packet in packets:
            send_response(table, router_id, packet)


def send_responses(table: RoutingTable):
    """
    Sends unsolicited `Response` messages containing the entire routing
    table to every neighbouring router.
    """
    pool.submit(_send_responses, (table))


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
        pool.submit(send_responses, (table))


def gc_processing(
    table: RoutingTable, router_id: int, entry: RouteEntry, now: datetime
):
    """Starts processing for the garbage collection timer."""
    ids_to_delete = []

    if router_id in table and entry.gc_time and entry.gc_time >= now:
        ids_to_delete.append(router_id)

    for current_id in ids_to_delete:
        try:
            del table[router_id]
        except KeyError:
            print(f"router-id {router_id} wasn't in the table at this time.")


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
        elif entry.gc_time is not None:
            gc_processing(table, router_id, entry, now)

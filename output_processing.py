from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from socket import socket

from packet import construct_packets
from routeentry import RouteEntry
from routingtable import RoutingTable
from validate_data import INFINITY

pool = ThreadPoolExecutor()


def send_response(
    table: RoutingTable, sock: socket, router_id: int, packet: bytearray
):
    """
    Sends a `Response` packet to the given `router_id`.
    """
    # Ignore the pyright error - it fails to resolve bytearray and bytes, when
    # it really should.
    sock.sendto(packet, ("localhost", table[router_id].port))


def _send_responses(table: RoutingTable, sock: socket, clear_flags=False):
    print(str(table))
    for router_id in table:
        packets = construct_packets(table, router_id)
        for packet in packets:
            send_response(table, sock, router_id, packet)

    if clear_flags:
        for router_id in table:
            entry: RouteEntry = table[router_id]
            entry.flag = False


def send_responses(table: RoutingTable, sock: socket, clear_flags=False):
    """
    Sends unsolicited `Response` messages containing the entire routing
    table to every neighbouring router.
    """
    pool.submit(_send_responses, table, sock, clear_flags)


def timeout_processing(table: RoutingTable, entry: RouteEntry, sock: socket):
    """Starts processing for the timeout timer."""
    entry.set_garbage_collection_time(table.gc_delta)
    entry.metric = INFINITY
    entry.flag = True

    now = datetime.now()
    can_update = table.set_triggered_update_time(now)

    # Suppresses the update if another triggered update has been sent
    if can_update:
        # Send triggered updates
        send_responses(table, sock, True)


def gc_processing(
    table: RoutingTable, router_id: int, entry: RouteEntry, now: datetime
):
    """Starts processing for the garbage collection timer."""
    ids_to_delete = []

    if router_id in table and entry.gc_time and entry.gc_time >= now:
        ids_to_delete.append(router_id)
        del table[router_id]


def deletion_process(table: RoutingTable, sock: socket):
    """
    Handles the timeout and garbage collection timer processing for the
    routing table.
    """
    now = datetime.now()  # Only calling it once minimises system time
    for router_id in table:
        entry: RouteEntry = table[router_id]
        if hasattr(entry, "gc_time"):
            gc_processing(table, router_id, entry, now)
        elif entry.timeout_time <= now:
            pool.submit(timeout_processing, table, entry, sock)

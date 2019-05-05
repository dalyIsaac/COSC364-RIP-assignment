from datetime import datetime
from socket import socket
from typing import Optional

from packet import construct_packets
from routeentry import RouteEntry
from routerbase import logger, pool
from routingtable import RoutingTable
from validate_data import INFINITY


def send_response(sock: socket, port: int, packet: bytearray):
    """
    Sends a `Response` packet to the given `router_id`.
    """
    # Ignore the pyright error - it fails to resolve bytearray and bytes, when
    # it really should.
    sock.sendto(packet, ("localhost", port))


def _send_responses(table: RoutingTable, sock: socket, clear_flags=False):
    logger(str(table))
    for router_id in table:
        if router_id in table.config_table:
            packets = construct_packets(table, router_id)
            port = table.config_table[router_id].port
            for packet in packets:
                logger(
                    f"Sending to router_id {router_id} port {port} ",
                    is_debug=True,
                )
                send_response(sock, port, packet)

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
    logger("About to set gc time", is_debug=True)
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
    if (
        router_id in table
        and entry.gc_time is not None
        and entry.gc_time <= now
    ):
        logger(f"Deleting router id {router_id}", is_debug=True)
        del table[router_id]


def deletion_process(
    table: RoutingTable, sock: socket, new_infinite_id: Optional[int] = None
):
    """
    Handles the timeout and garbage collection timer processing for the
    routing table.
    """
    logger("In deletion process", is_debug=True)
    logger(f"New infinite id is {new_infinite_id}", is_debug=True)
    now = datetime.now()  # Only calling it once minimises system time
    for router_id in table:
        logger(f"Current router id is {router_id}", is_debug=True)
        entry: RouteEntry = table[router_id]
        if entry.gc_time is not None:
            logger(
                f"About to go into GC processing for router {router_id}",
                is_debug=True,
            )
            gc_processing(table, router_id, entry, now)
        elif entry.timeout_time <= now or router_id == new_infinite_id:
            logger(
                f"About to go into timeout processing for router {router_id}",
                is_debug=True,
            )
            pool.submit(timeout_processing, table, entry, sock)

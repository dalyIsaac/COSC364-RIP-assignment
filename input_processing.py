from datetime import datetime, timedelta
from select import select
from socket import socket
from typing import List, Tuple

from packet import ResponseEntry, ResponsePacket, read_packet, validate_packet
from routeentry import RouteEntry
from routingtable import RoutingTable
from validate_data import INFINITY, MAX_ID, MIN_ID
from output_processing import pool, deletion_process, send_responses

MIN_METRIC = 1
MAX_METRIC = INFINITY


def validate_entry(entry: ResponseEntry) -> bool:
    """Validates an individual router entry."""

    # Checks for the router_id
    if entry.router_id < MIN_ID or entry.router_id > MAX_ID:
        print(
            f"The entries router id of {entry.router_id} should be an integer "
            + "between {MIN_ID} and {MAX_ID}, inclusive."
        )
        return False

    # Checks that the entry's metric is between the expected minimum and
    # maximum metric.
    if entry.metric < MIN_METRIC or entry.metric > MAX_METRIC:
        print(
            f"The entry's metric of {entry.metric} was not between the expected"
            + " range of {MIN_METRIC} and {MAX_METRIC}, inclusive."
        )
        return False

    return True


def add_route(
    table: RoutingTable,
    response: ResponseEntry,
    metric: int,
    port: int,
    learned_from: int,
    sock: socket,
):
    """
    Adds a newly learned route to the routing table.
    """
    entry = RouteEntry(
        port, metric, learned_from, table.timeout_delta, learned_from
    )
    entry.gc_time = None
    entry.flag = True
    table.add_route(response.router_id, entry)
    send_responses(table, sock)


def adopt_route(
    table: RoutingTable,
    entry: RouteEntry,
    new_metric: int,
    learned_from: int,
    sock: socket,
):
    """
    Adopts the newly received route, and updates the existing routing table
    entry.
    """
    entry.metric = new_metric
    entry.next_address = learned_from
    entry.flag = True
    send_responses(table, sock)
    if new_metric == INFINITY:
        pool.submit(deletion_process, (table))
    else:
        entry.update_timeout_time(table.timeout_delta)


def update_table(
    table: RoutingTable,
    response: ResponseEntry,
    new_metric: int,
    learned_from: int,
    sock: socket,
):
    """
    Goes through the process of updating the routing table with the new route,
    if applicable.
    """
    entry: RouteEntry = table[response.router_id]

    if (
        learned_from == entry.next_address and new_metric != entry.metric
    ) or new_metric < entry.metric:
        adopt_route(table, entry, new_metric, learned_from, sock)
    elif new_metric == INFINITY:
        # nothing happens if the entry's existing metric is `INFINITY`
        if entry.metric != INFINITY:
            pool.submit(deletion_process, (table))
    elif new_metric == entry.metric and learned_from != entry.next_address:
        # Adding a check for `learned_from` means that the entyr will not be
        # updated if its the same as the old entry.

        # If the timeout for the existing route is at least halfway to the
        # expiration point, switch to the new route.
        time_diff: timedelta = entry.timeout_time - datetime.now()
        half_time = table.timeout_delta / 2
        if time_diff.seconds >= half_time:
            adopt_route(table, entry, new_metric, learned_from, sock)
    else:
        # Drop all the remaining packets
        pass


def process_entry(
    table: RoutingTable,
    entry: ResponseEntry,
    packet: ResponsePacket,
    port: int,
    sock: socket,
):
    if not validate_entry(entry):
        return

    # Update the metric
    new_metric = entry.metric + table[entry.router_id].metric
    if new_metric > INFINITY:
        new_metric = INFINITY

    if entry.router_id in table:
        update_table(table, entry, new_metric, packet.sender_router_id, sock)
    else:
        add_route(table, entry, new_metric, port, packet.sender_router_id, sock)


def get_packets(
    sockets: List[socket]
) -> List[Tuple[ResponsePacket, int, socket]]:
    """Reads received packets from the input ports/sockets."""
    read: List[socket]
    read, _, _ = select(sockets, [], [], 1)

    packets = []

    for sock in read:
        _, port = sock.getsockname()
        packet, client_address = sock.recvfrom(1024)
        packets.append((read_packet(packet), port, sock))

    return packets


def input_processing(table: RoutingTable, sockets: List[socket]):
    """
    The processing is the same, no matter why the Response was generated.
    """
    for packet, port, sock in get_packets(sockets):
        if validate_packet(table, packet):
            for entry in packet.entries:
                process_entry(table, entry, packet, port, sock)

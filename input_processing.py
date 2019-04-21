from datetime import datetime, timedelta
from select import select
from socket import AF_INET, socket
from typing import List, Tuple

from output_processing import deletion_process, pool, send_responses
from packet import ResponseEntry, ResponsePacket, read_packet, validate_packet
from routeentry import RouteEntry
from routingtable import RoutingTable
from validate_data import INFINITY, MAX_ID, MAX_METRIC, MIN_ID, MIN_METRIC


def validate_entry(packet_entry: ResponseEntry) -> bool:
    """Validates an individual router entry."""

    # Checks the entry's AFI value
    if packet_entry.afi != AF_INET:
        print(
            f"The value {packet_entry.afi} for AFI does not match the "
            f"expected value of AF_INET = {AF_INET}."
        )
        return False

    # Checks for the router_id
    if packet_entry.router_id < MIN_ID or packet_entry.router_id > MAX_ID:
        print(
            f"The entry's router id of {packet_entry.router_id} should be an "
            f"integer between {MIN_ID} and {MAX_ID}, inclusive."
        )
        return False

    # Checks that the entry's metric is between the expected minimum and
    # maximum metric.
    if packet_entry.metric < MIN_METRIC or packet_entry.metric > MAX_METRIC:
        print(
            f"The entry's metric of {packet_entry.metric} was not between the "
            f"expected range of {MIN_METRIC} and {MAX_METRIC}, inclusive."
        )
        return False

    return True


def add_route(
    table: RoutingTable,
    packet_entry: ResponseEntry,
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
    table.add_route(packet_entry.router_id, entry)

    # NOTE: As per the assignment spec, "implement triggered updates when
    # routes become invalid  (i.e. when a router sets the routes metric to
    # 16 <INFINITY> for whatever reason, compare end of page 24 and
    # beginning of 25 in [1]), not for other metric updates or new routes".
    # Thus, the following line is commented out, and the success lines added.
    # send_responses(table, sock)

    if entry.metric == INFINITY:
        send_responses(table, sock)


def adopt_route(
    table: RoutingTable,
    table_entry: RouteEntry,
    new_metric: int,
    learned_from: int,
    sock: socket,
):
    """
    Adopts the newly received route, and updates the existing routing table
    entry.
    """
    table_entry.metric = new_metric
    table_entry.next_address = learned_from
    table_entry.flag = True
    table.learned_from = learned_from

    # NOTE: As per the assignment spec, "implement triggered updates when
    # routes become invalid  (i.e. when a router sets the routes metric to
    # 16 <INFINITY> for whatever reason, compare end of page 24 and
    # beginning of 25 in [1]), not for other metric updates or new routes".
    # Thus, the following line is commented out.
    # send_responses(table, sock)

    if new_metric == INFINITY:
        # NOTE: The following line was added, so that only updates to INFINITY
        # cause triggered updates.
        send_responses(table, sock)

        pool.submit(deletion_process, table)
    else:
        table_entry.update_timeout_time(table.timeout_delta)


def update_table(
    table: RoutingTable,
    packet_entry: ResponseEntry,
    new_metric: int,
    learned_from: int,
    sock: socket,
):
    """
    Goes through the process of updating the routing table with the new route,
    if applicable.
    """
    table_entry: RouteEntry = table[packet_entry.router_id]

    if (
        learned_from == table_entry.next_address
        and new_metric != table_entry.metric
    ) or new_metric < table_entry.metric:
        adopt_route(table, table_entry, new_metric, learned_from, sock)
    elif new_metric == INFINITY:
        # nothing happens if the entry's existing metric is `INFINITY`
        if table_entry.metric != INFINITY:
            pool.submit(deletion_process, table)
    elif (
        new_metric == table_entry.metric
        and learned_from != table_entry.next_address
    ):
        # Adding a check for `learned_from` means that the entry will not be
        # updated if its the same as the old entry.

        # If the timeout for the existing route is at least halfway to the
        # expiration point, switch to the new route.
        time_diff: timedelta = table_entry.timeout_time - datetime.now()
        half_time = table.timeout_delta / 2
        if time_diff.seconds >= half_time:
            adopt_route(table, table_entry, new_metric, learned_from, sock)
    else:
        # The packet_entry is no better than the current route
        pass


def process_entry(
    table: RoutingTable,
    packet_entry: ResponseEntry,
    packet: ResponsePacket,
    port: int,
    sock: socket,
):
    if not validate_entry(packet_entry):
        return

    # Update the metric
    new_metric = packet_entry.metric + table[packet.sender_router_id].metric
    if new_metric > INFINITY:
        new_metric = INFINITY

    if packet_entry.router_id in table:
        update_table(
            table, packet_entry, new_metric, packet.sender_router_id, sock
        )
    else:
        add_route(
            table, packet_entry, new_metric, port, packet.sender_router_id, sock
        )


def get_packets(
    sockets: List[socket]
) -> List[Tuple[ResponsePacket, int, socket]]:
    """Reads received packets from the input ports/sockets."""
    read: List[socket]
    read, _, _ = select(sockets, [], [], 1)

    packets = []

    for sock in read:
        _, port = sock.getsockname()
        # bigger than the maximum packet size
        raw_packet, client_address = sock.recvfrom(1024)
        packet = read_packet(raw_packet)
        packets.append((packet, port, sock))
        print(
            f"Received packet from router_id: {packet.sender_router_id} | "
            f"port: {port}"
        )

    return packets


def input_processing(table: RoutingTable, sockets: List[socket]):
    """
    The processing is the same, no matter why the Response was generated.
    """
    for packet, port, sock in get_packets(sockets):
        if validate_packet(table, packet):
            for entry in packet.entries:
                process_entry(table, entry, packet, port, sock)

from routingtable import RoutingTable
from packet import validate_packet, ResponsePacket, ResponseEntry
from validate_data import MIN_ID, MAX_ID, INFINITY
from typing import List, Tuple
from routeentry import RouteEntry
from datetime import datetime, timedelta

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
):
    entry = RouteEntry(
        port, metric, learned_from, table.timeout_delta, learned_from
    )
    entry.gc_time = None
    entry.flag = True
    table.add_route(response.router_id, entry)
    # TODO: trigger an update


def update_table(
    table: RoutingTable,
    response: ResponseEntry,
    new_metric: int,
    learned_from: int,
):
    entry: RouteEntry = table[response.router_id]

    if (
        learned_from == entry.next_address and new_metric != entry.metric
    ) or new_metric < entry.metric:
        entry.metric = new_metric
        entry.next_address = learned_from
        entry.flag = True
        # TODO: trigger an update
        if new_metric == INFINITY:
            # TODO: start the deletion process
            pass
        else:
            entry.update_timeout_time(table.timeout_delta)
    elif new_metric == INFINITY:
        if entry.metric != INFINITY:
            # TODO: start the deletion process
            pass
    elif new_metric == entry.metric:
        # if the timeout for the existing route is at least halfway to the
        # expiration point, switch to the new route.
        time_diff: timedelta = entry.timeout_time - datetime.now()
        half_time = table.timeout_delta / 2
        if time_diff.seconds >= half_time:
            # TODO: switch to the new route
            pass
    else:
        # Drop all the remaining packets
        pass


def process_entry(
    table: RoutingTable, entry: ResponseEntry, packet: ResponsePacket, port: int
):
    if not validate_entry(entry):
        return

    # Update the metric
    new_metric = entry.metric + table[entry.router_id].metric
    if new_metric > INFINITY:
        new_metric = INFINITY

    if entry.router_id in table:
        # TODO: go through the process for updating the routing table.
        pass
    else:
        add_route(table, entry, new_metric, port, packet.sender_router_id)


def get_packets() -> List[Tuple[ResponsePacket, int]]:
    # TODO: reads received packets from the input ports
    return []


def input_processing(table: RoutingTable):
    """
    The processing is the same, no matter why the Response was generated.
    """
    for packet, port in get_packets():
        if validate_packet(table, packet):
            for entry in packet.entries:
                process_entry(table, entry, packet, port)
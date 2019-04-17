from routingtable import RoutingTable
from packet import validate_packet, ResponsePacket, ResponseEntry
from validate_data import MIN_ID, MAX_ID, INFINITY
from typing import List

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


def process_entry(table: RoutingTable, entry: ResponseEntry):
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
        # TODO: add the new route to the routing table
        pass


def get_packets() -> List[ResponsePacket]:
    # TODO: reads received packets from the input ports
    return []


def input_processing(table: RoutingTable):
    """
    The processing is the same, no matter why the Response was generated.
    """
    for packet in get_packets():
        if validate_packet(table, packet):
            for entry in packet.entries:
                process_entry(table, entry)

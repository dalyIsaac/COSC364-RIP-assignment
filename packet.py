from router import INFINITY
from routingtable import RoutingTable
from routeentry import RouteEntry
from math import ceil
from socket import AF_INET
from typing import Iterator, Tuple, Union, List, NewType

MAX_ENTRIES = 25
ENTRY_LEN = 20
HEADER_LEN = 4
RIP_PACKET_COMMAND = 2
RIP_VERSION_NUMBER = 2


def get_next_packet_entries(table: RoutingTable, router_id: int):
    """
    Gets the entries from the routing table, which can be sent to the given `router_id`. Entries which have
    a metric of less than infinity, or have a flag, and are not learned from the router to whom the packets
    are going to be sent to are added to the yielded list of entries.
    
    Keyword arguments:
    table -- The routing table, containing all of the entries.
    router_id -- The router the packet is being sent to.
    """
    entries  = []
    for destination_router_id in table:
        route = table[destination_router_id]
        if route.learned_from != router_id and (route.metric < INFINITY or route.flag):
            entries.append((destination_router_id, route))
            if len(entries) == MAX_ENTRIES:
                yield entries
                entries = []
    yield entries


def _construct_packet_header(packet: bytearray, table) -> None:
    """
    Modifies the packet's header.
    
    Keyword arguments:
    packet -- The packet who will have its header populated.
    table -- The table from whom the packet is going to be sent from. 
    """
    # the following are implicitly converted to bytes
    packet[0] = RIP_PACKET_COMMAND
    packet[1] = RIP_VERSION_NUMBER
    packet[2:4] = table.router_id.to_bytes(2, "big")


def _construct_packet(table: RoutingTable, entries, router_id) -> bytearray:
    """Constructs an individual packet, with up to 25 entries inside, with the given table entries."""
    packet = bytearray(HEADER_LEN + len(entries) * ENTRY_LEN)
    _construct_packet_header(packet, table)
    current_index = 4

    for (destination_router_id, entry) in entries:
        packet[current_index : current_index + 2] = AF_INET.to_bytes(2, "big")
        packet[current_index + 4 : current_index + 8] = destination_router_id.to_bytes(4, "big")
        packet[current_index + 16 : current_index + ENTRY_LEN] = entry.metric.to_bytes(4, "big")
        current_index += ENTRY_LEN

    return packet


def construct_packets(table: RoutingTable, router_id: int) -> List[bytearray]:
    """Constructs packets to send to a `router_id`, from the routing table."""
    packets: List[bytearray] = []

    for entries in get_next_packet_entries(table, router_id):
        packets.append(_construct_packet(table, entries, router_id))

    return packets

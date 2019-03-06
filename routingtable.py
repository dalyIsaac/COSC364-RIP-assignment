from typing import Dict
from routeentry import RouteEntry


class RoutingTable:
    table: Dict[int, RouteEntry]

    def __init__(self):
        self.table = {}

    def __len__(self):
        """Returns the length of the routing table"""
        return len(self.table)

    def __iter__(self):
        """Iterates over the items in the routing table"""
        return iter(self.table.keys())

    def __getitem__(self, index: int):
        """Returns a specific item in the routing table"""
        return self.table[index]

    def add_route(self, router_id: int, route: RouteEntry) -> None:
        """Adds the route to the table"""
        self.table[router_id] = route

    def remove_route(self, router_id: int) -> None:
        """Removes the route from the table."""
        del self.table[router_id]

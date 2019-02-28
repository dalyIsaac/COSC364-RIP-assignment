from typing import Dict
from route import Route


class RoutingTable:
    table: Dict[int, Route]

    def __init__(self):
        table = {}

    def add_route(self, router_id: int, route: Route) -> None:
        """Adds the route to the table"""
        self.table[router_id] = route

    def remove_route(self, router_id: int) -> None:
        """Removes the route from the table."""
        del self.table[router_id]


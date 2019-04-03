from typing import Dict

from routeentry import RouteEntry


class RoutingTable:
    """
    Contains all of the entries for the routing table, for this router.

    Instance variables:
    table -- Contains the routing table, in the form of `{[key: router_id]: RouteEntry}`.
    router_id -- The router of this router.
    """
    table: Dict[int, RouteEntry]

    def __init__(self, router_id):
        self.table = {}
        self.router_id = router_id

    def __len__(self):
        """Returns the number of items inside the routing table"""
        return len(self.table)

    def __iter__(self):
        """Iterates over the `RouteEntry` items in the routing table"""
        return iter(self.table.keys())

    def __getitem__(self, index: int):
        """Returns a specific `RouteEntry` in the routing table, given its `router_id`"""
        return self.table[index]

    def add_route(self, router_id: int, route: RouteEntry) -> None:
        """Adds the `RouteEntry`  to the table, and associates it with the given `router_id`."""
        self.table[router_id] = route

    def remove_route(self, router_id: int) -> None:
        """Removes the `router_id` and RouteEntry` from the table."""
        del self.table[router_id]

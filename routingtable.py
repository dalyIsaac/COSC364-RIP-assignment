from typing import Dict
from routeentry import RouteEntry
from datetime import datetime, timedelta
from random import randint


class RoutingTable:
    """
    Contains all of the entries for the routing table, for this router.

    Instance variables:
    table -- Contains the routing table, in the form of `{[key: router_id]: RouteEntry}`.
    router_id -- The router of this router.
    sched_update_time -- The time at which a normally scheduled Response will be sent to other routers.
    update_delta -- The delta to increment the `sched_update_time` by.
    timeout_delta -- The delta for the time after which a route is no longer valid.
    gc_delta -- The delta for the time after which invalid routes are removed from the table.
    """

    table: Dict[int, RouteEntry]

    sched_update_time: datetime

    update_delta: int
    timeout_delta: int
    gc_delta: int

    def __init__(
        self, router_id: int, update_delta: int, timeout_delta: int, gc_delta: int
    ):
        self.table = {}
        self.router_id = router_id
        self.update_delta = update_delta
        self.update_sched_update_time()
        self.timeout_delta = timeout_delta
        self.gc_delta = gc_delta

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

    def update_sched_update_time(self, initial_time=datetime.now()) -> datetime:
        """
        Updates the scheduled time at which an update will be sent out for this `RouteEntry`.
        Returns the `initial_time`, which is the what `SCHEDULED_UPDATE_TIME` is added to.
        
        Keyword arguments:
        initial_time -- The initial time, as specified. Defaults to `datetime.now()`
        """
        self.sched_update_time = initial_time + timedelta(
            self.update_delta + randint(-5, 5)
        )
        return initial_time

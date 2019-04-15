from typing import Dict
from routeentry import RouteEntry
from datetime import datetime, timedelta
from router import SCHEDULED_UPDATE_TIME
from random import randint


class RoutingTable:
    """
    Contains all of the entries for the routing table, for this router.

    Instance variables:
    table -- Contains the routing table, in the form of `{[key: router_id]: RouteEntry}`.
    router_id -- The router of this router.
    sched_update_time -- The time at which a normally scheduled Response will be sent to other routers.
    """

    table: Dict[int, RouteEntry]
    sched_update_time: datetime

    def __init__(
        self,
        router_id: int,
        sched_update_time: datetime = datetime.now() + timedelta(SCHEDULED_UPDATE_TIME),
    ):
        self.table = {}
        self.router_id = router_id
        self.sched_update_time = sched_update_time

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
            SCHEDULED_UPDATE_TIME + randint(-5, 5)
        )
        return initial_time

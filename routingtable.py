from datetime import datetime, timedelta
from random import randint
from time import sleep
from typing import Dict, Iterator, Optional

from routeentry import RouteEntry


class RoutingTable:
    """
    Contains all of the entries for the routing table, for this router.

    Instance variables:

    table -- Contains the routing table, in the form of
    `{[key: router_id]: RouteEntry}`.

    router_id -- The router of this router.

    sched_update_time -- The time at which a normally scheduled Response will
    be sent to other routers.

    update_delta -- The delta to increment the `sched_update_time` by.

    timeout_delta -- The delta for the time after which a route is no longer
    valid.

    gc_delta -- The delta for the time after which invalid routes are removed
    from the table.
    """

    table: Dict[int, RouteEntry]

    sched_update_time: datetime
    triggered_update_time: Optional[datetime] = None

    update_delta: int
    timeout_delta: int
    gc_delta: int

    def __init__(
        self,
        router_id: int,
        update_delta: int,
        timeout_delta: int,
        gc_delta: int,
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

    def __iter__(self) -> Iterator[int]:
        """Iterates over the `RouteEntry` items in the routing table"""
        return iter(self.table.keys())

    def __getitem__(self, index: int) -> RouteEntry:
        """
        Returns a specific `RouteEntry` in the routing table, given its
        `router_id`.
        """
        return self.table[index]

    def __contains__(self, router_id: int) -> bool:
        """
        Checks to see if the given `router_id` is inside the routing table.
        """
        return router_id in self.table

    def __delitem__(self, router_id: int):
        """
        Removes the `router_id` and associated `RouteEntry` from the table.
        """
        self.remove_route(router_id)

    def _str_headers(self, router_id: int) -> str:
        output = (
            "| port | metric | next_address | learned_from | flag   | "
            + "timeout_time".ljust(26)
            + " | "
            + "gc_time".ljust(26)
            + " |\n"
        )
        delim = output.split("|")
        for d in delim[1:-1]:
            output += "|" + "=" * len(d)
        output += "|\n"
        return output

    def _str_entry(self, router_id: int) -> str:
        """
        Returns the string representation of a `RouteEntry` inside the table.
        """
        e = self.table[router_id]
        output = (
            "| "
            + str(e.port).ljust(4)
            + " | "
            + str(e.metric).ljust(6)
            + " | "
            + str(e.next_address).ljust(12)
            + " | "
            + str(e.learned_from).ljust(12)
            + " | "
            + str(e.flag).ljust(6)
            + " | "
        )

        try:
            output += str(e.timeout_time).ljust(26)
        except AttributeError:
            output += str(None).ljust(26)
        output += " | "

        try:
            output += str(e.gc_time).ljust(26)
        except AttributeError:
            output += str(None).ljust(26)
        output += " |\n"

        return output

    def __str__(self):
        """Returns a string representation of the routing table."""

        output = ""

        router_id = None
        for router_id in self.table:
            output += self._str_entry(router_id)

        if output:
            output = self._str_headers(router_id) + output
        else:
            output = "Empty table"

        return output

    def neighbours(self):
        """
        Returns the `router_id`s of the neighbouring routers.
        """
        return self.table.keys()

    def add_route(self, router_id: int, route: RouteEntry) -> None:
        """
        Adds the `RouteEntry`  to the table, and associates it with the given
        `router_id`."""
        self.table[router_id] = route

    def remove_route(self, router_id: int) -> None:
        """
        Removes the `router_id` and associated `RouteEntry` from the table.
        """
        del self.table[router_id]

    def update_sched_update_time(self, initial_time=datetime.now()) -> datetime:
        """
        Updates the scheduled time at which an update will be sent out for this
        `RouteEntry`. Returns the `initial_time`, which is the what
        `self.update_delta` is added to.

        Keyword arguments:

        initial_time -- The initial time, as specified. Defaults to
        `datetime.now()`
        """
        self.sched_update_time = initial_time + timedelta(
            seconds=self.update_delta + randint(-5, 5)
        )
        return initial_time

    def set_triggered_update_time(self, initial_time=datetime.now()) -> int:
        """
        Updates the triggered time at which an update will be sent out for
        this `RouteEntry`.

        Returns a Boolean indicating whether another triggered update has been
        requested. This detects if this method has been called after
        `self.triggered_update_time` has been set. If it has been set again,
        then it will return `False`. Otherwise, it will return `True`.

        Returns `False` if the `triggered_update_time` is after the next
        scheduled `sched_update_time`.

        Keyword arguments:

        initial_time -- The initial time, as specified. Defaults to
        `datetime.now()`.
        """
        diff = randint(1, 5)
        self.triggered_update_time = initial_time + timedelta(seconds=diff)
        if self.triggered_update_time >= self.sched_update_time:
            return False

        sleep(diff)
        return initial_time + diff == self.triggered_update_time

from datetime import datetime, timedelta
from typing import Optional, Union


class RouteEntry:
    """
    Entry for a route inside the RIP routing table.

    Instance variables:

    flag -- Set to `True` to indicate that the entry has changed.

    port -- The port that this `RouteEntry` is going to be sent to.

    metric -- The cost in total.

    learned_from -- The router-id of the router from whom this route was
    learned from. `-1` if the router wasn't learned from anyone (i.e. learned
    from the config file on startup).

    timeout_time -- The delta for the time at which the timeout occurs, and the
    deletion process for this `RouteEntry` starts. This is not stored.

    gc_time --- The time after which this `RouteEntry` should be deleted from
    `RoutingTable`.
    """

    flag = False
    port: int
    metric: int
    learned_from: int

    timeout_time: datetime
    gc_time: Optional[datetime] = None

    def __init__(
        self,
        port: int,
        metric: int,
        timeout_time: Union[int, datetime],
        learned_from=-1,
    ):
        self.port = port
        self.metric = metric
        if isinstance(timeout_time, int):
            self.timeout_time = datetime.now() + timedelta(seconds=timeout_time)
        else:
            self.timeout_time = timeout_time
        self.learned_from = learned_from

    def shallow_copy(self):
        copy = RouteEntry(
            self.port, self.metric, self.timeout_time, self.learned_from
        )
        copy.flag = self.flag
        copy.gc_time = self.gc_time
        return copy

    def update_timeout_time(
        self, timeout_time: int, initial_time_arg: Optional[datetime] = None
    ) -> datetime:
        """
        Updates the timeout time, at which point this `RouteEntry` enter the
        deletion process.

        Returns the `initial_time`, which is the what `timeout_time` is added
        to.

        Keyword arguments:

        timeout_time -- The delta for between the `initial_time` and the new
        `timeout_time`.

        initial_time -- The initial time, defaults to `datetime.now()`
        """
        initial_time = (
            initial_time_arg if initial_time_arg is not None else datetime.now()
        )
        self.timeout_time = initial_time + timedelta(seconds=timeout_time)
        self.gc_time = None
        return initial_time

    def set_garbage_collection_time(
        self, gc_delta: int, initial_time_arg: Optional[datetime] = None
    ) -> datetime:
        """
        Updates the garbage collection time, at which point this `RouteEntry`
        will be removed from the table.

        Returns the `initial_time`, which is the what `gc_delta` is added to.

        Keyword arguments:
        gc_time -- The delta for between the `initial_time` and the new
        `gc_time`.

        initial_time -- The initial time, as specified. Defaults to
        `datetime.now()`
        """
        initial_time = (
            initial_time_arg if initial_time_arg is not None else datetime.now()
        )
        self.gc_time = initial_time + timedelta(seconds=gc_delta)
        return initial_time

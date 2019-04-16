from typing import Optional
from datetime import datetime, timedelta


class RouteEntry:
    """
    Entry for a route inside the RIP routing table.

    Instance variables:
    
    flag -- Set to `True` to indicate that the entry has changed.

    port -- The output port for this `RouteEntry`.

    metric -- The cost in total.

    next_address - the router-id for the next-address along the path to the destination.

    learned_from -- The router-id of the router from whom this route was learned from. -1 if the router wasn't learned 
    from anyone (i.e. learned from the config file on startup).

    output_socket -- The output socket for this router to communicate with the router specified in this `RouteEntry`.
    
    timeout_time -- The delta for the time at which the timeout occurs, and the deletion process for this `RouteEntry` 
    starts. This is not stored.

    gc_time --- The time after which this `RouteEntry` should be deleted from `RoutingTable`.
    """

    flag = False
    port: int
    metric: int
    next_address: int
    learned_from: int
    output_socket: int

    timeout_time: datetime
    gc_time: Optional[datetime]

    def __init__(
        self,
        port: int,
        metric: int,
        next_address: int,
        timeout_time: int,
        learned_from=-1,
        output_socket=-1,
    ):
        self.port = port
        self.metric = metric
        self.next_address = next_address
        current_time = datetime.now()
        self.timeout_time = current_time + timedelta(seconds=timeout_time)
        self.learned_from = learned_from
        self.output_socket = output_socket

    def update_timeout_time(
        self, timeout_time: int, initial_time=datetime.now()
    ) -> datetime:
        """
        Updates the timeout time, at which point this `RouteEntry` enter the deletion process.

        Returns the `initial_time`, which is the what `timeout_time` is added to.
        
        Keyword arguments:
        
        timeout_time -- The delta for between the `initial_time` and the new `timeout_time`.

        initial_time -- The initial time, defaults to `datetime.now()`
        """
        self.timeout_time = initial_time + timedelta(seconds=timeout_time)
        return initial_time

    def set_garbage_collection_time(
        self, gc_delta: int, initial_time=datetime.now()
    ) -> datetime:
        """
        Updates the garbage collection time, at which point this `RouteEntry` will be removed from the table.

        Returns the `initial_time`, which is the what `gc_delta` is added to.
        
        Keyword arguments:
        gc_time -- The delta for between the `initial_time` and the new `gc_time`.

        initial_time -- The initial time, as specified. Defaults to `datetime.now()`
        """
        self.gc_time = initial_time + timedelta(seconds=gc_delta)
        return initial_time

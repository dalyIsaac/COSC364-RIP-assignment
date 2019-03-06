from typing import Optional
from datetime import datetime, timedelta
from random import randint
from router import SCHEDULED_UPDATE_TIME, TIMEOUT_TIME, GARBAGE_COLLECTION_TIME


class RouteEntry:
    """
    Entry for a route inside the RIP routing table.

    Instance variables:
    port -- The output port for this `RouteEntry`.
    next_address - the router-id for the next-address along the path to the destination.
    sched_update_time -- The time at which a normally scheduled Response will be sent to other routers.
    timeout_time -- The time at which the timeout occurs, and the deletion process for this `RouteEntry` starts.
    garbage_collection_time --- The time after which this `RouteEntry` should be deleted from `RoutingTable`.
    flag -- Set to `True` to indicate that the entry has changed.
    learned_from -- The router-id of the router from whom this route was learned from. -1 if the router wasn't learned 
    from anyone (i.e. learned from the config file on startup).
    """

    flag = False

    def __init__(self, port: int, metric: int, next_address: int, learned_from = -1):
        self.port = port
        self.metric = metric
        self.next_address = next_address
        current_time = datetime.now()
        self.sched_update_time = current_time + timedelta(SCHEDULED_UPDATE_TIME)
        self.timeout_time = current_time + timedelta(TIMEOUT_TIME)
        self.learned_from = learned_from

    def update_sched_update_time(self, initial_time=datetime.now()) -> datetime:
        """
        Updates the scheduled time at which an update will be sent out for this `RouteEntry`.
        Returns the `initial_time`, which is the what `SCHEDULED_UPDATE_TIME` is added to.
        
        Keyword arguments:
        initial_time -- The initial time, as specified. Defaults to `datetime.now()`
        """
        self.sched_update_time = initial_time + timedelta(SCHEDULED_UPDATE_TIME + randint(-5, 5))
        return initial_time

    def update_timeout_time(self, initial_time=datetime.now()) -> datetime:
        """
        Updates the timeout time, at which point this `RouteEntry` enter the deletion process.
        Returns the `initial_time`, which is the what `TIMEOUT_TIME` is added to.
        
        Keyword arguments:
        initial_time -- The initial time, defaults to `datetime.now()`
        """
        self.timeout_time = initial_time + timedelta(TIMEOUT_TIME)
        return initial_time

    def set_garbage_collection_time(self, initial_time=datetime.now()) -> datetime:
        """
        Updates the garbage collection time, at which point this `RouteEntry` will be removed from the table.
        Returns the `initial_time`, which is the what `GARBAGE_COLLECTION_TIME` is added to.
        
        Keyword arguments:
        initial_time -- The initial time, as specified. Defaults to `datetime.now()`
        """
        self.timeout_time = initial_time + timedelta(GARBAGE_COLLECTION_TIME)
        return initial_time

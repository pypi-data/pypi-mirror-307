from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union, cast
from uuid import UUID, uuid4

from eventsourcing.dispatch import singledispatchmethod
from eventsourcing.domain import Aggregate


class Location(Enum):
    """
    Locations in the world.
    """

    HAMBURG = "HAMBURG"
    HONGKONG = "HONGKONG"
    NEWYORK = "NEWYORK"
    STOCKHOLM = "STOCKHOLM"
    TOKYO = "TOKYO"

    NLRTM = "NLRTM"
    USDAL = "USDAL"
    AUMEL = "AUMEL"


class Leg:
    """
    Leg of an itinerary.
    """

    def __init__(
        self,
        origin: str,
        destination: str,
        voyage_number: str,
    ):
        self.origin: str = origin
        self.destination: str = destination
        self.voyage_number: str = voyage_number


class Itinerary:
    """
    An itinerary along which cargo is shipped.
    """

    def __init__(
        self,
        origin: str,
        destination: str,
        legs: Tuple[Leg, ...],
    ):
        self.origin = origin
        self.destination = destination
        self.legs = legs


class HandlingActivity(Enum):
    RECEIVE = "RECEIVE"
    LOAD = "LOAD"
    UNLOAD = "UNLOAD"
    CLAIM = "CLAIM"


# Custom static types.
LegDetails = Dict[str, str]

ItineraryDetails = Dict[str, Union[str, List[LegDetails]]]

NextExpectedActivity = Optional[Tuple[HandlingActivity, Location, str]]


# Some routes from one location to another.
REGISTERED_ROUTES = {
    ("HONGKONG", "STOCKHOLM"): [
        Itinerary(
            origin="HONGKONG",
            destination="STOCKHOLM",
            legs=(
                Leg(
                    origin="HONGKONG",
                    destination="NEWYORK",
                    voyage_number="V1",
                ),
                Leg(
                    origin="NEWYORK",
                    destination="STOCKHOLM",
                    voyage_number="V2",
                ),
            ),
        )
    ],
    ("TOKYO", "STOCKHOLM"): [
        Itinerary(
            origin="TOKYO",
            destination="STOCKHOLM",
            legs=(
                Leg(
                    origin="TOKYO",
                    destination="HAMBURG",
                    voyage_number="V3",
                ),
                Leg(
                    origin="HAMBURG",
                    destination="STOCKHOLM",
                    voyage_number="V4",
                ),
            ),
        )
    ],
}


class Cargo(Aggregate):
    """
    The Cargo aggregate is an event-sourced domain model aggregate that
    specifies the routing from origin to destination, and can track what
    happens to the cargo after it has been booked.
    """

    def __init__(
        self,
        origin: Location,
        destination: Location,
        arrival_deadline: datetime,
    ):
        self._origin: Location = origin
        self._destination: Location = destination
        self._arrival_deadline: datetime = arrival_deadline
        self._transport_status: str = "NOT_RECEIVED"
        self._routing_status: str = "NOT_ROUTED"
        self._is_misdirected: bool = False
        self._estimated_time_of_arrival: datetime | None = None
        self._next_expected_activity: NextExpectedActivity = None
        self._route: Itinerary | None = None
        self._last_known_location: Location | None = None
        self._current_voyage_number: str | None = None

    @property
    def origin(self) -> Location:
        return self._origin

    @property
    def destination(self) -> Location:
        return self._destination

    @property
    def arrival_deadline(self) -> datetime:
        return self._arrival_deadline

    @property
    def transport_status(self) -> str:
        return self._transport_status

    @property
    def routing_status(self) -> str:
        return self._routing_status

    @property
    def is_misdirected(self) -> bool:
        return self._is_misdirected

    @property
    def estimated_time_of_arrival(
        self,
    ) -> datetime | None:
        return self._estimated_time_of_arrival

    @property
    def next_expected_activity(self) -> NextExpectedActivity:
        return self._next_expected_activity

    @property
    def route(self) -> Itinerary | None:
        return self._route

    @property
    def last_known_location(self) -> Location | None:
        return self._last_known_location

    @property
    def current_voyage_number(self) -> str | None:
        return self._current_voyage_number

    @classmethod
    def new_booking(
        cls,
        origin: Location,
        destination: Location,
        arrival_deadline: datetime,
    ) -> Cargo:
        return cls._create(
            event_class=cls.BookingStarted,
            id=uuid4(),
            origin=origin,
            destination=destination,
            arrival_deadline=arrival_deadline,
        )

    class BookingStarted(Aggregate.Created):
        origin: Location
        destination: Location
        arrival_deadline: datetime

    class Event(Aggregate.Event):
        def apply(self, aggregate: Aggregate) -> None:
            cast(Cargo, aggregate).when(self)

    @singledispatchmethod
    def when(self, event: Event) -> None:
        """
        Default method to apply an aggregate event to the aggregate object.
        """

    def change_destination(self, destination: Location) -> None:
        self.trigger_event(
            self.DestinationChanged,
            destination=destination,
        )

    class DestinationChanged(Event):
        destination: Location

    @when.register
    def _(self, event: Cargo.DestinationChanged) -> None:
        self._destination = event.destination

    def assign_route(self, itinerary: Itinerary) -> None:
        self.trigger_event(self.RouteAssigned, route=itinerary)

    class RouteAssigned(Event):
        route: Itinerary

    @when.register
    def _(self, event: Cargo.RouteAssigned) -> None:
        self._route = event.route
        self._routing_status = "ROUTED"
        self._estimated_time_of_arrival = Cargo.Event.create_timestamp() + timedelta(
            weeks=1
        )
        self._next_expected_activity = (HandlingActivity.RECEIVE, self.origin, "")
        self._is_misdirected = False

    def register_handling_event(
        self,
        tracking_id: UUID,
        voyage_number: str | None,
        location: Location,
        handling_activity: HandlingActivity,
    ) -> None:
        self.trigger_event(
            self.HandlingEventRegistered,
            tracking_id=tracking_id,
            voyage_number=voyage_number,
            location=location,
            handling_activity=handling_activity,
        )

    class HandlingEventRegistered(Event):
        tracking_id: UUID
        voyage_number: str
        location: Location
        handling_activity: str

    @when.register
    def _(self, event: Cargo.HandlingEventRegistered) -> None:
        assert self.route is not None
        if event.handling_activity == HandlingActivity.RECEIVE:
            self._transport_status = "IN_PORT"
            self._last_known_location = event.location
            self._next_expected_activity = (
                HandlingActivity.LOAD,
                event.location,
                self.route.legs[0].voyage_number,
            )
        elif event.handling_activity == HandlingActivity.LOAD:
            self._transport_status = "ONBOARD_CARRIER"
            self._current_voyage_number = event.voyage_number
            for leg in self.route.legs:
                if (
                    leg.origin == event.location.value
                    and leg.voyage_number == event.voyage_number
                ):
                    self._next_expected_activity = (
                        HandlingActivity.UNLOAD,
                        Location[leg.destination],
                        event.voyage_number,
                    )
                    break
            else:
                msg = "Can't find leg with origin={} and voyage_number={}".format(
                    event.location,
                    event.voyage_number,
                )
                raise Exception(msg)

        elif event.handling_activity == HandlingActivity.UNLOAD:
            self._current_voyage_number = None
            self._last_known_location = event.location
            self._transport_status = "IN_PORT"
            if event.location == self.destination:
                self._next_expected_activity = (
                    HandlingActivity.CLAIM,
                    event.location,
                    "",
                )
            elif event.location.value in [leg.destination for leg in self.route.legs]:
                for i, leg in enumerate(self.route.legs):
                    if leg.voyage_number == event.voyage_number:
                        next_leg: Leg = self.route.legs[i + 1]
                        assert Location[next_leg.origin] == event.location
                        self._next_expected_activity = (
                            HandlingActivity.LOAD,
                            event.location,
                            next_leg.voyage_number,
                        )
                        break
            else:
                self._is_misdirected = True
                self._next_expected_activity = None

        elif event.handling_activity == HandlingActivity.CLAIM:
            self._next_expected_activity = None
            self._transport_status = "CLAIMED"

        else:
            msg = f"Unsupported handling event: {event.handling_activity}"
            raise Exception(msg)

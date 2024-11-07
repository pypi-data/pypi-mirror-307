from __future__ import annotations

from datetime import datetime, timezone
from functools import singledispatch
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict

from eventsourcing.utils import get_topic


class DomainEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    originator_id: UUID
    originator_version: int
    timestamp: datetime


def create_timestamp() -> datetime:
    return datetime.now(tz=timezone.utc)


class Aggregate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID
    version: int
    created_on: datetime
    modified_on: datetime


class Snapshot(DomainEvent):
    topic: str
    state: Dict[str, Any]

    @classmethod
    def take(cls, aggregate: Aggregate) -> Snapshot:
        return Snapshot(
            originator_id=aggregate.id,
            originator_version=aggregate.version,
            timestamp=create_timestamp(),
            topic=get_topic(type(aggregate)),
            state=aggregate.model_dump(),
        )


TAggregate = TypeVar("TAggregate", bound=Aggregate)
MutatorFunction = Callable[..., Optional[TAggregate]]


def aggregate_projector(
    mutator: MutatorFunction[TAggregate],
) -> Callable[[TAggregate | None, Iterable[DomainEvent]], TAggregate | None]:
    def project_aggregate(
        aggregate: TAggregate | None, events: Iterable[DomainEvent]
    ) -> TAggregate | None:
        for event in events:
            aggregate = mutator(event, aggregate)
        return aggregate

    return project_aggregate


class Trick(BaseModel):
    name: str


class Dog(Aggregate):
    name: str
    tricks: Tuple[Trick, ...]


class DogRegistered(DomainEvent):
    name: str


class TrickAdded(DomainEvent):
    trick: Trick


def register_dog(name: str) -> DomainEvent:
    return DogRegistered(
        originator_id=uuid4(),
        originator_version=1,
        timestamp=create_timestamp(),
        name=name,
    )


def add_trick(dog: Dog, trick: Trick) -> DomainEvent:
    return TrickAdded(
        originator_id=dog.id,
        originator_version=dog.version + 1,
        timestamp=create_timestamp(),
        trick=trick,
    )


@singledispatch
def mutate_dog(_: DomainEvent, __: Dog | None) -> Dog | None:
    """Mutates aggregate with event."""


@mutate_dog.register
def _(event: DogRegistered, _: None) -> Dog:
    return Dog(
        id=event.originator_id,
        version=event.originator_version,
        created_on=event.timestamp,
        modified_on=event.timestamp,
        name=event.name,
        tricks=(),
    )


@mutate_dog.register
def _(event: TrickAdded, dog: Dog) -> Dog:
    return Dog(
        id=dog.id,
        version=event.originator_version,
        created_on=dog.created_on,
        modified_on=event.timestamp,
        name=dog.name,
        tricks=(*dog.tricks, event.trick),
    )


@mutate_dog.register
def _(event: Snapshot, _: None) -> Dog:
    return Dog(
        id=event.state["id"],
        version=event.state["version"],
        created_on=event.state["created_on"],
        modified_on=event.state["modified_on"],
        name=event.state["name"],
        tricks=event.state["tricks"],
    )


project_dog = aggregate_projector(mutate_dog)

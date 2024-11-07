from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from eventsourcing.application import Application
from eventsourcing.examples.aggregate7.domainmodel import (
    Snapshot,
    Trick,
    add_trick,
    project_dog,
    register_dog,
)
from eventsourcing.examples.aggregate7.persistence import (
    OrjsonTranscoder,
    PydanticMapper,
)

if TYPE_CHECKING:  # pragma: nocover
    from uuid import UUID

    from eventsourcing.persistence import Mapper, Transcoder


class DogSchool(Application):
    is_snapshotting_enabled = True
    snapshot_class = Snapshot

    def register_dog(self, name: str) -> UUID:
        event = register_dog(name)
        self.save(event)
        return event.originator_id

    def add_trick(self, dog_id: UUID, trick: str) -> None:
        dog = self.repository.get(dog_id, projector_func=project_dog)
        self.save(add_trick(dog, Trick(name=trick)))

    def get_dog(self, dog_id: UUID) -> Dict[str, Any]:
        dog = self.repository.get(dog_id, projector_func=project_dog)
        return {
            "name": dog.name,
            "tricks": tuple([t.name for t in dog.tricks]),
            "created_on": dog.created_on,
            "modified_on": dog.modified_on,
        }

    def construct_mapper(self) -> Mapper:
        return self.factory.mapper(
            transcoder=self.construct_transcoder(),
            mapper_class=PydanticMapper,
        )

    def construct_transcoder(self) -> Transcoder:
        return OrjsonTranscoder()

from __future__ import annotations

import os
from typing import ClassVar, Dict, cast
from unittest import TestCase
from uuid import uuid4

from eventsourcing.examples.contentmanagement.application import PageNotFoundError
from eventsourcing.examples.searchablecontent.application import (
    SearchableContentApplication,
)
from eventsourcing.examples.searchablecontent.persistence import (
    SearchableContentRecorder,
)
from eventsourcing.postgres import PostgresDatastore
from eventsourcing.tests.postgres_utils import drop_postgres_table


class SearchableContentRecorderTestCase(TestCase):
    env: ClassVar[Dict[str, str]] = {}

    def test_recorder(self) -> None:
        app = SearchableContentApplication(env=self.env)

        # Need to cover the case where select_page() raises PageNotFound.
        recorder = cast(SearchableContentRecorder, app.recorder)
        with self.assertRaises(PageNotFoundError):
            recorder.select_page(uuid4())


class TestWithSQLite(SearchableContentRecorderTestCase):
    env: ClassVar[Dict[str, str]] = {
        "PERSISTENCE_MODULE": "eventsourcing.examples.searchablecontent.sqlite",
        "SQLITE_DBNAME": ":memory:",
    }


class TestWithPostgres(SearchableContentRecorderTestCase):
    env: ClassVar[Dict[str, str]] = {
        "PERSISTENCE_MODULE": "eventsourcing.examples.searchablecontent.postgres"
    }

    def setUp(self) -> None:
        super().setUp()
        os.environ["POSTGRES_DBNAME"] = "eventsourcing"
        os.environ["POSTGRES_HOST"] = "127.0.0.1"
        os.environ["POSTGRES_PORT"] = "5432"
        os.environ["POSTGRES_USER"] = "eventsourcing"
        os.environ["POSTGRES_PASSWORD"] = "eventsourcing"  # noqa: S105
        self.drop_tables()

    def tearDown(self) -> None:
        self.drop_tables()
        super().tearDown()

    def drop_tables(self) -> None:
        with PostgresDatastore(
            os.environ["POSTGRES_DBNAME"],
            os.environ["POSTGRES_HOST"],
            os.environ["POSTGRES_PORT"],
            os.environ["POSTGRES_USER"],
            os.environ["POSTGRES_PASSWORD"],
        ) as datastore:
            drop_postgres_table(datastore, "public.searchablecontentapplication_events")
            drop_postgres_table(datastore, "public.pages_projection_example")


del SearchableContentRecorderTestCase

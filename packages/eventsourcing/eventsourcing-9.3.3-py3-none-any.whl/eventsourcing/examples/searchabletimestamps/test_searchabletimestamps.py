from __future__ import annotations

import os
from datetime import timedelta
from time import sleep
from typing import ClassVar, Dict
from unittest import TestCase

from eventsourcing.application import AggregateNotFoundError
from eventsourcing.domain import create_utc_datetime_now
from eventsourcing.examples.cargoshipping.domainmodel import Location
from eventsourcing.examples.searchabletimestamps.application import (
    SearchableTimestampsApplication,
)
from eventsourcing.postgres import PostgresDatastore
from eventsourcing.tests.postgres_utils import drop_postgres_table


class SearchableTimestampsTestCase(TestCase):
    env: ClassVar[Dict[str, str]]

    def test(self) -> None:
        # Construct application.
        app = SearchableTimestampsApplication(env=self.env)
        timestamp0 = create_utc_datetime_now()
        sleep(1e-5)

        # Book new cargo.
        tracking_id = app.book_new_cargo(
            origin=Location["NLRTM"],
            destination=Location["USDAL"],
            arrival_deadline=create_utc_datetime_now() + timedelta(weeks=3),
        )
        timestamp1 = create_utc_datetime_now()
        sleep(1e-5)

        # Change destination.
        app.change_destination(tracking_id, destination=Location["AUMEL"])
        timestamp2 = create_utc_datetime_now()
        sleep(1e-5)

        # View the state of the cargo tracking at particular times.
        with self.assertRaises(AggregateNotFoundError):
            app.get_cargo_at_timestamp(tracking_id, timestamp0)

        cargo_at_timestamp1 = app.get_cargo_at_timestamp(tracking_id, timestamp1)
        self.assertEqual(cargo_at_timestamp1.destination, Location["USDAL"])

        cargo_at_timestamp2 = app.get_cargo_at_timestamp(tracking_id, timestamp2)
        self.assertEqual(cargo_at_timestamp2.destination, Location["AUMEL"])


class WithSQLite(SearchableTimestampsTestCase):
    env: ClassVar[Dict[str, str]] = {
        "PERSISTENCE_MODULE": "eventsourcing.examples.searchabletimestamps.sqlite",
        "SQLITE_DBNAME": ":memory:",
    }


class WithPostgreSQL(SearchableTimestampsTestCase):
    env: ClassVar[Dict[str, str]] = {
        "PERSISTENCE_MODULE": "eventsourcing.examples.searchabletimestamps.postgres"
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
            drop_postgres_table(
                datastore, "public.searchabletimestampsapplication_events"
            )
            drop_postgres_table(
                datastore, "public.searchabletimestampsapplication_timestamps"
            )


del SearchableTimestampsTestCase

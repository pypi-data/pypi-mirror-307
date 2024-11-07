from __future__ import annotations

import os
from typing import ClassVar, Dict
from unittest import TestCase
from uuid import uuid4

from eventsourcing.examples.contentmanagement.domainmodel import user_id_cvar
from eventsourcing.examples.searchablecontent.application import (
    SearchableContentApplication,
)
from eventsourcing.postgres import PostgresDatastore
from eventsourcing.tests.postgres_utils import drop_postgres_table


class SearchableContentApplicationTestCase(TestCase):
    env: ClassVar[Dict[str, str]] = {}

    def test_app(self) -> None:
        app = SearchableContentApplication(env=self.env)

        # Set user_id context variable.
        user_id = uuid4()
        user_id_cvar.set(user_id)

        # Create empty pages.
        app.create_page(title="Animals", slug="animals")
        app.create_page(title="Plants", slug="plants")
        app.create_page(title="Minerals", slug="minerals")

        # Search, expect no results.
        self.assertEqual(0, len(app.search("dog")))
        self.assertEqual(0, len(app.search("rose")))
        self.assertEqual(0, len(app.search("zinc")))

        # Update the pages.
        app.update_body(slug="animals", body="cat dog zebra")
        app.update_body(slug="plants", body="bluebell rose jasmine")
        app.update_body(slug="minerals", body="iron zinc calcium")

        # Search for single words, expect results.
        pages = app.search("dog")
        self.assertEqual(1, len(pages))
        self.assertEqual(pages[0]["slug"], "animals")
        self.assertEqual(pages[0]["body"], "cat dog zebra")

        pages = app.search("rose")
        self.assertEqual(1, len(pages))
        self.assertEqual(pages[0]["slug"], "plants")
        self.assertEqual(pages[0]["body"], "bluebell rose jasmine")

        pages = app.search("zinc")
        self.assertEqual(1, len(pages))
        self.assertEqual(pages[0]["slug"], "minerals")
        self.assertEqual(pages[0]["body"], "iron zinc calcium")

        # Search for multiple words in same page.
        pages = app.search("dog cat")
        self.assertEqual(1, len(pages))
        self.assertEqual(pages[0]["slug"], "animals")
        self.assertEqual(pages[0]["body"], "cat dog zebra")

        # Search for multiple words in same page, expect no results.
        pages = app.search("rose zebra")
        self.assertEqual(0, len(pages))

        # Search for alternative words, expect two results.
        pages = app.search("rose OR zebra")
        self.assertEqual(2, len(pages))
        self.assertEqual(["animals", "plants"], sorted(p["slug"] for p in pages))


class TestWithSQLite(SearchableContentApplicationTestCase):
    env: ClassVar[Dict[str, str]] = {
        "PERSISTENCE_MODULE": "eventsourcing.examples.searchablecontent.sqlite",
        "SQLITE_DBNAME": ":memory:",
    }


class TestWithPostgres(SearchableContentApplicationTestCase):
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


del SearchableContentApplicationTestCase

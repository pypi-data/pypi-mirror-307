import asyncio
import hashlib
import logging
import re
import time
from abc import ABC, abstractmethod
from datetime import datetime
from tempfile import NamedTemporaryFile
from typing import Any, Optional
from urllib.request import urlopen

from asgiref.sync import sync_to_async
from celery import shared_task
from django.conf import settings
from django.core.files import File
from wagtail.images import get_image_model

from .facebook_api import FacebookEventsAPI
from .processors import AsyncEventsProcessor, EventsProcessor

logger = logging.getLogger(__name__)


class BaseFacebookEventsImporter(ABC):
    events_api = FacebookEventsAPI()
    processor = EventsProcessor()
    full_sync = False

    @abstractmethod
    def import_events(self):
        pass


class FacebookEventsImporterSync(BaseFacebookEventsImporter):
    def __init__(self, full_sync=False):
        self.full_sync = full_sync
        logger.info(
            f"Initialized FacebookEventsImporterBase with full_sync={self.full_sync}"
        )

    def import_events(self):
        logger.info("Starting synchronous event import")
        start_time = time.time()
        events_page = self.events_api.get()
        create_events, update_events = [], []

        if self.full_sync:
            logger.info("Full sync enabled; fetching all pages")
            while events_page:
                new_create_events, new_update_events = self.processor.process_page(
                    events_page
                )
                create_events.extend(new_create_events)
                update_events.extend(new_update_events)
                next_url = events_page.get("paging", {}).get("next")
                if next_url:
                    logger.info(f"Fetching next page from URL: {next_url}")
                    events_page = self.events_api.fetch_next_page(next_url)
                else:
                    break
            logger.info(
                f"Creating {len(create_events)} events and updating {len(update_events)} events"
            )
        else:
            new_create_events, new_update_events = self.processor.process_page(
                events_page
            )
            create_events.extend(new_create_events)
            update_events.extend(new_update_events)
            logger.info(
                f"Creating {len(create_events)} events and updating {len(update_events)} events"
            )
        self.processor.bulk_create(create_events)
        self.processor.bulk_update(update_events)
        logger.info(
            f"Synchronous import finished in {time.time() - start_time:.2f} seconds"
        )
        return [event["id"] for event in create_events] + [
            event[1].facebook_id for event in update_events
        ]


class FacebookEventsImporterAsync(BaseFacebookEventsImporter):
    def __init__(self, full_sync=False):
        self.full_sync = full_sync
        self.processor = AsyncEventsProcessor()
        logger.info(
            f"Initialized FacebookEventsImporterBase with full_sync={self.full_sync}"
        )

    async def import_events(self):
        logger.info("Starting asynchronous event import")
        start_time = time.time()
        events_page = await self.events_api.async_get()
        create_events, update_events = [], []
        if self.full_sync:
            logger.info("Full sync enabled; fetching all pages")
            while events_page:
                next_url = events_page.get("paging", {}).get("next")
                next_page_task = (
                    asyncio.create_task(self.events_api.async_fetch_next_page(next_url))
                    if next_url
                    else None
                )

                (
                    new_create_events,
                    new_update_events,
                ) = await self.processor.process_page(events_page)
                create_events.extend(new_create_events)
                update_events.extend(new_update_events)

                events_page = await next_page_task if next_page_task else None
            logger.info(
                f"Creating {len(create_events)} events and updating {len(update_events)} events"
            )
        else:
            new_create_events, new_update_events = await self.processor.process_page(
                events_page
            )
            create_events.extend(new_create_events)
            update_events.extend(new_update_events)
            logger.info(
                f"Creating {len(create_events)} events and updating {len(update_events)} events"
            )
        await sync_to_async(self.processor.bulk_create)(create_events)
        await sync_to_async(self.processor.bulk_update)(update_events)
        logger.info(
            f"Asynchronous import finished in {time.time() - start_time:.2f} seconds"
        )
        return [event["id"] for event in create_events] + [
            event[1].facebook_id for event in update_events
        ]


@shared_task
def process_page_task(events_page):
    # WIP
    """
    Celery task to process a single page of events.
    """
    processor = AsyncEventsProcessor()  # Use the async processor
    new_create_events, new_update_events = asyncio.run(
        processor.process_page(events_page)
    )

    # Bulk create and update within the task
    processor.bulk_create(new_create_events)
    processor.bulk_update(new_update_events)

    return {
        "created": [event["id"] for event in new_create_events],
        "updated": [event[1].facebook_id for event in new_update_events],
    }


class CeleryFacebookEventsImporterAsync(FacebookEventsImporterAsync):
    # WIP

    async def import_events(self):
        logger.info("Starting asynchronous event import with Celery")
        start_time = time.time()
        events_page = await self.events_api.async_get()

        # List to store async task results for each page
        tasks = []

        if self.full_sync:
            logger.info("Full sync enabled; fetching all pages")
            while events_page:
                # Add a task to Celery for processing the current page
                task = process_page_task.delay(events_page)
                tasks.append(task)

                # Fetch the next page asynchronously
                next_url = events_page.get("paging", {}).get("next")
                events_page = (
                    await self.events_api.async_fetch_next_page(next_url)
                    if next_url
                    else None
                )
        else:
            # Process a single page if full sync is not enabled
            task = process_page_task.delay(events_page)
            tasks.append(task)

        # Collect all results once tasks are done
        create_events_ids, update_events_ids = [], []
        for task in tasks:
            result = task.get()  # Retrieve task result
            create_events_ids.extend(result.get("created", []))
            update_events_ids.extend(result.get("updated", []))

        logger.info(
            f"Finished asynchronous import with Celery in {time.time() - start_time:.2f} seconds"
        )

        return create_events_ids + update_events_ids

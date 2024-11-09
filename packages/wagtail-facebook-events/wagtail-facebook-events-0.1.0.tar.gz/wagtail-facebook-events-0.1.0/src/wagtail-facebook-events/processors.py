import asyncio
import hashlib
import logging
import time
from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile
from typing import Optional
from urllib.request import urlopen

import httpx
from asgiref.sync import sync_to_async
from django.core.files import File
from wagtail.images import get_image_model

from kabelbreukevents.apps.facebook.utils import get_event_model, get_event_serializer

logger = logging.getLogger(__name__)


class BaseEventsProcessor(ABC):
    def __init__(self):
        self.EventModel = get_event_model()
        self.EventSerializer = get_event_serializer()
        self.image_model = get_image_model()
        self.image_processor = EventImageProcessor()

    @abstractmethod
    def process_page(self, page):
        pass

    def bulk_create(self, create_events):
        logger.info("Starting bulk create for events")
        start_time = time.time()
        create_serializer = self.EventSerializer(data=create_events, many=True)
        if create_serializer.is_valid():
            instances = [
                self.EventModel(**data) for data in create_serializer.validated_data
            ]
            self.EventModel.objects.bulk_create(instances)
            logger.info(
                f"Bulk created {len(instances)} events in {time.time() - start_time:.2f} seconds"
            )
        else:
            logger.info(f"Bulk create failed: {create_serializer.errors}")

    def bulk_update(self, update_events):
        logger.info("Starting bulk update for events")
        start_time = time.time()
        update_instances = []

        for data, instance in update_events:
            serializer = self.EventSerializer(instance, data=data, partial=False)
            if serializer.is_valid():
                for field, value in serializer.validated_data.items():
                    setattr(instance, field, value)
                update_instances.append(instance)
            else:
                logger.info(
                    f"Could not update event {instance.id}: {serializer.errors}"
                )

        if update_instances:
            self.EventModel.objects.bulk_update(
                update_instances,
                fields=[
                    field.name
                    for field in self.EventModel._meta.fields
                    if not field.primary_key
                ],
            )
            logger.info(
                f"Bulk updated {len(update_instances)} events in {time.time() - start_time:.2f} seconds"
            )

    def _create_or_update(self, json_event):
        event_id = json_event.get("id")
        event_hash = self._hash(json_event)
        logger.info(f"Processing event {event_id}")

        if self.EventModel.objects.filter(facebook_id=event_id).exists():
            event_in_db = self.EventModel.objects.get(facebook_id=event_id)
            if event_hash != event_in_db.hashed and not event_in_db.stop_import:
                json_event["hashed"] = event_hash
                logger.info(f"Event {event_id} requires an update")
                return None, (json_event, event_in_db)
        else:
            json_event["hashed"] = event_hash
            logger.info(f"Event {event_id} will be created")
            return json_event, None

        logger.info(f"Event {event_id} did not change; skipping")
        return None, None

    @staticmethod
    def _hash(event) -> str:
        included_fields = [
            "id",
            "name",
            "description",
            "start_time",
            "end_time",
            "place",
        ]
        hash_string = "".join(
            f"{key}:{value}" for key, value in event.items() if key in included_fields
        )
        return hashlib.sha256(hash_string.encode()).hexdigest()


class EventsProcessor(BaseEventsProcessor):
    def process_page(self, page):
        logger.info("Processing a page of events")
        start_time = time.time()
        events = page.get("data", [])
        create_events, update_events = [], []

        for event in events:
            create_event, update_event = self._create_or_update(event)
            if create_event:
                if create_event.get("cover", {}).get("source"):
                    create_event["image"] = self.image_processor.download(create_event)
                create_events.append(create_event)
            if update_event:
                new_data, instance = update_event
                if new_data.get("cover", {}).get("source"):
                    new_data["image"] = self.image_processor.download(new_data)
                update_events.append((new_data, instance))

        logger.info(f"Processed page in {time.time() - start_time:.2f} seconds")
        return create_events, update_events


class AsyncEventsProcessor(BaseEventsProcessor):
    def __init__(self):
        super().__init__()
        self.image_processor = AsyncEventImageProcessor()

    async def process_page(self, page):
        """Process each event page, downloading and saving images concurrently."""
        logger.info("Processing a page of events asynchronously")
        start_time = time.time()
        events = page.get("data", [])
        create_events, update_events = [], []
        image_tasks = []

        for event in events:
            create_event, update_event = await sync_to_async(self._create_or_update)(
                event
            )
            if create_event:
                create_events.append(create_event)
                if create_event.get("cover", {}).get("source"):
                    image_tasks.append(self.image_processor.download(create_event))
            if update_event:
                update_events.append(update_event)
                if update_event[0].get("cover", {}).get("source"):
                    image_tasks.append(self.image_processor.download(update_event[0]))

        # Await all download and save tasks to complete
        saved_images = await asyncio.gather(*image_tasks)
        logger.info(
            f"Finished processing page in {time.time() - start_time:.2f} seconds"
        )
        return create_events, update_events


class BaseImageProcessor(ABC):
    image_model = get_image_model()

    @abstractmethod
    def download(self, url):
        pass


class EventImageProcessor(BaseImageProcessor):
    def download(self, event) -> Optional[int]:
        logger.info(f"Downloading image for event {event.get('id')}")
        start_time = time.time()
        response = urlopen(event["cover"]["source"])
        image_temp = NamedTemporaryFile(delete=True)
        image_temp.write(response.read())
        image_temp.flush()
        image_model = get_image_model()
        name = event["name"]
        image, created = image_model.objects.get_or_create(
            title=name,
            file=File(image_temp, name=f"{name}.jpg"),
        )
        logger.info(
            f"Downloaded and saved image for event {event.get('id')} in {time.time() - start_time:.2f} seconds"
        )
        return image.pk


class AsyncEventImageProcessor(BaseImageProcessor):
    async def download(self, event):
        """Downloads the image and immediately saves it to the database."""
        logger.info(f"Downloading image for event {event.get('id')}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(event["cover"]["source"])
                response.raise_for_status()

                image_temp = NamedTemporaryFile(delete=True)
                image_temp.write(response.content)
                image_temp.flush()

                # As soon as download completes, save the image to the database
                return await self._save_image(image_temp, event)
        except httpx.HTTPError as e:
            logger.error(f"Failed to download image for event {event.get('id')}: {e}")
            return None, event.get("id")

    async def _save_image(self, image_temp, event):
        """Save the downloaded image to the database."""
        name = event["name"]
        image_model = self.image_model

        image, created = await image_model.objects.aget_or_create(
            title=name,
            file=File(image_temp, name=f"{name}.jpg"),
        )
        image_temp.close()
        event["image"] = image.pk
        return image.pk

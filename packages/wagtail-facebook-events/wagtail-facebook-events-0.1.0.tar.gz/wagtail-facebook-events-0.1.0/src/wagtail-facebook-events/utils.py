from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string


def get_event_model():
    return apps.get_model(settings.FACEBOOK_EVENT_MODEL)


def get_event_serializer():
    return import_string(settings.FACEBOOK_EVENT_SERIALIZER)

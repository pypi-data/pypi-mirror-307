from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View

from kabelbreukevents.apps.cms.forms import ContactForm
from kabelbreukevents.apps.cms.tasks import import_facebook_events



class EventsImporterTriggerAPIView(LoginRequiredMixin, View):
    def get(self, request):
        import_facebook_events.delay()
        return JsonResponse(
            {"status": "Imported events from facebook to your website."}
        )
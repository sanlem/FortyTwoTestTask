from django.shortcuts import render
from apps.requests.models import RequestEntry
from apps.requests.serializers import RequestEntrySerializer
from rest_framework import generics


def requests_list(request):
    objects = RequestEntry.objects.all()[:10]
    return render(request, "requests.html", {"objects": objects})


class RequestEntryListView(generics.ListAPIView):
    queryset = RequestEntry.objects.all()[:10]
    serializer_class = RequestEntrySerializer

from django.shortcuts import render
from apps.requests.models import RequestEntry
from apps.requests.serializers import RequestEntrySerializer
from rest_framework import generics


def requests_list(request):
    objects = RequestEntry.objects.all()[:10]
    return render(request, "requests.html", {"objects": objects})


class RequestEntryListView(generics.ListAPIView):
    serializer_class = RequestEntrySerializer

    def get_queryset(self):
        """ filter entries by id that is greater than passed """
        queryset = RequestEntry.objects.all()
        pk = self.request.query_params.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(pk__gt=pk)
        return queryset[:10]

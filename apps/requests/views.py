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
        queryset = RequestEntry.objects.all().order_by('-priority',
                                                       '-timestamp')
        pk = self.request.query_params.get('pk', None)
        ordr = self.request.query_params.get('order', None)
        if pk is not None:
            queryset = queryset.filter(pk__gt=pk)
        if ordr is not None:
            queryset = queryset.order_by('priority')
        return queryset[:10]

from django.shortcuts import render
from apps.requests.models import RequestEntry
from apps.requests.serializers import RequestEntrySerializer
from rest_framework import generics


def requests_list(request):
    objects = list(RequestEntry.objects.order_by('-timestamp')[:10])
    objects.sort(key=sort_by_priority, reverse=True)
    return render(request, "requests.html", {"objects": objects})


def sort_by_priority(obj):
    return obj.priority


class RequestEntryListView(generics.ListAPIView):
    serializer_class = RequestEntrySerializer

    def get_queryset(self):
        """ filter entries by id that is greater than passed """
        queryset = RequestEntry.objects.order_by('-timestamp')
        pk = self.request.query_params.get('pk', None)
        ordr = self.request.query_params.get('order', None)
        qs = list(queryset[:10])
        qs.sort(key=sort_by_priority)
        if pk is not None:
            queryset = queryset.filter(pk__gt=pk)
        if ordr is not None:
            qs.sort(key=sort_by_priority)
            return qs
        else:
            qs.sort(key=sort_by_priority, reverse=True)
            return qs

from django.shortcuts import render
from apps.requests.models import RequestEntry


def requests_list(request):
    objects = RequestEntry.objects.all()[:10]
    return render(request, "requests.html", {"objects": objects})

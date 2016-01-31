from django.shortcuts import render
from .models import Request


def requests_list(request):
    objects = Request.objects.all()[:10]
    return render(request, "requests.html", {"objects": objects})

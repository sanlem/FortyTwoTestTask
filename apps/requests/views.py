from django.shortcuts import render


def requests_list(request):
    objects = [{"url": "http://example.com", "timestamp": "16:00"},
               {"url": "http://example.com/blabla", "timestamp": "16:05"}]
    return render(request, "requests.html", {"objects": objects})

from rest_framework import serializers
from apps.requests.models import RequestEntry


class RequestEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestEntry

from django.core import serializers
from django.http import HttpResponse
from rooms import models

# Create your views here.

def list_rooms(request):
    data = serializers.serialize("json", models.Room.objects.all())
    reponse = HttpResponse(content=data)
    return reponse
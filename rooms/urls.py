""" viewset settings 
from rest_framework.routers import DefaultRouter
from django.urls import path
from . import viewsets

app_name = "rooms"

router = DefaultRouter()
router.register("", viewsets.RoomViewset, basename='room')

urlpatterns = router.urls """

from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("",views.RoomsView.as_view()),
    path("<int:pk>",views.RoomView.as_view()),
]

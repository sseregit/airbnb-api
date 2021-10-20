from django.core.paginator import Page
from rest_framework import pagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from .models import Room
from .serializers import RoomSerializer
from .permissions import IsOwner
from rooms import serializers

class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):

        if self.action == "list" or self.action == "retrieve":
            # GET 처리에대해 모두가 요청이 가능하게 설정.
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            # POST 처리에대해 로그인상태만 가능하게끔
            permission_classes = [permissions.IsAuthenticated]
        else:
            # PUT, DELETE Rooms의 주인만 수정,삭제가 가능해야한다.
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
        
    

@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get('max_price',None)
    min_price = request.GET.get('min_price',None)
    beds = request.GET.get('beds',None)
    bedrooms = request.GET.get('bedrooms',None)
    bathrooms = request.GET.get('bathrooms',None)
    lat = request.GET.get('lat',None)
    lng = request.GET.get('lng',None)
    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price        
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms
    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - 0.005  # 왼쪽으로
        filter_kwargs["lat__lte"] = float(lat) + 0.005  # 오른쪽으로
        filter_kwargs["lng__gte"] = float(lng) - 0.005  # 아래쪽으로
        filter_kwargs["lng__lte"] = float(lng) + 0.005  # 위쪽으로
    paginator = OwnPagination()
    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError:
        rooms = Room.objects.all()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)
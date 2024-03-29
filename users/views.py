from collections import UserString
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from .models import User
from rooms.models import Room
from rooms.serializers import RoomSerializer
from .permissions import IsSelf

# Create your views here.

class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            # Admin 계정만 확인할수있다.
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            # 누구나 만들수있음.
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        
        return (permission() for permission in permission_classes)

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username and not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = RoomSerializer(user.favs.all(), many=True, context={"request":request})
        return Response(serializer.data)
    
    @favs.mapping.put
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk",None)
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
from rest_framework import serializers
from . import models

class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (        
        "username",
        "first_name",
        "last_name",
        "email",
        "avatar",
        "superhost",)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User        
        fields = ( 
        "id",       
        "username",
        "first_name",
        "last_name",
        "email",
        "avatar",
        "superhost",)
        read_only_fields = ["id","superhost","avatar"]

    def validate_username(self, value):
        pass
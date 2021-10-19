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

    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.User        
        fields = ( 
        "id",       
        "username",
        "first_name",
        "last_name",
        "email",
        "avatar",
        "superhost",
        "password",)
        read_only_fields = ["id","superhost","avatar"]

    def validate_username(self, value):
        return value

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
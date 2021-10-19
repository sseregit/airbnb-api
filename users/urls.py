from django.urls import path
from .views import MeView, user_detail, FavsView, UserView, login

app_name = "users"

urlpatterns = [
    path("",UserView.as_view()),
    path("token/",login),
    path("me/",MeView.as_view()),
    path("me/favs/",FavsView.as_view()),
    path("<int:pk>/",user_detail),
]

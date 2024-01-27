from django.urls import URLPattern, path
from . import views

urlpatterns: list[URLPattern] = [
    path("", views.getRoutes),
    path("rooms/", views.getRooms),
    path("rooms/<str:pk>/", views.getRoom),
]

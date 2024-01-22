from django.shortcuts import render
from django.http import HttpRequest
from .models import Room


# Create your views here.
def home(request: HttpRequest):
    rooms = Room.objects.all()
    context: dict = {"rooms": rooms}
    return render(request, "base/home.html", context)


def room(request: HttpRequest, pk: str):
    room: Room = Room.objects.get(id=int(pk))
    context: dict[str, Room] = {"room": room}

    return render(request, "base/room.html", context)

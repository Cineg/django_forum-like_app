from django.shortcuts import render, redirect
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from .models import Room
from .forms import RoomForm


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    rooms = Room.objects.all()
    context: dict = {"rooms": rooms}
    return render(request, "base/home.html", context)


def room(request: HttpRequest, pk: str) -> HttpResponse:
    room: Room = Room.objects.get(id=int(pk))
    context: dict[str, Room] = {"room": room}

    return render(request, "base/room.html", context)


def createRoom(
    request: HttpRequest,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    form: RoomForm = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context: dict = {"form": form}
    return render(request, "base/room_form.html", context)


def updateRoom(request: HttpRequest, pk: str) -> HttpResponse:
    room: Room = Room.objects.get(id=pk)
    form: RoomForm = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context: dict = {"form": form}
    return render(request, "base/room_form.html", context)


def deleteRoom(request: HttpRequest, pk: str) -> HttpResponse:
    room: Room = Room.objects.get(id=int(pk))
    context: dict = {"obj": room}
    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", context)

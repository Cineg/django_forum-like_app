from django.shortcuts import render
from django.http import HttpRequest

rooms: list[dict] = [
    {"id": 1, "name": "Name number 1"},
    {"id": 2, "name": "Test name"},
    {"id": 3, "name": "Another name"},
]


# Create your views here.
def home(request: HttpRequest):
    context: dict = {"rooms": rooms}
    return render(request, "base/home.html", context)


def room(request: HttpRequest, pk: str):
    context: dict | None = None
    for room in rooms:
        if room["id"] == int(pk):
            context = {"room": room}

    return render(request, "base/room.html", context)

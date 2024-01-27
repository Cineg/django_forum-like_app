from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


@api_view(["GET"])
def getRoutes(request: HttpRequest) -> Response:
    routes: list[str] = ["GET /api", "GET /api/rooms", "GET /api/room/:id"]

    return Response(routes)


@api_view(["GET"])
def getRooms(request: HttpRequest) -> Response:
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def getRoom(request: HttpRequest, pk: str) -> Response:
    room: Room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)

    return Response(serializer.data)

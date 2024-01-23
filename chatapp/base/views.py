from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractBaseUser
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.
def loginPage(request: HttpRequest) -> HttpResponse:
    page: str = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username: str | None = request.POST.get("username")
        password: str | None = request.POST.get("password")

        try:
            user: User | AbstractBaseUser | None = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist.")

    context: dict = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    logout(request)
    return redirect("home")


def registerPage(request) -> HttpResponse:
    page: str = "register"
    form: UserCreationForm = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        is_error: bool = False

        user_exists: User | None
        try:
            user_exists = User.objects.get(username=form.data["username"])
        except:
            user_exists = None

        if not form.is_valid():
            messages.error(request, "An error occurred during registration.")
            is_error = True

        if user_exists != None:
            messages.error(request, "User already exists.")
            is_error = True

        if not is_error:
            user: User = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")

    context: dict = {"page": page, "form": form}
    return render(request, "base/login_register.html", context)


def home(request: HttpRequest) -> HttpResponse:
    q: str | None = request.GET.get("q")
    if q == None:
        q = ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    rooms_count: int = rooms.count()

    context: dict = {"rooms": rooms, "topics": topics, "rooms_count": rooms_count}
    return render(request, "base/home.html", context)


def room(request: HttpRequest, pk: str) -> HttpResponse:
    room: Room = Room.objects.get(id=int(pk))
    context: dict[str, Room] = {"room": room}

    return render(request, "base/room.html", context)


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def updateRoom(request: HttpRequest, pk: str) -> HttpResponse:
    room: Room = Room.objects.get(id=pk)
    form: RoomForm = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here.")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context: dict = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def deleteRoom(request: HttpRequest, pk: str) -> HttpResponse:
    room: Room = Room.objects.get(id=int(pk))
    context: dict = {"obj": room}

    if request.user != room.host:
        return HttpResponse("You are not allowed here.")

    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", context)

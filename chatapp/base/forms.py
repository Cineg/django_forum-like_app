from django.forms import ModelForm, TextInput
from .models import Room, UserData


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["host", "participants"]


class UserDataForm(ModelForm):
    class Meta:
        model = UserData
        fields = "__all__"
        exclude = ["user"]

from django.forms import ModelForm, TextInput
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["host", "participants"]
        widgets = {"topic": TextInput(attrs={"class": "myfieldclass"})}

from django.forms import ModelForm, IntegerField
# from django.db import models
from .models import User


class ProfileForm(ModelForm):
    age = IntegerField(
        label='Возраст',
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'age')
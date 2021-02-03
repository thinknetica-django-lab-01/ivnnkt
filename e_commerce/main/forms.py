from django.forms import ModelForm, IntegerField
from django.core.exceptions import ValidationError
from .models import User, Product


class ProfileForm(ModelForm):
    age = IntegerField(
        label='Возраст',
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'age')

    def clean_age(self):
        data = self.cleaned_data['age']

        #Проверка возраста
        if data < 18:
            raise ValidationError('Вам должно быть больше чем 18 лет')

        return data


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'discription',
            'category',
            'price',
            'in_stock',
            'seller',
            'tag',
        )
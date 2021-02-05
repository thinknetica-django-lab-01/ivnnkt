from django.forms import ModelForm, CharField, EmailField
from django.core.exceptions import ValidationError
from .models import Profile, User, Product


class ProfileForm(ModelForm):

    first_name = CharField(max_length=150,)
    last_name = CharField(max_length=150,)
    email = EmailField()


    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'age',)
        exclude = ['user']

    def clean_age(self):
        data = self.cleaned_data['age']

        #Проверка возраста
        if data < 18:
            raise ValidationError('Вам должно быть больше чем 18 лет')

        return data
      
    def save(self, *args, **kwargs):
        super(ProfileForm, self).save(*args, **kwargs)
        self.instance.username.first_name = self.cleaned_data.get('first_name')
        self.instance.username.last_name = self.cleaned_data.get('last_name')
        self.instance.username.email = self.cleaned_data.get('email')
        self.instance.username.save()



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

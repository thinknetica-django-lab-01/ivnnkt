from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Product, Profile
from django.views import generic
from django.views.generic.edit import UpdateView
from .forms import ProfileForm


def index(request):
    prod = Product.objects.all()
    user = User.objects.filter(logentry=True)
    turn_on_block = True

    return render(
        request,
        'main/index.html',
        {
            'prod': prod,
            'user': user,
            'turn_on_block': turn_on_block,
            'for_revers': 'Hello world!'
        }
    )


class ProductListView(generic.ListView):
    '''полный список товаров'''
    model = Product
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('tag')
        if query:
            queryset = Product.objects.filter(tag__name=query)
        else:
            queryset = Product.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        x = self.request.GET.get('tag')
        if x:
            context['tags'] = ''.join(["tag={}&".format(x)])
            return context
        else:
            return context


class ProductDetailView(generic.DetailView):
    '''страничка товара'''
    model = Product


class ProfileUpdate(UpdateView):
    '''Форма редактирования пользователя'''
    model = Profile
    form_class = ProfileForm
    template_name = 'main/profile_form.html'
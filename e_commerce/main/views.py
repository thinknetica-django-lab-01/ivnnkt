from django.shortcuts import render
from .models import Product, Profile
from django.views import generic
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProfileForm, ProductForm
from django.urls import reverse_lazy


def index(request):
    prod = Product.objects.all()
    turn_on_block = True

    return render(
        request,
        'main/index.html',
        {
            'prod': prod,
            'turn_on_block': turn_on_block,
            'for_revers': 'Hello world!'
        }
    )


class ProductListView(generic.ListView):
    '''полный список товаров'''
    model = Product
    form_class = ProfileForm
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


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    '''Форма редактирования пользователя'''
    model = Profile
    form_class = ProfileForm
    template_name = 'main/profile_form.html'


class ProductCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    '''станица добавления товара'''
    model = Product
    form_class = ProductForm

    def test_func(self):
        return self.request.user.groups.filter(name='sellers')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdate(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    '''станица редактирования товара'''
    model = Product
    form_class = ProductForm
    template_name_suffix = '_edit'
    success_url = reverse_lazy('goods')

    def test_func(self, *args, **kwargs):
        obj = super(UpdateView, self).get_object()
        return self.request.user == obj.owner
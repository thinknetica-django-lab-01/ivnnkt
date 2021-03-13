from django.shortcuts import render
from .models import Product, Profile, Subscriber
from django.views import generic
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProfileForm, ProductForm, SubscribForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.postgres.search import SearchVector, SearchQuery


def index(request):
    """Главная страница. Выводится список товаров,
    цена если turn_on_block = True, и пример работы фильтра revers_string.
    """
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
    """Полный список товаров."""
    model = Product
    form_class = SubscribForm
    success_url = '/goods'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('tag')
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = Product.objects.annotate(
                search=SearchVector('name', 'discription')
            ).filter(search=SearchQuery(search_query))
        elif query:
            query_list = []
            query_list.append(query)
            queryset = Product.objects.filter(tag__contains=query_list)
        else:
            queryset = Product.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        tag = self.request.GET.get('tag')
        search = self.request.GET.get('search')
        if tag:
            context['tags'] = ''.join(["tag={}&".format(tag)])
            return context
        elif search:
            context['search'] = ''.join(["search={}&".format(search)])
            return context
        else:
            return context

    def post(self, request, *args, **kwargs):
        if not Subscriber.objects.filter(username=request.user):
            subscr = Subscriber()
            subscr.username = request.user
            subscr.save()
        return HttpResponseRedirect('/')


class ProductDetailView(generic.DetailView):
    """Страничка товара."""
    model = Product

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.counter += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    """Форма редактирования пользователя."""
    model = Profile
    form_class = ProfileForm
    template_name = 'main/profile_form.html'


class ProductCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    """Станица добавления товара."""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('goods')

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
    """Станица редактирования товара."""
    model = Product
    form_class = ProductForm
    template_name_suffix = '_edit'
    success_url = reverse_lazy('goods')

    def test_func(self, *args, **kwargs) -> True:
        obj = super(UpdateView, self).get_object()
        return self.request.user == obj.owner

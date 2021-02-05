from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('goods/', views.ProductListView.as_view(), name='goods'),
    path('goods/<int:pk>/', views.ProductDetailView.as_view(), name='detail_goods'),
    path('accounts/<int:pk>/profile/', views.ProfileUpdate.as_view(), name="profile"),
]

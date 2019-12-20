from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    
    path('',views.cart_home, name='cart_home'),
    path('update', views.cart_update, name='update'),
    path('atualiza_qtd_carrinho/', views.atualiza_qtd_carrinho, name='atualiza_qtd_carrinho'),
]

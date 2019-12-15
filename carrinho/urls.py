from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    path('exibe_produtos_e_carrinho/', views.exibe_produtos_e_carrinho, name='exibe_produtos_e_carrinho'),
    path('exibe_produtos/', views.exibe_produtos, name='exibe_produtos'),
    path('exibe_carrinho/', views.exibe_carrinho, name='exibe_carrinho'),
    path('adicionar_ao_carrinho/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remove_produto_carrinho/', views.remove_produto_carrinho, name='remove_produto_carrinho'),
    path('atualiza_qtd_carrinho/', views.atualiza_qtd_carrinho, name='atualiza_qtd_carrinho'),
    path('',views.cart_home, name='cart_home')
]

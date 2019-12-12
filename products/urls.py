
from django.urls import path

app_name = "products"


from .views import (
                        #ProductListView, 
                        #ProductDetailSlugView, 
                        cadastra_produto, exibe_produto, edita_produto, remove_produto, pesquisa_produto, exibe_produtos#,product_detail_view,product_list_view
                    )

urlpatterns = [
    #path('', ProductListView.as_view(), name='list'),
    #path('<slug:slug>/', ProductDetailSlugView.as_view(), name= 'detail'),
    #path('products-fbv/', product_list_view, name ='list'), 
    #path('products-fbv/<int:pk>', product_detail_view, name = 'detail'), 
    path('cadprod/', cadastra_produto, name = 'cadprod'),
    path('exibe_produto/<int:id>/', exibe_produto, name='exibe_produto'),
    path('edita_produto/<int:id>/', edita_produto, name='edita_produto'),
    path('remove_produto/', remove_produto, name='remove_produto'),
    path('pesquisa_produto/', pesquisa_produto, name='pesquisa_produto'),
    path('exibe_produtos/', exibe_produtos, name='exibe_produtos'),



]
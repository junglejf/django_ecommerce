"""e_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from products import urls
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import home_page, about_page, contact_page, blog_page, courses_page, login_page, register_page, logout_page#, cadastra_produto, exibe_produto, edita_produto, remove_produto, pesquisa_produto, exibe_produtos


urlpatterns = [
    path('', home_page,name='home'),

    #path('admin/', admin.site.urls),
    #path('blog/', blog_page, name='blog'),
    #path('cursos/', courses_page,name='cursos'),
    #path('about/', about_page, name='about'),
    #path('contact/', contact_page, name='contact'),
    #path('login/', login_page, name='login'),  
    #path('logout/', logout_page, name='logout'),  
    #path('register/', register_page, name='register'),
    #path('cadprod/', cadastra_produto, name = 'cadprod'),
    #path('exibe_produto/<int:id>/', exibe_produto, name='exibe_produto'),
    #path('edita_produto/<int:id>/',edita_produto, name='edita_produto'),
    #path('remove_produto/', remove_produto, name='remove_produto'),
    #path('pesquisa_produto/', pesquisa_produto, name='pesquisa_produto'),
    #path('exibe_produtos/', exibe_produtos, name='exibe_produtos'),
    path('products/', include("products.urls", namespace="products")),

    

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

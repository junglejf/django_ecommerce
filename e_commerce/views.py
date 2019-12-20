from django.http import HttpResponse
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import ContactForm, LoginForm, RegisterForm
from products.forms import ProductForm, RemoveProdutoForm, PesquisaProdutoForm
from django.views.decorators.http import require_POST
from products.models import Product
from django.core.paginator import Paginator
from django.contrib import messages

def index(request):
    return render(request, 'index2.html')

def home_page(request):
    print(request.session.get("cart_id","unknow"))
    context = {
        "title":" Página principal",
        "content":"Bem-vindo a página principal"
    }
    context["usuario"] = "Seja bem vindo "+request.user.username+ " !!!"
    if request.user.is_authenticated:
        context["premium_content"] = "Você é um usuário Premium"

    if request.user.is_authenticated and request.user.is_staff:
        context["usuario"] += " Você possui funções administrativas <><><>"

    return render(request, "index.html", context)

def about_page(request):
    context = {
        "title":" Página sobre nós",
        "content":"Bem-vindo a página sobre nós"
    }
    return render(request, "about/view.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":" Página de contato",
        "content":"Bem-vindo a página de contato",
        "form": contact_form,
        "brand": "Novo nome da marca"
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get('Nome_Completo'))
        print(request.POST.get('email'))
        print(request.POST.get('Mensagem'))
    return render(request, "contact/view.html", context)

def blog_page(request):
    context = {
        "title":" Página de blog",
        "content":"Bem-vindo a página de blog"
    }
    return render(request, "blog/blog.html", context)

def courses_page(request):
    context = {
        "title":" Página de courses",
        "content":"Bem-vindo a página de courses"
    }
    return render(request, "cursos/cursos.html", context)
    
User = get_user_model()
def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
                    "form": form
              }
    print("User logged in")
    print(request.user.is_authenticated)
    print("USer ------>>>>>>"+str(User))
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password) 
        print(user)
        print(request.user.is_authenticated)
        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            print("Login válido")
            # Redireciona para uma página de sucesso.
            return redirect("/")
        else:
            #Retorna uma mensagem de erro de 'invalid login'.
            print("Login inválido")
    return render(request, "auth/login.html", context)

def logout_page(request):
    context = {
            "content": "Você efetuou logout com sucesso! :("
    }
    logout(request)
    return render(request, "auth/logout.html", context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
                    "form": form
              }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    return render(request, "auth/register.html", context)


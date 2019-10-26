from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm

def home_page(request):
    context = {
        "title":" Página principal",
        "content":"Bem-vindo a página principal"
    }
    return render(request, "index.html", context)

def about_page(request):
    context = {
        "title":" Página sobre nós",
        "content":"Bem-vindo a página sobre nós"
    }
    return render(request, "about/about.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":" Página de contato",
        "content":"Bem-vindo a página de contato",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get('Nome_Completo'))
        print(request.POST.get('email'))
        print(request.POST.get('Mensagem'))
    return render(request, "contact/contact.html", context)

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
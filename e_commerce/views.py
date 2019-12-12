from django.http import HttpResponse
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import ContactForm, LoginForm, RegisterForm
from products.forms import ProductForm, RemoveProdutoForm, PesquisaProdutoForm
from django.views.decorators.http import require_POST
from products.models import Product
from django.core.paginator import Paginator
from django.contrib import messages



def home_page(request):
    context = {
        "title":" Página principal",
        "content":"Bem-vindo a página principal"
    }
    context["usuario"] = "Seja bem vindo "+request.user.username+ " !!!"
    if request.user.is_authenticated:
        context["premium_content"] = "Você é um usuário Premium"

    if request.user.is_authenticated and request.user.is_staff:
        context["usuario"] += " Você possui funções administrativas <><><>"

    return render(request, "index2.html", context)

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

def cadastra_produto(request):
    if request.POST:
        produto_id = request.POST.get('products_product_id')
        print(produto_id)
        if produto_id:
            produto = get_object_or_404(Product, pk=produto_id)
            produto_form = ProductForm(request.POST, instance=produto)
        else:
            produto_form = ProductForm(request.POST)

        if produto_form.is_valid():
            produto = produto_form.save()
            if produto_id:
                messages.add_message(request, messages.INFO, 'Produto alterado com sucesso!')
            else:
                messages.add_message(request, messages.INFO, 'Produto cadastrado com sucesso!')
            return redirect('exibe_produto', id=produto.id)
        else:
            messages.add_message(request, messages.ERROR, 'Corrija o(s) erro(s) abaixo.')
    else:
        produto_form = ProductForm()
    print("produto form = "+str(produto_form))
    print("\n MESSAGES DO form = "+str(messages))
    return render(request, 'cadprod/cadprod2.html', {'form': produto_form })

def exibe_produto(request, id):
    produto = get_object_or_404(Product, pk=id)
    print("EXIBE_PRODUTO") 
    print(produto)
    print(produto.id)
    form_remove_produto = RemoveProdutoForm(initial={'products_product_id': id})
    print(form_remove_produto)
    return render(request, 'cadprod/exibe_produto.html', {'products': produto,'form_remove_produto': form_remove_produto})

def edita_produto(request, id):
    produto = get_object_or_404(Product, pk=id)
    produto_form = ProductForm(instance=produto)
    produto_form.fields['products_product_id'].initial = id
    return render(request, 'cadprod/cadprod2.html', {'form': produto_form })

def remove_produto(request):
    form_remove_produto = RemoveProdutoForm(request.POST)
    if form_remove_produto.is_valid():
        products_product_id = form_remove_produto.cleaned_data['products_product_id']
        produto = get_object_or_404(Produto, id=products_product_id)
        produto.delete()
        messages.add_message(request, messages.INFO, 'Produto removido com sucesso.')
        return render(request, 'cadprod/exibe_produto.html', {'produto': produto})
    else:
        raise ValueError('Ocorreu um erro inesperado ao tentar remover um produto (produto_id não foi validado).')


def pesquisa_produto(request):
    form = PesquisaProdutoForm()
    return render(request, 'cadprod/pesquisa_produto.html', {'form': form})


def exibe_produtos(request):
    # buscaPor = request.GET.get('buscaPor')
    form = PesquisaProdutoForm(request.GET)
    if form.is_valid():
        buscaPor = form.cleaned_data['buscaPor']
        lista_de_produtos = Produto.objects.filter(nome__contains=buscaPor)
        paginator = Paginator(lista_de_produtos,5)
        pagina = request.GET.get('pagina')
        produtos = paginator.get_page(pagina)
    else:
        raise ValueError('Ocorreu um erro inesperado ao pesquisar produtos.')

    return render(request, 'cadprod/pesquisa_produto.html', {'form': form,
                                                             'produtos': produtos})
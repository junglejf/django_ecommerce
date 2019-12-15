from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render

from carrinho.carrinho import Carrinho
from carrinho.forms import QuantidadeForm, RemoveProdutoDoCarrinhoForm
from products.models import Product

def cart_home(request):
    #print(request.session)
    #print(dir(request.session))
    #request.session.set_expiry(300) , 5 minutos
    #request.session.session_key
    #print(request.session.session_key)
    username = request.user.username
    request.session['cart_id'] = username
    return render(request,'carrinho/cart_home.html',{})

def exibe_produtos_e_carrinho(request):
    return render(request, 'carrinho/vendas.html')


def exibe_produtos(request):
    produtos = Product.objects.all()
    lista_de_forms = []
    for produto in produtos:
        lista_de_forms.append(QuantidadeForm(initial={'quantidade': 0}))

    return render(request, 'carrinho/produtos_a_venda.html',  {
       'listas': zip(produtos, lista_de_forms)
    })   


def exibe_carrinho(request):
    carrinho = Carrinho(request)

    lista_de_produtos_no_carrinho = carrinho.get_produtos()

    produtos_no_carrinho = []
    lista_de_forms = []
    valor_do_carrinho = 0
    for item in lista_de_produtos_no_carrinho:
        produtos_no_carrinho.append(item['produto'])
        lista_de_forms.append(QuantidadeForm(initial={'quantidade': item['quantidade']}))
        valor_do_carrinho = valor_do_carrinho + int(item['quantidade']) * Decimal(item['preco'])
    
    return render(request, 'carrinho/produtos_no_carrinho.html',  {
       'listas': zip(produtos_no_carrinho, lista_de_forms),
       'valor_do_carrinho': valor_do_carrinho
    })


def adicionar_ao_carrinho(request):
    form = QuantidadeForm(request.POST)
    if form.is_valid():
        quantidade = form.cleaned_data['quantidade']
        produto_id = form.cleaned_data['produto_id']

        carrinho = Carrinho(request)
        carrinho.adicionar(produto_id, quantidade)

        return exibe_carrinho(request)
    else:
        print(form.errors)
        raise ValueError('Ocorreu um erro inesperado ao adicionar um produto ao carrinho.')


def remove_produto_carrinho(request):
    form = RemoveProdutoDoCarrinhoForm(request.POST)
    if form.is_valid():
        carrinho = Carrinho(request)
        carrinho.remover(form.cleaned_data['produto_id'])

        return exibe_carrinho(request)
    else:
        print(form.errors)
        raise ValueError('Ocorreu um erro inesperado ao adicionar um produto ao carrinho.')


def atualiza_qtd_carrinho(request):
    form = QuantidadeForm(request.POST)
    if form.is_valid():
        produto_id = form.cleaned_data['produto_id']
        quantidade =  form.cleaned_data['quantidade']

        carrinho = Carrinho(request)
        carrinho.alterar(produto_id, quantidade)

        return exibe_carrinho(request)
    else:
        print(form.errors)
        raise ValueError('Ocorreu um erro inesperado ao adicionar um produto ao carrinho.')

from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect ,get_object_or_404

from carrinho.carrinho import Carrinho
from carrinho.forms import QuantidadeForm, RemoveProdutoDoCarrinhoForm
from products.models import Product
from .models import Cart

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "id": x.id,
        "url":x.get_absolute_url(),
        "name": x.name,
        "price":x.price
        } 
        for x in cart_obj.products.all()]
    #product_list = []
    #for x in cart_obj.products.all():
        #product_list.append({"name":x.name, "price":x.price})

    cart_data = {"products":products, "subtotal":cart_obj.subtotal, "total":cart_obj.total}
    return JsonResponse (cart_data)

def cart_home(request):
    cart_obj, new_obj= Cart.objects.new_or_get(request)

    return render(request,'carrinho/cart_home.html',{"cart":cart_obj})

def cart_update(request):
    
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("carrinho:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj) 
            added = True
        request.session['cart_items'] = cart_obj.products.count()
 
        if request.is_ajax():
            print("request AJAX")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data)
    #cart_obj.products.add(product_id)
    #cart_obj.products.remove(obj)
    return redirect("carrinho:cart_home")

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

from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect ,get_object_or_404
from carrinho.forms import QuantidadeForm, RemoveProdutoDoCarrinhoForm, CartAddProductForm
from products.models import Product
from .models import Cart


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = []
    for x in cart_obj.products.all():
        products.append({"id": x.id,"url":x.get_absolute_url(),"name": x.name,"price":x.price,"selected":x.selected, "quantidade":x.price * x.selected } )

    cart_data = {"products":products, "subtotal":cart_obj.subtotal, "total":cart_obj.total }
    return JsonResponse (cart_data)

def cart_home(request):
    cart_obj, new_obj= Cart.objects.new_or_get(request)
    lista_de_forms = []
    valor_do_carrinho = 0
    for x in cart_obj.products.all():
        lista_de_forms.append(QuantidadeForm(initial={'quantidade': x.quantidade}))
        valor_do_carrinho = valor_do_carrinho + int(x.quantidade) * Decimal(x.price)
    
    return render(request,'carrinho/cart_home.html',{"cart":cart_obj, "listas":lista_de_forms})

def cart_update(request):
    
    product_id = request.POST.get('product_id')
    #print("linha 42")
    #print(dir(product_id))
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
            #if 'selected' not in dir(product_obj):
             #   product_obj.selected = 1
              #  product_obj.save()
            #product_obj.selecionado = 0
            
     #       print(product_obj)
      #      print(product_obj.id)
       #     print("produtos selecionads"+str(product_obj.selected))
        except Product.DoesNotExist:
            print("Product not found")
            return redirect("carrinho:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
        #    print(product_obj)
         #   print(product_obj.id)
          #  print("produtos selecionads XXX = "+str(product_obj.selected))
            cart_obj.products.add(product_obj) 
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        
 
        if request.is_ajax():
           # print("request AJAX")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data)
    #cart_obj.products.add(product_id)
    #cart_obj.products.remove(obj)
    return redirect("carrinho:cart_home")

def atualiza_qtd_carrinho(request):
    form = QuantidadeForm(request.POST)
    if form.is_valid():
        produto_id = form.cleaned_data['produto_id']
        quantidade =  form.cleaned_data['quantidade']

        carrinho = Cart(request)
        carrinho.alterar(produto_id, quantidade)

        return cart_update(request)
    else:
        print(form.errors)
        raise ValueError('Ocorreu um erro inesperado ao adicionar um produto ao carrinho.')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'carrinho/cart_home.html', {'cart': cart})
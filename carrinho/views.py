from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect ,get_object_or_404

from carrinho.carrinho import Carrinho
from carrinho.forms import QuantidadeForm, RemoveProdutoDoCarrinhoForm
from products.models import Product
from .models import Cart

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    #products = [{
        #"id": x.id,
        #"url":x.get_absolute_url(),
        #"name": x.name,
        #"price":x.price,
        # "selected":x.selected
      #  } 
     #   for x in cart_obj.products.all()]
    products= []
    for x in cart_obj.products.all():
            products.append({"id": x.id,"url":x.get_absolute_url(),"name": x.name,"price":x.price,"selected":x.selected, "quantidade":x.price * x.selected } )

    cart_data = {"products":products, "subtotal":cart_obj.subtotal, "total":cart_obj.total}
    return JsonResponse (cart_data)

def cart_home(request):
    cart_obj, new_obj= Cart.objects.new_or_get(request)
    for x in cart_obj.products.all():
        x.quantidade = x.price * x.selected
    
    return render(request,'carrinho/cart_home.html',{"cart":cart_obj})

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
            print("Show message to user, product is gone?")
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

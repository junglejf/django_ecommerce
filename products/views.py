from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .models import Product
#from .forms import ProductForm

#from django.contrib import messages
#from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from e_commerce import forms
from .forms import ProductForm

#liestar todos os prodtuos que estiverem com destaque
class ProductFeaturedListView(ListView):
    template_name = "products/list.html"
    
    def get_queryset(self, *args, **kwargs):
        return Product.objects.featured()

#listar os detalhes de cada produto em destaque
class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"
    
class ProductListView(ListView):
    #traz todos os produtos do banco de dados sem filtrar nada 
    queryset = Product.objects.all()
    template_name = "products/list.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        print(" ===> context ProductListView ="+str(context))
        return context

#Function Based Vie

#def product_list_view(request):
    #return "aqui"
    #queryset = Product.objects.all()
    #context = {
        #'object_list': queryset
    #}
    #return render(request, "products/list.html", context)
    

#Class Based View
class ProductDetailView(DetailView):
    #traz todos os produtos do banco de dados sem filtrar nada 

    queryset = Product.objects.all()
    template_name = "products/detail.html"
    
    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(" ===> context ProductDETAILVIEW ="+str(context))
        return context


#Function Based View
#def product_detail_view(request, pk= None, *args, **kwargs):
    #print(args)
    #print(kwargs)
    #instance = Product.objects.get(pk = pk) #get the object id
    #instance = get_object_or_404(Product, pk = pk)
    #qs = Product.objects.filter(id = pk)
    #if qs.count() == 1: #só chega um produto, se chegar 0 da uma excessão
    #    instance = qs.first()
    #else:
    #    raise Http404("Esse produto não existe!")
    #context = {
    #    'object': instance
    #}
    #return render(request, "products/detail.html", context)

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug = slug, active = True)
        try:
            instance = Product.objects.get(slug = slug, active = True)
        except Product.DoesNotExist:
            raise Http404("Não encontrado!")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug = slug, active = True)
            instance =  qs.first()
        return instance

### Cadastro de produto com paginação


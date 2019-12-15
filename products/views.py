from django.views.generic import ListView, DetailView

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages

from .models import Product
#from .forms import ProductForm

#from django.contrib import messages
#from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .forms import ProductForm, RemoveProdutoForm, PesquisaProdutoForm
from django.core.paginator import Paginator
from datetime import datetime, timedelta

"""
#Class Based View
class ProductListView(ListView):
    #traz todos os produtos do banco de dados sem filtrar nada 
    queryset = Product.objects.all()
    template_name = "products/list.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        print(" ===> context ProductListView ="+str(context))
        return context

class ProductDetailView(DetailView):
    #traz todos os produtos do banco de dados sem filtrar nada 
    queryset = Product.objects.all()
    template_name = "products/detail.html"
    
    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(" ===> context ProductDETAILVIEW ="+str(context))
        return context


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

#listar todos os prodtuos que estiverem com destaque
class ProductFeaturedListView(ListView):
    template_name = "products/list.html"
    
    def get_queryset(self, *args, **kwargs):
        return Product.objects.featured()

#listar os detalhes de cada produto em destaque
class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"
    


#Function Based View
"""
def product_list_view(request):

    #return "aqui"
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    print("context from list_view = = ="+str(context))
    return render(request, "products/list.html", context)
    
def product_detail_view(request, pk=None, *args, **kwargs):
    print("args:"+str(args))
    print("kwargs:"+str(kwargs))
    print("request:"+str(request))
    print("pk:"+str(pk))
    slug = kwargs.get('slug')
    print("slug = "+slug)
    #instance = Product.objects.get(pk = pk) #get the object id
    #instance = get_object_or_404(Product, pk = pk)
    instance = get_object_or_404(Product, slug = slug, active = True)
    print("pk-instance:"+str(pk))
    context = {
        'object': instance
    }
    print("context ===> "+str(context))

    return render(request, "products/detail.html", context)
 




### Cadastro de produto com paginação

def cadastra_produto(request):
    if request.POST:
        produto_id = request.POST.get('produto_id')
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
            return redirect('products:exibe_produto', id=produto.id)
        else:
            messages.add_message(request, messages.ERROR, 'Corrija o(s) erro(s) abaixo.')
    else:
        produto_form = ProductForm()

    return render(request, 'products/cadastra_produto.html', {'form': produto_form })


def exibe_produto(request, id):
    produto = get_object_or_404(Product, pk=id)
    print("Produto")
    print(produto)
    print(produto.price)
    form_remove_produto = RemoveProdutoForm(initial={'produto_id': id})
    print("Produto")
    print(produto)
    print(produto.id)
    print(form_remove_produto)
    print(request)
    return render(request, 'products/exibe_produto.html', {'produto': produto,
                                                          'form_remove_produto': form_remove_produto})


def edita_produto(request, id):
    produto = get_object_or_404(Product, pk=id)
    produto_form = ProductForm(instance=produto)
    produto_form.fields['produto_id'].initial = id
    return render(request, 'products/cadastra_produto.html', {'form': produto_form })


def remove_produto(request):
    form_remove_produto = RemoveProdutoForm(request.POST)
    if form_remove_produto.is_valid():
        produto_id = form_remove_produto.cleaned_data['produto_id']
        produto = get_object_or_404(Product, id=produto_id)
        produto.delete()
        messages.add_message(request, messages.INFO, 'Produto removido com sucesso.')
        return render(request, 'products/exibe_produto.html', {'produto': produto})
    else:
        raise ValueError('Ocorreu um erro inesperado ao tentar remover um produto (produto_id não foi validado).')


def pesquisa_produto(request):
    form = PesquisaProdutoForm()
    return render(request, 'products/pesquisa_produto.html', {'form': form})


def exibe_produtos(request):
    # buscaPor = request.GET.get('buscaPor')
    form = PesquisaProdutoForm(request.GET)
    if (form.is_valid()):
        buscaPor = form.cleaned_data['buscaPor']
        lista_de_produtos = Product.objects.filter(title__contains=buscaPor).order_by('title')
        paginator = Paginator(lista_de_produtos,5)
        pagina = request.GET.get('pagina')
        produtos = paginator.get_page(pagina)
    else:
        raise ValueError('Ocorreu um erro inesperado ao pesquisar produtos.')
    print("-EXIBEPRODUTOS FORM->"+str(form))
    return render(request, 'products/pesquisa_produto.html', {'form': form,
                                                             'produtos': produtos})
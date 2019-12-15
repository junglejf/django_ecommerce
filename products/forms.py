from decimal import Decimal
from django import forms
from django.core.validators import RegexValidator
from products.models import Product, Category
from e_commerce import settings

from django.contrib.auth import get_user_model


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('produto_id', 'title', 'description', 'price','category','reg_date','quantidade')

    produto_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    title = forms.CharField(
        error_messages={'required': 'Campo obrigatório.',
                        'unique': 'Produto duplicado.'},
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
        required=True)

    description = forms.CharField(
        error_messages={'required': 'Campo obrigatório.',
                        'unique': 'Produto duplicado.'},
        widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
        required=True)

    price = forms.CharField(
        localize=True,
        error_messages={'required': 'Campo obrigatório.', },
        validators=[RegexValidator(regex='^[0-9]{1,7}(,[0-9]{2})?$', message="Informe o valor no formato 9999999,99.")],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'maxlength': '10',
                                      'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'}),
        required=True)    

    category = forms.ModelChoiceField(
        error_messages={'required': 'Campo obrigatório.', },
        queryset=Category.objects.all().order_by('name'),
        empty_label='--- Selecione uma categoria ---',
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        required=True)

    reg_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm'}),
        required=True)
    
    quantidade = forms.CharField(
        localize=True,
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'maxlength': '10'}),
        required=True)  
    #print("produto_form l20.",products_product_id,title) 

    def clean_price(self):
        price = self.cleaned_data.get('price')
        
        if not price:
            return price
        
        price = Decimal(price.replace(',', '.'))

        return price

class RemoveProdutoForm(forms.Form):
    class Meta:
        fields = ('produto_id')

    produto_id = forms.CharField(widget=forms.HiddenInput(), required=True)

    # <input type="hidden" name="produto_id" id="id_produto_id" value="xxx">


class PesquisaProdutoForm(forms.Form):
    class Meta:
        fields = ('buscaPor')

    buscaPor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
        required=False)
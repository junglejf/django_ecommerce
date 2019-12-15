from django import forms

class RemoveProdutoDoCarrinhoForm(forms.Form):
    class Meta:
        fields = ('produto_id')

    produto_id = forms.CharField(widget=forms.HiddenInput())

class QuantidadeForm(forms.Form):
    class Meta:
        fields = ('quantidade', 'produto_id')

    # <input type="hidden" name="produto_id" id="id_produto_id" value="xxx">
    produto_id = forms.CharField(widget=forms.HiddenInput())

    quantidade = forms.IntegerField(
        min_value=1,
        max_value=1000,
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm quantidade',
                                      'maxlength': '20',
                                      'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'}),
        required=True)

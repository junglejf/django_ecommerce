from decimal import Decimal
from e_commerce import settings

from products.models import Product

class Carrinho(object):

    def __init__(self, request):
        """ Initializa o carrinho de compras. """

        # Para que a sessão possa ser acessada por outros métodos
        self.session = request.session

        # recupera o carrinho da sessão e o salva na variável de instância 
        # carrinho
        self.carrinho = self.session.get(settings.CARRINHO_SESSION_ID)

        # Se a sessão não tiver um carrinho
        if not self.carrinho:
            # cria um carrinho vazio e o salva na sessão e na variável de 
            # instância carrinho. self.carrinho contém um dicionário com  
            # pares de chave e valor. A chave será o id de um produto e o 
            # valor será um dicionário contendo o id do produto, a quantidade 
            # e o preço.
            self.carrinho = self.session[settings.CARRINHO_SESSION_ID] = {}
        # Observação:
        # -----------
        # Nosso dicionário para o carrinho deve utilizar ids dos produtos como 
        # chaves e um dicionário com o id do produto, a quantidade e o preço, 
        # como valor. Fazendo isso, podemos garantir que um produto não é 
        # adicionado mais de uma vez no carrinho.
        #
        # print(carrinho)  # {1: {'id': 1, 'quantidade': 10, 'preco': '100'}}

    def __len__(self):
        """ Conta todos os itens no carrinho. """
        return sum(item['quantidade'] for item in self.carrinho.values())

    def get_produtos(self):
        # O carrinho tem o formato abaixo:

        #   {'1': {'id': 1, 'preco': 100, 'quantidade': 5},
        #    '2': {'id': 2, 'preco': 200, 'quantidade': 3}}

        lista = []
        for item in self.carrinho.values():
            produto = Product.objects.get(id=item['id'])
            lista.append({'produto': produto,
                          'preco': item['price'],
                          'quantidade': item['quantidade']})
        return lista
        # A lista retornada tem o formato abaixo:

        # [{'produto': obj_produto1, 'preco': 100.0, 'quantidade': 5},
        #  {'produto': obj_produto2, 'preco': 200.0, 'quantidade': 3}]


    def adicionar(self, id, quantidade):
        """ Adiciona um produto ao carrinho ou atualiza suas quantidades. """

        #   {'1': {'id': 1, 'preco': 100, 'quantidade': 5},
        #    '2': {'id': 2, 'preco': 200, 'quantidade': 3}}

        produto = Produto.objects.get(id=id)

        if id not in self.carrinho:
            self.carrinho[id] = {'id': id, 'preco': str(produto.preco), 'quantidade': quantidade}
        else:
            # Como o objeto sessão não é modificado, isto é, apenas o objeto carrinho foi alterado,
            # logo esta modificação não será salva!
            self.carrinho[id]['quantidade'] += quantidade

        self.salvar()        
        # O método salvar é chamado para que o carrinho seja salvo na sessão


    def alterar(self, id, quantidade):
        """ Adiciona um produto ao carrinho ou atualiza suas quantidades. """

        # if id in self.carrinho:
        
        self.carrinho[id]['quantidade'] = quantidade
        self.salvar()  # O método salvar é chamado para que o carrinho
                       # seja salvo na sessão.
        # else:
        #    self.adicionar(id, quantidade)

    def remover(self, id):
        """ Remove a produto from the carrinho. """

        if id in self.carrinho:
            del self.carrinho[id]
            self.salvar()   
        # O método salvar é chamado para que o carrinho seja salvo na sessão

    # Nós utilizamos o id do produto como chave no carrinho. Convertemos o ID 
    # do produto em um string uma vez que o Django utiliza JSON para serializar 
    # dados da sessão e o JSON apenas permite strings. O ID do produto é a 
    # chave e o valor que persistimos é um dicionário com o id do produto, a 
    # quantidade e o preço do produto. O preço do produto é convertido de decimal 
    # em string para ser serializado. Finalmente, chamamos o método salvar para 
    # salvar o carrinho na sessão. O método  salvar salva na sessão todas as  
    # mudanças  efetuadas no carrinho e marca a sessão como modificada utilizando 
    # session.modified = true.  Isto diz ao Django que a sessão foi modificada e 
    # que necessita ser salva.

    def salvar(self):
        # A linha abaixo atualiza o carrinho na sessão para que a sessão seja 
        # salva. Se o conteúdo do carrinho for alterado mas a referência para 
        # o carrinho não for salva na sessão, conforme vem na linha abaixo, 
        # ela não será salva. 
        # self.session[settings.CARRINHO_SESSION_ID] = self.carrinho

        # Já a linha abaixo marca a sessão como "modificada" para fazer com 
        # que ela seja salva. Isso não será necessário se o comentário da 
        # linha acima for removido.
        self.session.modified = True

        # Tudo em Python é um objeto. Um objeto mutável pode ser modificado
        # após ser criado, e um objeto imutável não pode. Objetos de tipos 
        # embutidos (built-in types) como (int, float, bool, str, tuple, 
        # unicode) são imutáveis. Objetos de tipos embutidos como (list, set, 
        # dict) são mutáveis. 

    def limpar(self):
        # Esvazia o carrinho
        self.session[settings.CARRINHO_SESSION_ID] = {}
        # self.session.modified = True 
        # A linha acima não é necessária pois a sessão está sendo alterada.

    def get_preco_total(self):
        return sum(Decimal(item['preco']) * item['quantidade'] for item in self.carrinho.values())

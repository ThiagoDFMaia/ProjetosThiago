class Pessoa:
    def __init__(self, nome, rg, cpf, endereco, numero, complemento, cidade, uf, cep, telefone_01, telefone_02, telefone_03):
        self.nome = nome
        self.rg = rg
        self.cpf = cpf
        self.endereco = endereco
        self.numero = numero
        self.complemento = complemento
        self.cidade = cidade
        self.uf = uf
        self.cep = cep
        self.telefone_01 = telefone_01
        self.telefone_02 = telefone_02
        self.telefone_03 = telefone_03

   
class Convenio:
    def __init__(self,cnpj,descricao):
        self.cnpj=cnpj
        self.descricao=descricao




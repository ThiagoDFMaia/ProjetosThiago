class Pessoa:
    def __init__(self, nome, rg, cpf,data_nas, endereco, numero, complemento, cidade, uf, cep, telefone_01, telefone_02, telefone_03):
        self.nome = nome
        self.rg = rg
        self.cpf = cpf
        self.data_nas=data_nas
        self.endereco = endereco
        self.numero = numero
        self.complemento = complemento
        self.cidade = cidade
        self.uf = uf
        self.cep = cep
        self.telefone_01 = telefone_01
        self.telefone_02 = telefone_02
        self.telefone_03 = telefone_03

    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nas":self.data_nas,
            "telefone_o1":self.telefone_01,
            "telefone_02":self.telefone_02,
            "telefone_03":self.telefone_03

           
        }

   
class Convenio:
    def __init__(self,cnpj,descricao):
        self.cnpj=cnpj
        self.descricao=descricao




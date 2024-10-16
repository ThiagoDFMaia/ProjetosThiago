class Pessoa:
    def __init__(self,nome, rg, cpf,data_nas, endereco, numero, complemento, cidade, uf, cep, telefone_01, telefone_02, telefone_03,id=None):
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
        self.id=id
 


class Paciente ():
    def __init__(self,fk_pessoa_id, tipoconvenio, fk_convenio_id, flgconvenio):
        # Inicializa os atributos herdados da classe Pessoa
       
        self.fk_pessoa_id=fk_pessoa_id
        self.flgconvenio=flgconvenio
        self.tipoconvenio=tipoconvenio
        self.fk_convenio_id=fk_convenio_id



class Medico():
    def __init__(self, fk_pessoa_id,codmedico, crm, flgativo,codespecialidade):
          
        # Atributos específicos de Medico
        self.codmedico = codmedico
        self.crm = crm
        self.flgativo = flgativo
        self.fk_pessoa_id=fk_pessoa_id
        self.codespecialidade=codespecialidade


    def ativar_medico(self):
        """Ativa o médico se estiver inativo."""
        self.flgativo = 1

    def desativar_medico(self):
        """Desativa o médico se estiver ativo."""
        self.flgativo = 0

    def __repr__(self):
        status = "Ativo" if self.flgativo else "Inativo"
        return f"Medico(CRM: {self.crm}, Nome: {self.nome}, Status: {status})"


class Convenio:
    def __init__(self,cnpj,descricao):
        self.cnpj=cnpj
        self.descricao=descricao


class Especialidade:
    def __init__(self,descricao,codespecialidade):
        self.descricao=descricao
        self.codespecialidade=codespecialidade

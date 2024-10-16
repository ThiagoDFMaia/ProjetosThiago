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
 

    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nas":self.data_nas,
            "telefone_o1":self.telefone_01,
            "telefone_02":self.telefone_02,
            "telefone_03":self.telefone_03

           
        }

class Paciente (Pessoa):
    def __init__(self,fk_pessoa_id, nome, endereco, cep, uf, cidade, complemento, numero, telefone_01, telefone_02, telefone_03, rg, cpf, data_nas, tipoconvenio, fk_convenio_id, flgconvenio):
        # Inicializa os atributos herdados da classe Pessoa
        super().__init__(nome=nome,endereco= endereco,cep= cep,uf= uf,cidade= cidade,complemento= complemento,numero= numero,telefone_01= telefone_01,telefone_02= telefone_02, telefone_03=telefone_03,rg= rg,cpf= cpf,data_nas= data_nas)
        self.fk_pessoa_id=fk_pessoa_id
        self.flgconvenio=flgconvenio
        self.tipoconvenio=tipoconvenio
        self.fk_convenio_id=fk_convenio_id

    def retornar_dados_pessoais(self):
        return Pessoa(nome=self.nome,
                endereco=self.endereco,
                cep=self.cep,
                uf=self.uf,
                cidade=self.cidade,
                complemento=self.complemento,
                numero=self.numero,
                telefone_01=self.telefone_01,
                telefone_02=self.telefone_02,
                telefone_03=self.telefone_03,
                rg=self.rg,
                cpf=self.cpf,
                data_nas=self.data_nas,
                tipo=self.tipo)

class Medico(Pessoa):
    def __init__(self, id_pessoa, nome, endereco, cep, uf, cidade, complemento, numero, telefone_01, telefone_02, telefone_03, rg, cpf, data_nas, codmedico, crm, flgativo,codespecialidade):
        # Inicializa os atributos herdados da classe Pessoa
        super().__init__(nome=nome,endereco= endereco,cep= cep,uf= uf,cidade= cidade,complemento= complemento,numero= numero,telefone_01= telefone_01,telefone_02= telefone_02, telefone_03=telefone_03,rg= rg,cpf= cpf,data_nas= data_nas)
        
        # Atributos específicos de Medico
        self.codmedico = codmedico
        self.crm = crm
        self.flgativo = flgativo
        self.id_pessoa=id_pessoa
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

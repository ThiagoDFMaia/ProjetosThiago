from pydantic import BaseModel
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

class Usuario ():
    def __init__(self,fk_pessoa_id, login, senha, flgativo):
        # Inicializa os atributos herdados da classe Pessoa
       
        self.fk_pessoa_id=fk_pessoa_id
        self.login=login
        self.senha=senha
        self.flgativo=flgativo

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

class Escala:
    def __init__(self,data,quantvagasmanha,quantvagastarde,quantvagasnoite,flaativo,codmedico):
        self.data=data
        self.quantvagasmanha=quantvagasmanha
        self.quantvagastarde=quantvagastarde
        self.quantvagasnoite=quantvagasnoite
        self.flaativo=flaativo
        self.codmedico=codmedico

class Agendamento:
    def __init__(self,dataagenda,datacadastro,flgsituacao,fk_paciente_id,escala_id,horaagendamento,turno):
       
        self.dataagenda=dataagenda
        self.datacadastro=datacadastro
        self.flgsituacao=flgsituacao
        self.fk_paciente_id=fk_paciente_id
        self.escala_id=escala_id
        self.horaagendamento=horaagendamento
        self.turno=turno




class Prontuario:
    def __init__(self,fk_paciente_id,anamnese,conclusao_diagnostica,lista_de_problemas,cid,fk_codmedico,dataAgenda,fk_codigo_agendamento):
       
        self.fk_paciente_id=fk_paciente_id
        self.anamnese=anamnese
        self.conclusao_diagnostica=conclusao_diagnostica
        self.lista_de_problemas=lista_de_problemas
        self.cid=cid
        self.fk_codmedico=fk_codmedico
        self.dataAgenda=dataAgenda
        self.fk_codigo_agendamento=fk_codigo_agendamento


class CancerFeatures(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float
    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float
    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float

class InfartoFeatures(BaseModel):
    age: float
    sex: float
    cp: float
    trtbps: float
    chol: float
    fbs: float
    restecg: float
    thalachh: float
    exng: float
    oldpeak: float
    slp: float
    caa: float
    thall: float
 
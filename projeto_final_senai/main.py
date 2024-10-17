# pip install flask (no terminal)
# importando modulos
from flask import Flask,render_template,request,redirect,url_for,jsonify
import urllib.parse
# realizar o mapeamento objeto relacional -DB First
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, relationship
from biblioteca import *

# definindo objeto flask
app = Flask(__name__)

app.secret_key = "df6e83eb7983f75b2561c875cbebc40ab9900624b22c6040f5831ecd6faaea429f043b35bd5a6fae4692fa6c80fdcf060f61207f53eb744ba684f84517fc9881sua chave secreta"


user = 'root'
password = urllib.parse.quote_plus('123456')
host = 'localhost'
database = 'clinica'
# ==========================================
#           connection string
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'


engine = create_engine(connection_string)

#  Refletindo o Banco de Dados
metadata = MetaData()
metadata.reflect(engine)

"""
-- Cria uma classe base que vai mapear 
-- Automaticamente as tabelas do banco de dados 
-- Que estão descritas no objeto metadata.

"""
Base = automap_base(metadata=metadata) # definindo a classe

"""
--Esse método realiza o mapeamento das tabelas para classes Python, 
--Gera uma classe para cada tabela 
--Pode ser usada para interagir com os dados diretamente.
"""
Base.prepare() # mapeando


Pessoa =  Base.classes.pessoa
Paciente= Base.classes.paciente
Convenio= Base.classes.convenio
Medico=Base.classes.medico
Especialidade=Base.classes.especialidade
Escala=Base.classes.escala


# Relacionamentos entre tabelas
#Medico.pessoa = relationship("Pessoa", backref="medicos", foreign_keys=[Medico.fk_pessoa_id])
'''
Medico.pessoa = relationship("Pessoa", back_populates="medicos", foreign_keys=[Medico.fk_pessoa_id])
Pessoa.medicos = relationship("Medico", back_populates="pessoa")
'''


Session = sessionmaker(bind=engine)


# funcoes
def lista_convenios():
    session_db = Session()
  
    try:
        # Executa a consulta e retorna todos os convênios
        convenios = session_db.query(Convenio).order_by(Convenio.id).all()
       
    except Exception as e:
        session_db.rollback()

        return []
    finally:
        session_db.close()

    return convenios

def gravar_pessoa(pessoa):
    session_db = Session()
    
    try:
        # Verifica se já existe uma pessoa com o mesmo CPF
        pessoa_existente = session_db.query(Pessoa).filter_by(cpf=pessoa.cpf).first()

        if pessoa_existente:
            # Atualiza os dados da pessoa existente
            pessoa_existente.nome = pessoa.nome
            pessoa_existente.endereco = pessoa.endereco
            pessoa_existente.cep = pessoa.cep
            pessoa_existente.uf = pessoa.uf
            pessoa_existente.cidade = pessoa.cidade
            pessoa_existente.complemento = pessoa.complemento
            pessoa_existente.numero = pessoa.numero
            pessoa_existente.telefone_01 = pessoa.telefone_01
            pessoa_existente.telefone_02 = pessoa.telefone_02
            pessoa_existente.telefone_03 = pessoa.telefone_03
            pessoa_existente.rg = pessoa.rg
            pessoa_existente.data_nas = pessoa.data_nas
   
            
            # Salva as alterações
            session_db.commit()
            id = pessoa_existente.id  # Retorna o ID da pessoa existente
        else:
            # Se não existir, adiciona uma nova pessoa
            session_db.add(pessoa)
            session_db.commit()
            id = pessoa.id  # Retorna o ID da nova pessoa

    except Exception as e:
        session_db.rollback()  # Desfaz a sessão em caso de erro
        app.logger.info(f"Erro ao gravar pessoa: {e}")
        return False, None
    finally:
        session_db.close()

    return True, id

def gravar_paciente(paciente):
    session_db = Session()
    
    try:

        paciente_existente = session_db.query(Paciente).filter_by(fk_pessoa_id=paciente.fk_pessoa_id).first()

        if paciente_existente:

            paciente_existente.tipoconvenio=paciente.tipoconvenio
            paciente_existente.flgconvenio=paciente.flgconvenio
 
            session_db.commit()
            id = paciente_existente.id  # Retorna o ID da pessoa existente
        else:
         
            session_db.add(paciente)
            session_db.commit()
            id = paciente.id  

    except Exception as e:
        session_db.rollback()  # Desfaz a sessão em caso de erro
        app.logger.info(f"Erro ao gravar o paciente: {e}")
        return False, None
    finally:
        session_db.close()

    return True, id

def gravar_medico(medico):
    session_db = Session()
    
    try:

        medico_existente = session_db.query(Medico).filter_by(fk_pessoa_id=medico.fk_pessoa_id).first()

        if medico_existente:
            medico_existente.crm=medico.crm
            medico_existente.flgativo=medico.flgativo
            medico_existente.codespecialidade=medico.codespecialidade
            medico_existente.crm=medico.crm
            session_db.commit()
            id = medico_existente.codmedico  # Retorna o ID da pessoa existente
        else:
            session_db.add(medico)
            session_db.commit()
            id = medico.codmedico  

    except Exception as e:
        session_db.rollback()  # Desfaz a sessão em caso de erro
        app.logger.info(f"Erro ao gravar o medico: {e}")
        return False, None
    finally:
        session_db.close()

    return True, id

def pesquisar_dados_paciente(cpf):
    session_db=Session()
    
    pessoa=session_db.query(Pessoa).filter(Pessoa.cpf == cpf).one_or_none()
    if pessoa:
        paciente=session_db.query(Paciente).filter(Paciente.fk_pessoa_id == pessoa.id).one_or_none()
    else:
        return jsonify({"flgencontrou": False})

    if paciente:
        return jsonify({
            'flgencontrou':True,
            'nome': pessoa.nome,
            'rg': pessoa.rg,
            'data_nas': pessoa.data_nas.strftime('%Y-%m-%d'),  # Formata a data
            'cep': pessoa.cep,
            'uf': pessoa.uf,
            'cidade': pessoa.cidade,
            'endereco': pessoa.endereco,
            'complemento': pessoa.complemento,
            'numero': pessoa.numero,
            'telefone_01': pessoa.telefone_01,
            'telefone_02': pessoa.telefone_02,
            'telefone_03': pessoa.telefone_03,
            "flgconvenio":paciente.flgconvenio,
            "tipoconvenio":paciente.tipoconvenio,
            "fk_convenio_id":paciente.fk_convenio_id
        })
    elif pessoa:
        return jsonify({
           'flgencontrou':True,
           'nome': pessoa.nome,
            'rg': pessoa.rg,
            'data_nas': pessoa.data_nas.strftime('%Y-%m-%d'),  # Formata a data
            'cep': pessoa.cep,
            'uf': pessoa.uf,
            'cidade': pessoa.cidade,
            'endereco': pessoa.endereco,
            'complemento': pessoa.complemento,
            'numero': pessoa.numero,
            'telefone_01': pessoa.telefone_01,
            'telefone_02': pessoa.telefone_02,
            'telefone_03': pessoa.telefone_03,
            "flgconvenio":None,
            "tipoconvenio":None,
            "fk_convenio_id":None})

def pesquisar_dados_medico(cpf):
    session_db=Session()

    pessoa=session_db.query(Pessoa).filter(Pessoa.cpf == cpf).one_or_none()
    if pessoa:
        medico=session_db.query(Medico).filter(Medico.fk_pessoa_id == pessoa.id).one_or_none()
    else:
        return jsonify({"flgencontrou": False})
    if medico:
        app.logger.info(f" {medico.flgativo}")
        return jsonify({
            "flgencontrou": True,
            'codmedico':medico.codmedico,
            'nome': pessoa.nome,
            'rg': pessoa.rg,
            'data_nas': pessoa.data_nas.strftime('%Y-%m-%d'),  # Formata a data
            'cep': pessoa.cep,
            'uf': pessoa.uf,
            'cidade': pessoa.cidade,
            'endereco': pessoa.endereco,
            'complemento': pessoa.complemento,
            'numero': pessoa.numero,
            'telefone_01': pessoa.telefone_01,
            'telefone_02': pessoa.telefone_02,
            'telefone_03': pessoa.telefone_03,
            "crm":medico.crm,
            "flgativo":medico.flgativo,
            "codespecialidade":medico.codespecialidade
        })
    elif pessoa:
        return jsonify({
           "flgencontrou": True,
           'nome': pessoa.nome,
            'rg': pessoa.rg,
            'data_nas': pessoa.data_nas.strftime('%Y-%m-%d'),  # Formata a data
            'cep': pessoa.cep,
            'uf': pessoa.uf,
            'cidade': pessoa.cidade,
            'endereco': pessoa.endereco,
            'complemento': pessoa.complemento,
            'numero': pessoa.numero,
            'telefone_01': pessoa.telefone_01,
            'telefone_02': pessoa.telefone_02,
            'telefone_03': pessoa.telefone_03,
            "crm":None,
            "flgativo":None,
            "codespecialidade":None})    

def pesquisar_dados_medico_escala(cpf):
    session_db=Session()

    pessoa=session_db.query(Pessoa).filter(Pessoa.cpf == cpf).one_or_none()
    if pessoa:
        medico=session_db.query(Medico).filter(Medico.fk_pessoa_id == pessoa.id).one_or_none()
  
    else:

        return jsonify({"flgencontrou": False})
    if medico:
       
        especialidade=session_db.query(Especialidade).filter(Especialidade.codespecialidade == medico.codespecialidade).one_or_none()
     
        return jsonify({
            'flgencontrou': True,
            'codmedico':medico.codmedico,
            'nome': pessoa.nome,
            'crm':medico.crm,
            'flgativo':medico.flgativo,
            'codespecialidade':medico.codespecialidade,
            'especialidade':especialidade.descricao
        })
    else:
    
        return jsonify({"flgencontrou": False})


@app.route("/",methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/cadastro_pacientes',methods=['GET'])
def cadastro_paciente():
    
    convenios=lista_convenios()

    return render_template('cadastropaciente.html',lista_convenios=convenios)

@app.route('/cadastro_convenio',methods=['GET'])
def cadastro_convenio():
    return render_template('cadastroconvenio.html')

@app.route('/cadastro_medico',methods=['GET'])
def cadastro_medico():
    session_db = Session()
 
    especialidades =  session_db.query(Especialidade).all()
    return render_template('cadastromedicos.html', especialidades=especialidades)


@app.route('/cadastro_escala',methods=['GET'])
def cadastro_escala():
    return render_template('cadastroescala.html')

@app.route('/cadastro_clinica',methods=['GET'])
def cadastro_clinica():
    return render_template('cadastroclinica.html')

@app.route('/abrir_agenda', methods=['GET'])
def abrir_agenda():
    return render_template('agenda.html')


@app.route('/salvar_medico', methods=['POST'])
def salvar_medico():
    
  
    nome = request.form.get('nome')
    cpf = request.form.get('cpf').replace('.', '').replace('-', '')
    rg = request.form.get('rg').replace('.', '').replace('-', '')
    data_nas = request.form.get('data_nas')
    cep = request.form.get('cep').replace('.', '').replace('-', '')
    endereco = request.form.get('endereco')
    uf = request.form.get('uf')
    cidade = request.form.get('cidade')
    complemento = request.form.get('complemento')
    numero = request.form.get('numero')
    telefone_01 = request.form.get('telefone_01')
    telefone_02 = request.form.get('telefone_02')
    telefone_03 = request.form.get('telefone_03')

   
    crm = request.form.get('crm')
    flgativo = request.form.get('flgativo')
    codespecialidade = request.form.get('especialidade')

 
    pessoa = Pessoa(
        nome=nome,
        cpf=cpf,
        rg=rg,
        data_nas=data_nas,
        cep=cep,
        endereco=endereco,
        uf=uf,
        cidade=cidade,
        complemento=complemento,
        numero=numero,
        telefone_01=telefone_01,
        telefone_02=telefone_02,
        telefone_03=telefone_03
      
    )
    valida,id= gravar_pessoa(pessoa)
    if  valida==False:
        return render_template("cadastromedicos.html", mensagem=f"Ocorreu uma falha no cadastro!")

    # Cria uma nova instância da classe Medico
    medico = Medico(
        crm=crm,
        fk_pessoa_id=id,
        flgativo=int(flgativo)
        ,codespecialidade=codespecialidade
    )

    valida,id=gravar_medico(medico)
    
    if valida==False:
        return render_template("cadastromedicos.html", mensagem=f"Ocorreu uma falha no cadastro do medico!")
    
    return render_template("cadastromedicos.html", mensagem=f"Dados gravados com sucesso!")
    

@app.route('/salvar_paciente', methods=['POST'])
def salvar_paciente():
   
    nome = request.form['Nome']
    rg = request.form['RG'].replace('.', '').replace('-', '')
    cpf = request.form['CPF'].replace('.', '').replace('-', '')
    data_nas = request.form['Data_Nascimento']
    endereco = request.form['Endereco']
    numero = request.form.get('numero', '')
    complemento = request.form.get('Complemento', '')
    cidade = request.form['Cidade']
    uf = request.form['UF']
    cep = request.form['CEP'].replace('.', '').replace('-', '')
    telefone_01 = request.form['Telefone_01']
    telefone_02 = request.form.get('Telefone_02', None)
    telefone_03 = request.form.get('Telefone_03', None)

    # Verifica se o paciente possui convênio
    possui_convenio = request.form.get('possui_convenio')
    flgconvenio = True if possui_convenio == 'sim' else False

    # Se possuir convênio, captura o tipo e o convênio selecionado
    if flgconvenio:
        tipoconvenio = request.form['tipoconvenio']
        convenio_id = request.form['convenio']
    else:
        tipoconvenio = None
        convenio_id = None

    pessoa = Pessoa(
        nome=nome,
        cpf=cpf,
        rg=rg,
        data_nas=data_nas,
        cep=cep,
        endereco=endereco,
        uf=uf,
        cidade=cidade,
        complemento=complemento,
        numero=numero,
        telefone_01=telefone_01,
        telefone_02=telefone_02,
        telefone_03=telefone_03
       
    )

    valida,id=gravar_pessoa(pessoa)
    if valida==False:
        return render_template("cadastropaciente.html", mensagem=f"Ocorreu uma falha no cadastro!")
  
    paciente = Paciente(
        fk_pessoa_id=id,
        tipoconvenio=tipoconvenio,
        fk_convenio_id=convenio_id,
        flgconvenio=flgconvenio
       
    )

    valida,id=gravar_paciente(paciente)
 
    if valida==False:
        return render_template("cadastropaciente.html", mensagem=f"Ocorreu uma falha no cadastro!")
  
   
    
    return render_template("cadastropaciente.html", mensagem=f"Dados gravados com sucesso!")
   

   
    
@app.route('/pesquisar_paciente/<cpf>', methods=['GET'])
def pesquisar_paciente(cpf):
    return pesquisar_dados_paciente(cpf)

@app.route('/pesquisar_medico_cadescala/<cpf>',methods=['GET'])
def pesquisar_medico_cadescala(cpf):
    return pesquisar_dados_medico_escala(cpf)

@app.route('/pesquisar_medico/<cpf>', methods=['GET'])
def pesquisar_medico(cpf):
    return pesquisar_dados_medico(cpf)
    
 


@app.route('/buscar_pessoa/<cpf>', methods=['GET'])
def buscar_pessoa(cpf):
    session_db = Session()
    
    try:
        pessoa = session_db.query(Pessoa).filter_by(cpf=cpf).first()
        if pessoa:
            # Retorna os dados da pessoa como um dicionário
            return jsonify({
                'nome': pessoa.nome,
                'rg': pessoa.rg,
                'data_nas': pessoa.data_nas.strftime('%Y-%m-%d'),  # Formata a data
                'cep': pessoa.cep,
                'uf': pessoa.uf,
                'cidade': pessoa.cidade,
                'endereco': pessoa.endereco,
                'complemento': pessoa.complemento,
                'numero': pessoa.numero,
                'telefone_01': pessoa.telefone_01,
                'telefone_02': pessoa.telefone_02,
                'telefone_03': pessoa.telefone_03
            })
        else:
            return jsonify(None), 404  # Retorna 404 se a pessoa não for encontrada
    except Exception as e:
           app.logger.info(f" {e}")
    finally:
        session_db.close()


@app.route('/buscar_escalas/<codmedico>',methods=['GET'])
def buscar_escalas(codmedico):
    session_db = Session()

    try:
        # Consulta para buscar todas as escalas do médico
        escalas = session_db.query(Escala).filter_by(codmedico=codmedico).all()
        
        if escalas:
            # Extrai apenas as datas das escalas e cria uma lista
            datas = [escala.data for escala in escalas]
            
            # Log para verificar as datas encontradas
            app.logger.info(f"Escalas encontradas: {datas}")
            
            # Retorna as datas das escalas em formato de lista
            return jsonify({
                'datas': datas
            })
        else:
            # Se nenhuma escala for encontrada, retorna 404
            return jsonify(None), 404
    except Exception as e:
        app.logger.error(f"Erro ao buscar escalas: {e}")
    finally:
        session_db.close()

@app.route('/buscar_vagas_por_data/<data>/<codmedico>', methods=['GET'])
def buscar_vagas_por_data(data, codmedico):
    session_db = Session()

    try:
        # Consulta para buscar a escala do médico para a data específica
        escala = session_db.query(Escala).filter_by(codmedico=codmedico, data=data).first()
        
        if escala:
            # Log para verificar as vagas encontradas
            app.logger.info(f"Vagas encontradas para {data}: Manhã: {escala.quantvagasmanha}, Tarde: {escala.quantvagastarde}, Noite: {escala.quantvagasnoite}")
            
            # Retorna as vagas para os diferentes turnos
            return jsonify({
                'vagasManha': escala.quantvagasmanha,
                'vagasTarde': escala.quantvagastarde,
                'vagasNoite': escala.quantvagasnoite
                
            })
        else:
            # Se nenhuma escala for encontrada, retorna 404
            return jsonify({'message': 'Escala não encontrada para essa data'})
    except Exception as e:
        app.logger.error(f"Erro ao buscar vagas: {e}")
        return jsonify({'message': 'Erro ao buscar vagas'}), 500
    finally:
        session_db.close()




@app.route('/salvar_convenio',methods=['POST'])
def salvar_convenio():
    session_db = Session()
    cnpj = request.form['cnpj']
    descricao=request.form['descricao']
    convenio=Convenio(cnpj=cnpj,descricao=descricao)
    try:
        session_db.add(convenio)
        session_db.commit()
       
    except:
        session_db.rollback()
    finally:
        session_db.close()

    # Redireciona para uma página de sucesso ou outra rota
   
    return render_template("cadastroconvenio.html", mensagem=f"Cadastro Realizado com sucesso!")
if __name__ == "__main__":
    app.run(debug=True)




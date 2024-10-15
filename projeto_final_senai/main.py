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



@app.route("/",methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/cadastro_pacientes',methods=['GET'])
def cadastro_paciente():
    
    convenios=lista_convenios()
    app.logger.info(f"iniciando{len(convenios)}")
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
    cpf = request.form.get('cpf')
    rg = request.form.get('rg')
    data_nas = request.form.get('data_nas')
    cep = request.form.get('cep')
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


    # Obtenha o ID da nova pessoa para o relacionamento com o médico
    

    # Cria uma nova instância da classe Medico
    medico = Medico(
        crm=crm,
        fk_pessoa_id=id,
        flgativo=int(flgativo)
        ,codespecialidade=codespecialidade
    )
    session_db = Session()
    # Adiciona o novo médico à sessão
    session_db.add(medico)

    # Tenta salvar as alterações no banco de dados
    try:
        session_db.add(medico)
        session_db.commit()
       
    except Exception as e:
        session_db.rollback()  # Desfaz a sessão em caso de erro
        app.logger.info(f" {e}")
        return render_template("cadastromedicos.html", mensagem=f"Ocorreu uma falha no cadastro2!")

    finally :
        session_db.close
    
    return render_template("cadastromedicos.html", mensagem=f"Dados gravados com sucesso!")
    

@app.route('/salvar_paciente', methods=['POST'])
def salvar_paciente():
   
    nome = request.form['Nome']
    rg = request.form['RG']
    cpf = request.form['CPF'].replace('.', '').replace('-', '')
    data_nas = request.form['Data_Nascimento']
    endereco = request.form['Endereco']
    numero = request.form.get('numero', '')
    complemento = request.form.get('Complemento', '')
    cidade = request.form['Cidade']
    uf = request.form['UF']
    cep = request.form['CEP']
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
    session_db=Session()
  
    try:
        session_db.add(paciente)
        session_db.commit()
       
    except Exception as e:
        session_db.rollback()  # Desfaz a sessão em caso de erro
        app.logger.info(f" {e}")
        return render_template("cadastropaciente.html", mensagem=f"Ocorreu uma falha no cadastro!")

    finally :
        session_db.close
    
    return render_template("cadastropaciente.html", mensagem=f"Dados gravados com sucesso!")
   

   
    
@app.route('/pesquisar_paciente', methods=['GET'])
def pesquisar_paciente():
    session_db = Session()
    cpf = request.args.get('cpf')
    paciente =  session_db.query(Pessoa).filter(Pessoa.cpf == cpf).one_or_none()
  
    if paciente:
        return jsonify({
           "nome": paciente.nome,
            "cpf": paciente.cpf,
            "data_nas":paciente.data_nas,
            "telefone_01":paciente.telefone_01,
            "telefone_02":paciente.telefone_02,
            "telefone_03":paciente.telefone_03
        })
    return jsonify({"error": "Paciente não encontrado."}), 404

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




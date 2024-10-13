# pip install flask (no terminal)
# importando modulos
from flask import Flask,render_template,request,redirect,url_for
import urllib.parse
# realizar o mapeamento objeto relacional -DB First
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
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
Convenio= Base.classes.convenio


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

@app.route("/",methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/cadastro_pacientes',methods=['GET'])
def cadastro_paciente():
    
    convenios=lista_convenios()
    app.logger.info(f'abrindo cadastro{len(convenios)}')
    return render_template('cadastropaciente.html',lista_convenios=convenios,quantidade=convenios)

@app.route('/cadastro_convenio',methods=['GET'])
def cadastro_convenio():
    return render_template('cadastroconvenio.html')

@app.route('/salvar_paciente', methods=['POST'])
def salvar_paciente():
    session_db = Session()
    # Recebe os dados enviados pelo formulário HTML
    
    nome = request.form['Nome']
    rg = request.form['RG']
    cpf = request.form['CPF']
    endereco = request.form['Endereco']
    numero = request.form.get('numero', '')
    complemento = request.form.get('Complemento', '')
    cidade = request.form['Cidade']
    uf = request.form['UF']
    cep = request.form['CEP']
    telefone_01 = request.form['Telefone_01']
    telefone_02 = request.form.get('Telefone_02', None)
    telefone_03 = request.form.get('Telefone_03', None)
   
    # Cria um objeto Pessoa com os dados recebidos
    pessoa = Pessoa(nome=nome, rg=rg, cpf=cpf, endereco=endereco, numero=numero, complemento=complemento, cidade=cidade, uf=uf, cep=cep, telefone_01=telefone_01, telefone_02=telefone_02, telefone_03=telefone_03)

    
   

    try:
        session_db.add(pessoa)
        session_db.commit()
        codigo_paciente = pessoa.id  # Captura o código do paciente gerado
    except:
        session_db.rollback()
    finally:
        session_db.close()

    # Redireciona para uma página de sucesso ou outra rota
   
    return render_template("cadastropaciente.html", mensagem=f"Cadastro Realizado com sucesso:{codigo_paciente}")

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




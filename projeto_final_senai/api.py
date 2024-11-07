# importando as bibliotecas e modulos
from fastapi import FastAPI, HTTPException, status, Depends
# biblioteca de token de segurança
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score





modelo_cancer=None
modelo_infarto=None
app= FastAPI()

auth2_scheme=OAuth2PasswordBearer(tokenUrl='token')


async def carrega_modelo_cancer():
    try:
        print (50*"#","carregando dataset cancer")
        df = pd.read_csv('dataset/cancer_mama.csv')
        print(df.head())
        print(df.info())
        df = df.drop(columns = "id")
        df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
        corr=df.corr()
        print(corr['diagnosis'])
        classe = df['diagnosis']
        df = df.drop(columns = 'diagnosis')
        df=df.drop(columns='Unnamed: 32')
        x_test, x_train, y_test, y_train = train_test_split(df, classe, test_size=0.3, random_state=42)
        modelo=LogisticRegression(max_iter=3200)
        modelo.fit(x_train, y_train)
        acuracia_treino=modelo.score(x_train, y_train)
        print(f"Acurácia de treino modelo de cancer: {(acuracia_treino*100):.2f}%")
        y_pred =  modelo.predict(x_test)


        acuracia_teste = accuracy_score(y_test, y_pred)
        print(f"Acurácia de teste do modelo de: {(acuracia_teste*100):.2f}%")

    except FileNotFoundError:
        print("Erro: O arquivo de dataset de cancer não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o dataset de cancer: {e}")
        return None
    return modelo

async def carrega_modelo_infarto():
    try:
        print (50*"#","carregando dataset infarto")
        df = pd.read_csv('dataset/heart.csv')
        print(df.head())
        print(df.info())
        corr=df.corr()
        print(corr['output'])


        classe = df['output']
        df.drop('output',axis=1,inplace=True)
        X_train,X_test,Y_train,Y_test=train_test_split(df,classe,test_size=0.3,random_state=42)
        modelo=LogisticRegression(max_iter=3200)
        modelo.fit(X_train, Y_train)
        acuracia_treino=modelo.score(X_train, Y_train)
        print(f"Acurácia de treino modelo de infarto: {(acuracia_treino*100):.2f}%")


        y_pred =  modelo.predict(X_test)
        acuracia_teste = accuracy_score(Y_test, y_pred)
        print(f"Acurácia de teste do modelo de infarto: {(acuracia_teste*100):.2f}%")

    except FileNotFoundError:
        print("Erro: O arquivo de dataset de infarto não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o dataset de infarto: {e}")
        return None
    return modelo
# rodar api: uvicorn api:app --reload 
@app.on_event("startup")
async def load_dataset():
  modelo_cancer= await carrega_modelo_cancer()
  modelo_infarto=await carrega_modelo_infarto()


@app.get('/')
async def index():
    return {"mensagem": "API está funcionando e os datasets foram carregadod!"}

@app.get('/prever/{json}')
async def prever():
    # Exemplo de uso do dataset
    #return {"exemplo": df.head(5).to_dict()}  # Retorna as 5 primeiras linhas do dataset como exemplo
    pass



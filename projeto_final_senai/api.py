# importando as bibliotecas e modulos
from fastapi import FastAPI, HTTPException, status, Depends
# biblioteca de token de segurança
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from pydantic import BaseModel
import numpy as np

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
  global modelo_cancer
  modelo_cancer= await carrega_modelo_cancer()
  modelo_infarto=await carrega_modelo_infarto()


@app.get('/')
async def index():
    return {"mensagem": "API está funcionando e os datasets foram carregadod!"}

@app.post('/prever_cancer/')
async def prever(features: CancerFeatures):
    print('testandoooo')
    colunas_treinamento = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se',
    'concave points_se', 'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst',
    'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst', 'symmetry_worst',
    'fractal_dimension_worst'
]

# Criando um DataFrame com as características do usuário
    dados = pd.DataFrame([[
    features.radius_mean,
    features.texture_mean,
    features.perimeter_mean,
    features.area_mean,
    features.smoothness_mean,
    features.compactness_mean,
    features.concavity_mean,
    features.concave_points_mean,  # Certificando-se que o nome da coluna está correto
    features.symmetry_mean,
    features.fractal_dimension_mean,
    features.radius_se,
    features.texture_se,
    features.perimeter_se,
    features.area_se,
    features.smoothness_se,
    features.compactness_se,
    features.concavity_se,
    features.concave_points_se,  # Certificando-se que o nome da coluna está correto
    features.symmetry_se,
    features.fractal_dimension_se,
    features.radius_worst,
    features.texture_worst,
    features.perimeter_worst,
    features.area_worst,
    features.smoothness_worst,
    features.compactness_worst,
    features.concavity_worst,
    features.concave_points_worst,  # Certificando-se que o nome da coluna está correto
    features.symmetry_worst,
    features.fractal_dimension_worst
]], columns=colunas_treinamento)

    # Realiza a previsão usando o modelo
    try:
        resposta = modelo_cancer.predict(dados)  # modelo_cancer deve estar carregado anteriormente
        print(f'respostaaaa: {resposta}')
        return {"previsao": int(resposta)}
    except Exception as e:
        print(f'errooooooooooooooooooooo {e}')
        raise HTTPException(status_code=500, detail=f"Erro na previsão: {e}")



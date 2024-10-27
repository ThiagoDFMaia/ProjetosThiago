# importando as bibliotecas e modulos
from fastapi import FastAPI, HTTPException, status, Depends
# biblioteca de token de segurança
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


app= FastAPI()

auth2_scheme=OAuth2PasswordBearer(tokenUrl='token')

# rodar api: uvicorn api:app --reload 
@app.on_event("startup")
async def load_dataset():
    global df  # Define o dataframe como variável global para acessar nos endpoints
    try:
        df = pd.read_csv('dataset/cancer_mama.csv')
        print(df.head())
        df = df.drop(columns = "id")
        df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
        classe = df['diagnosis']
        df = df.drop(columns = 'diagnosis')
        df=df.drop(columns='Unnamed: 32')
        x_test, x_train, y_test, y_train = train_test_split(df, classe, test_size=0.2, random_state=42)
        
        modelo=LogisticRegression(max_iter=3200)
        modelo.fit(x_train, y_train)
        acuracia_treino=modelo.score(x_train, y_train)
        print(f"Acurácia no treino: {(acuracia_treino*100):.2f}%")

    except FileNotFoundError:
        print("Erro: O arquivo de dataset não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o dataset: {e}")

@app.get('/')
async def index():
    return {"mensagem": "API está funcionando e o dataset foi carregado!"}

@app.get('/prever/{json}')
async def prever():
    # Exemplo de uso do dataset
    return {"exemplo": df.head(5).to_dict()}  # Retorna as 5 primeiras linhas do dataset como exemplo




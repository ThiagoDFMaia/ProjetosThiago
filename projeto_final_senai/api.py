# importando as bibliotecas e modulos
from fastapi import FastAPI, HTTPException, status, Depends
# biblioteca de token de segurança
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

from sklearn.preprocessing import StandardScaler

import numpy as np
from biblioteca import *
import pickle




modelo_cancer=None
modelo_infarto=None
app= FastAPI()

auth2_scheme=OAuth2PasswordBearer(tokenUrl='token')

# rodar api: uvicorn api:app --reload 
import os
async def carrega_modelo_cancer():
    print("carregando modelo cancer")
    if os.path.exists("modelocancer.pkl"):
        print(f"Tamanho do arquivo: {os.path.getsize('modelocancer.pkl')} bytes")
    if os.path.getsize("modelocancer.pkl") == 0:
        print("Erro: O arquivo está vazio!")
    

    with open('modelocancer.pkl', 'rb') as arquivo:
        return pickle.load(arquivo)

async def carrega_modelo_infarto():
    print("carregando modelo infarto")
    if os.path.exists("modeloinfarto.pkl"):
        print(f"Tamanho do arquivo: {os.path.getsize('modeloinfarto.pkl')} bytes")
    if os.path.getsize("modeloinfarto.pkl") == 0:
        print("Erro: O arquivo está vazio!")
    

    with open('modeloinfarto.pkl', 'rb') as arquivo:
        return pickle.load(arquivo)


@app.on_event("startup")
async def load_dataset():
  global modelo_cancer
  global modelo_infarto
  modelo_cancer= await carrega_modelo_cancer()
  modelo_infarto=await carrega_modelo_infarto()


@app.get('/')
async def index():
    return {"mensagem": "API está funcionando e os datasets foram carregadod!"}

class EntradaModeloCancer(BaseModel):
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

@app.post('/prever_cancer/')
async def prever_cancer(dados: EntradaModeloCancer):
    print('prevendo')
    try:
        # Converter os dados em um array numpy
        entrada = np.array([[
            dados.radius_mean,
            dados.texture_mean,
            dados.perimeter_mean,
            dados.area_mean,
            dados.smoothness_mean,
            dados.compactness_mean,
            dados.concavity_mean,
            dados.concave_points_mean,
            dados.symmetry_mean,
            dados.fractal_dimension_mean,
            dados.radius_se,
            dados.texture_se,
            dados.perimeter_se,
            dados.area_se,
            dados.smoothness_se,
            dados.compactness_se,
            dados.concavity_se,
            dados.concave_points_se,
            dados.symmetry_se,
            dados.fractal_dimension_se,
            dados.radius_worst,
            dados.texture_worst,
            dados.perimeter_worst,
            dados.area_worst,
            dados.smoothness_worst,
            dados.compactness_worst,
            dados.concavity_worst,
            dados.concave_points_worst,
            dados.symmetry_worst,
            dados.fractal_dimension_worst
        ]])  # Envolvendo em uma lista para o modelo aceitar como input
        # Fazer a previsão
    


        
        previsao = modelo_cancer.predict(entrada)
       
        probabilidades = modelo_cancer.predict_proba(entrada)
        classe_predita = previsao[0]  # Pega a classe predita
        confianca = probabilidades[0][classe_predita]  # Pega a probabilidade da classe predita
        print(f'Resposta: {previsao[0]} confiança: {confianca:.2f}%')
        return {"previsao": int(previsao[0]),"confianca":confianca}
    except Exception as e:
        print(f'erro: {e}')
        
'''
const data = {
        age: age,
        sex: sex,
        cp: cp,
        trtbps: trtbps,
        chol: chol,
        fbs: fbs,
        restecg: restecg,
        thalachh: thalachh,
        exng: exng,
        oldpeak: oldpeak,
        slp: slp,
        caa: caa,
        thall: thall
    };
'''

class EntradaModeloInfarto(BaseModel):
        age: int
        sex: int
        cp: int
        trtbps: int
        chol: int
        fbs: int
        restecg: int
        thalachh: int
        exng: int
        oldpeak: float
        slp: int
        caa: int
        thall: int
@app.post('/prever_infarto/')
async def prever_infarto(dados: EntradaModeloInfarto):
    
    print('prevendo')
    try:
        # Converter os dados em um array numpy
        entrada = np.array([[
           dados.age,
           dados.sex,
           dados.cp,
           dados.trtbps,
           dados.chol,
           dados.fbs,
           dados.restecg,
           dados.thalachh,
           dados.exng,
           dados.oldpeak,
           dados.slp,
           dados.caa,
           dados.thall
        ]])  # Envolvendo em uma lista para o modelo aceitar como input
        # Fazer a previsão
    


        
        previsao = modelo_infarto.predict(entrada)
       
        probabilidades = modelo_infarto.predict_proba(entrada)
        classe_predita = previsao[0]  # Pega a classe predita
        confianca = probabilidades[0][classe_predita]  # Pega a probabilidade da classe predita
        print(f'Resposta: {previsao[0]} confiança: {confianca:.2f}%')
        return {"previsao": int(previsao[0]),"confianca":confianca}
    except Exception as e:
        print(f'erro: {e}')



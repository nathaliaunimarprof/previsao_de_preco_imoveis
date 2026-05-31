"""
Módulo de Machine Learning: treino do modelo e geração de previsões.

Encapsula toda a lógica de modelagem para que a UI não precise conhecer
detalhes do scikit-learn. Para trocar o algoritmo (ex.: RandomForest),
basta alterar este arquivo.
"""

from dataclasses import dataclass
from typing import Tuple

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from src.data_loader import FEATURE_COLUMNS

# Semente fixa para garantir reprodutibilidade dos splits/treinos.
RANDOM_STATE = 42
TEST_SIZE = 0.2


@dataclass
class TrainedModel:
    """
    Container leve com o modelo treinado e suas métricas de avaliação.

    Usar uma dataclass evita ter que retornar múltiplos valores soltos e
    deixa claro o "contrato" do que o treinamento devolve.
    """
    estimator: LinearRegression
    r2: float           # Coeficiente de determinação no conjunto de teste.
    mae: float          # Erro absoluto médio no conjunto de teste.
    n_train: int        # Tamanho do conjunto de treino.
    n_test: int         # Tamanho do conjunto de teste.


def train_model(X: pd.DataFrame, y: pd.Series) -> TrainedModel:
    """
    Treina um modelo de Regressão Linear e calcula métricas no conjunto de teste.

    O split treino/teste acontece aqui dentro para manter a interface simples:
    quem chama só precisa fornecer X e y completos.

    Parâmetros
    ----------
    X : pd.DataFrame
        Features de entrada.
    y : pd.Series
        Vetor alvo.

    Retorno
    -------
    TrainedModel
        Objeto contendo o modelo já ajustado e suas métricas.
    """
    # Divide os dados em treino e teste (80/20).
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    # Treina o estimador.
    estimator = LinearRegression()
    estimator.fit(X_train, y_train)

    # Avalia no conjunto de teste — métricas úteis para exibir no app.
    y_pred = estimator.predict(X_test)
    return TrainedModel(
        estimator=estimator,
        r2=r2_score(y_test, y_pred),
        mae=mean_absolute_error(y_test, y_pred),
        n_train=len(X_train),
        n_test=len(X_test),
    )


def predict_price(
    model: TrainedModel,
    distance_to_mrt: float,
    num_convenience_stores: int,
    latitude: float,
    longitude: float,
) -> float:
    """
    Gera a previsão de preço por unidade de área para um único imóvel.

    Parâmetros
    ----------
    model : TrainedModel
        Modelo previamente treinado.
    distance_to_mrt : float
        Distância (em metros) até a estação MRT mais próxima.
    num_convenience_stores : int
        Quantidade de lojas de conveniência nas redondezas.
    latitude, longitude : float
        Coordenadas geográficas do imóvel.

    Retorno
    -------
    float
        Preço estimado por unidade de área (mesma unidade do dataset).
    """
    # Monta um DataFrame de 1 linha respeitando a ordem/nomes das colunas
    # usadas no treino — isso elimina warnings do scikit-learn.
    features = pd.DataFrame(
        [[distance_to_mrt, num_convenience_stores, latitude, longitude]],
        columns=FEATURE_COLUMNS,
    )
    return float(model.estimator.predict(features)[0])

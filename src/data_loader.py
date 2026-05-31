"""
Módulo responsável pelo carregamento e pré-processamento do dataset.

Mantém isolada toda a lógica de I/O e seleção de colunas, de forma que
trocar a fonte de dados (ex.: banco de dados, API) afete apenas este arquivo.
"""

from pathlib import Path
from typing import Tuple

import pandas as pd

# --- Constantes do dataset ---------------------------------------------------
# Centralizar os nomes das colunas evita "strings mágicas" espalhadas pelo
# código e facilita a manutenção caso o schema mude no futuro.
FEATURE_COLUMNS = [
    "Distance to the nearest MRT station",
    "Number of convenience stores",
    "Latitude",
    "Longitude",
]
TARGET_COLUMN = "House price of unit area"

# Caminho padrão para o CSV — relativo à raiz do projeto.
DEFAULT_DATA_PATH = Path("data") / "real_estate.csv"


def load_dataset(file_path: Path | str = DEFAULT_DATA_PATH) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Carrega o dataset de imóveis e separa as variáveis preditoras (X) do alvo (y).

    Parâmetros
    ----------
    file_path : Path | str
        Caminho para o arquivo CSV contendo os dados. Default: ``data/real_estate.csv``.

    Retorno
    -------
    X : pd.DataFrame
        Matriz de features (distância MRT, lojas, latitude, longitude).
    y : pd.Series
        Vetor alvo (preço por unidade de área).

    Lança
    -----
    FileNotFoundError
        Caso o arquivo informado não exista no caminho fornecido.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(
            f"Arquivo de dados não encontrado: {file_path.resolve()}"
        )

    # Lê o CSV completo e seleciona apenas as colunas de interesse.
    df = pd.read_csv(file_path)
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    return X, y

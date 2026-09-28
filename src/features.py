"""Montagem da base de modelagem e das variáveis do modelo de risco.

Usado pelo notebook 03 (treino) e pelo app Streamlit (predição), para garantir
que as duas pontas calculem as variáveis exatamente da mesma forma.
"""
import pandas as pd

FEATURES = [
    "fase", "idade", "defasagem", "anos_programa",
    "iaa", "ieg", "ips", "ida", "ipv", "mat", "por",
    "gap_autoavaliacao",
]

COLUNAS_ENTRADA = [
    "ano", "ano_ingresso", "fase", "idade", "defasagem",
    "iaa", "ieg", "ips", "ida", "ipv", "mat", "por",
]


def preparar_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["anos_programa"] = out["ano"] - out["ano_ingresso"]
    # Quanto o aluno se avalia acima (+) ou abaixo (-) do desempenho acadêmico real
    out["gap_autoavaliacao"] = out["iaa"] - out["ida"]
    return out[FEATURES]


def montar_pares(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por aluno e ano t, com o alvo observado em t+1.

    risco = 1 quando a defasagem piora de t para t+1 E o aluno termina t+1 defasado
    (entrou em defasagem ou aprofundou a que já tinha).
    """
    alunos = df[~df["flag_universitario"]]
    seguinte = alunos[["ra", "ano", "defasagem"]].assign(ano=lambda d: d["ano"] - 1)
    pares = alunos.merge(seguinte, on=["ra", "ano"], suffixes=("", "_seguinte"))
    piorou = pares["defasagem_seguinte"] < pares["defasagem"]
    defasado = pares["defasagem_seguinte"] < 0
    pares["risco"] = (piorou & defasado).astype(int)
    return pares

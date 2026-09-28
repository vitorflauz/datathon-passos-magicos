"""Passos Mágicos: risco de defasagem no ano seguinte.

Executar localmente:  streamlit run app/app.py
"""
import json
import sys
from pathlib import Path

import altair as alt
import joblib
import pandas as pd
import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from src.features import COLUNAS_ENTRADA, preparar_features  # noqa: E402

st.set_page_config(page_title="Passos Mágicos · Risco de defasagem", page_icon=":material/query_stats:", layout="wide")

# Cores da FIAP, as mesmas da apresentação
ACENTO, CINZA = "#D30F59", "#91A3AD"


@st.cache_resource
def carregar_modelo():
    modelo = joblib.load(RAIZ / "modelos" / "modelo_risco.joblib")
    info = json.loads((RAIZ / "modelos" / "modelo_info.json").read_text(encoding="utf-8"))
    return modelo, info


@st.cache_data
def carregar_base():
    df = pd.read_csv(RAIZ / "dados" / "tratados" / "pede_long.csv")
    return df[~df["flag_universitario"]]


def pontuar(dados: pd.DataFrame) -> pd.DataFrame:
    saida = dados.copy()
    saida["probabilidade"] = modelo.predict_proba(preparar_features(saida))[:, 1]
    saida["classificacao"] = saida["probabilidade"].ge(LIMIAR).map({True: "Acompanhar", False: "Rotina"})
    return saida.sort_values("probabilidade", ascending=False)


@st.cache_data
def pontuar_ano(ano: int) -> pd.DataFrame:
    return pontuar(base[base["ano"] == ano])


def nome_fase(f: int) -> str:
    return "ALFA" if f == 0 else f"Fase {f}"


# Rótulos de exibição das tabelas; os CSVs baixados mantêm os nomes originais das colunas.
COLUNAS_TABELA = {
    "posicao": st.column_config.NumberColumn("Posição", help="Ordem de prioridade na lista filtrada."),
    "ra": st.column_config.TextColumn("RA"),
    "fase": st.column_config.NumberColumn("Fase", help="Nível do aluno no programa: 0 é a ALFA (alfabetização, 1º e 2º ano), 7 é o 3º ano do ensino médio."),
    "idade": st.column_config.NumberColumn("Idade"),
    "defasagem": st.column_config.NumberColumn("Defasagem", help="Fase atual menos a fase ideal para a idade. Negativo = atrasado; 0 ou mais = em fase."),
    "ida": st.column_config.NumberColumn("IDA", format="%.1f", help="Desempenho acadêmico: média das notas de Matemática, Português e Inglês, de 0 a 10."),
    "ieg": st.column_config.NumberColumn("IEG", format="%.1f", help="Engajamento: tarefas de casa, atividades acadêmicas e voluntariado, de 0 a 10."),
    "ips": st.column_config.NumberColumn("IPS", format="%.1f", help="Psicossocial: avaliação comportamental, emocional e social feita por psicólogos, de 0 a 10."),
    "ipv": st.column_config.NumberColumn("IPV", format="%.1f", help="Ponto de virada: evolução acadêmica, de engajamento e emocional ao longo do ano, de 0 a 10."),
    "probabilidade": st.column_config.ProgressColumn("Probabilidade", format="percent", min_value=0, max_value=1,
                                                     help="Pontuação de risco usada para ordenar a lista. Abaixo de 60% ela superestima o risco real."),
    "classificacao": st.column_config.TextColumn("Classificação"),
}

modelo, info = carregar_modelo()
LIMIAR = info["limiar"]
base = carregar_base()
ano_recente = int(base["ano"].max())
metricas = info["metricas_teste_2023_2024"]

st.title("Passos Mágicos · Risco de defasagem")
st.caption(
    "Estima a probabilidade de o aluno **entrar em defasagem ou aprofundar a defasagem no próximo ano**, "
    "a partir dos indicadores do PEDE do ano atual."
)

aba_lista, aba_aluno, aba_arquivo, aba_modelo = st.tabs([
    f":material/format_list_numbered: Lista de risco {ano_recente + 1}",
    ":material/person: Consultar aluno",
    ":material/upload_file: Pontuar arquivo",
    ":material/info: Sobre o modelo",
])

# --------------------------------------------------------------------------- aluno individual
with aba_aluno:
    entrada, resultado = st.columns([3, 2], gap="large")
    with entrada:
        with st.container(border=True):
            st.markdown("**Perfil do aluno**")
            p1, p2 = st.columns(2)
            fase = p1.selectbox("Fase", options=list(range(8)), format_func=nome_fase, index=2,
                                help="ALFA é a alfabetização (1º e 2º ano); as fases 1 a 7 vão do 3º ano do fundamental ao 3º do médio.")
            idade = p2.number_input("Idade", min_value=6, max_value=25, value=11)
            defasagem = p1.number_input(
                "Defasagem (fase atual − fase ideal)", min_value=-5, max_value=3, value=0,
                help="Negativo = atrasado; 0 = em fase; positivo = adiantado.",
            )
            ano_ingresso = p2.number_input("Ano de ingresso na Passos Mágicos", min_value=2010, max_value=ano_recente, value=ano_recente - 1)
        with st.container(border=True):
            st.markdown("**Indicadores do PEDE no ano atual**")
            i1, i2 = st.columns(2)
            ida = i1.slider("IDA · Desempenho acadêmico", 0.0, 10.0, 6.5, 0.1)
            mat = i1.slider("Nota de Matemática", 0.0, 10.0, 6.3, 0.1)
            por = i1.slider("Nota de Português", 0.0, 10.0, 6.8, 0.1)
            ieg = i1.slider("IEG · Engajamento", 0.0, 10.0, 8.5, 0.1)
            iaa = i2.slider("IAA · Autoavaliação", 0.0, 10.0, 8.0, 0.1)
            ips = i2.slider("IPS · Psicossocial", 0.0, 10.0, 6.5, 0.1)
            ipv = i2.slider("IPV · Ponto de virada", 0.0, 10.0, 7.5, 0.1)

    aluno = pd.DataFrame([{
        "ano": ano_recente, "ano_ingresso": ano_ingresso, "fase": fase, "idade": idade, "defasagem": defasagem,
        "iaa": iaa, "ieg": ieg, "ips": ips, "ida": ida, "ipv": ipv, "mat": mat, "por": por,
    }])
    prob = float(modelo.predict_proba(preparar_features(aluno))[:, 1][0])

    with resultado:
        st.metric(
            "Probabilidade de risco no próximo ano", f"{prob:.0%}",
            delta=f"{(prob - LIMIAR) * 100:+.0f} p.p. em relação ao limiar", delta_color="inverse", border=True,
        )
        if prob >= LIMIAR:
            st.error(f"**Acompanhar.** Acima do limiar de {LIMIAR:.0%}.", icon=":material/priority_high:")
        else:
            st.success(f"**Acompanhamento de rotina.** Abaixo do limiar de {LIMIAR:.0%}.", icon=":material/check_circle:")

        mesma_fase = base[(base["ano"] == ano_recente) & (base["fase"] == fase)]
        comparacao = pd.DataFrame({
            "Aluno": [ida, ieg, iaa, ips, ipv, mat, por],
            f"Mediana da fase ({ano_recente})": mesma_fase[["ida", "ieg", "iaa", "ips", "ipv", "mat", "por"]].median().values,
        }, index=["IDA", "IEG", "IAA", "IPS", "IPV", "Matemática", "Português"]).round(1)
        comparacao["Diferença"] = (comparacao["Aluno"] - comparacao.iloc[:, 1]).round(1)
        st.markdown(f"**Comparação com alunos da {nome_fase(fase)}**")
        st.dataframe(
            comparacao, width="stretch",
            column_config={c: st.column_config.NumberColumn(format="%.1f") for c in comparacao.columns}
            | {"Diferença": st.column_config.NumberColumn(format="%+.1f")},
        )
        st.caption(
            "A probabilidade é uma estimativa para priorizar o acompanhamento, não um diagnóstico. "
            "Idade e defasagem atual são os fatores de maior peso: alunos em fase nas transições da ALFA e da fase 5 "
            "concentram o risco de retenção."
        )

# --------------------------------------------------------------------------- lista do ano mais recente
with aba_lista:
    atual = pontuar_ano(ano_recente)
    n_acompanhar = int((atual["classificacao"] == "Acompanhar").sum())

    k1, k2, k3 = st.columns(3)
    k1.metric(f"Alunos avaliados ({ano_recente})", f"{len(atual)}", border=True)
    k2.metric(f"Sinalizados para acompanhamento ({n_acompanhar / len(atual):.0%} da base)", f"{n_acompanhar}", border=True)
    k3.metric("Limiar de decisão", f"{LIMIAR:.0%}", border=True)

    st.caption(
        f"Os alunos de {ano_recente} estão ordenados pela probabilidade de risco em {ano_recente + 1}. "
        "Informe quantos a equipe consegue acompanhar: a lista mostra os primeiros, em ordem de prioridade."
    )

    f1, f2, f3 = st.columns([5, 2, 1.4], vertical_alignment="bottom", gap="medium")
    fases = f1.pills("Filtrar fases", options=list(range(8)), default=list(range(8)),
                     format_func=nome_fase, selection_mode="multi")
    capacidade = f2.number_input("Capacidade da equipe (alunos)", min_value=1, max_value=len(atual),
                                 value=n_acompanhar, step=10)
    so_acompanhar = f3.toggle("Só sinalizados", value=True)
    filtro = atual[atual["fase"].isin(fases)]
    if so_acompanhar:
        filtro = filtro[filtro["classificacao"] == "Acompanhar"]
    total_filtro = len(filtro)
    filtro = filtro.head(capacidade).copy()
    filtro.insert(0, "posicao", range(1, len(filtro) + 1))

    grafico, tabela = st.columns([1, 2], gap="large")
    with grafico:
        st.markdown("**Sinalizados por fase**")
        por_fase = (atual.groupby("fase")["classificacao"].apply(lambda s: (s == "Acompanhar").sum())
                    .rename("Sinalizados").reset_index())
        por_fase["Fase"] = por_fase["fase"].map(nome_fase)
        por_fase["destaque"] = por_fase["Sinalizados"] == por_fase["Sinalizados"].max()
        st.altair_chart(
            alt.Chart(por_fase).mark_bar().encode(
                x=alt.X("Sinalizados:Q", title=None),
                y=alt.Y("Fase:N", sort=list(por_fase["Fase"]), title=None),
                color=alt.condition("datum.destaque", alt.value(ACENTO), alt.value(CINZA)),
                tooltip=["Fase", "Sinalizados"],
            ).properties(height=320),
            width="stretch",
        )
    with tabela:
        colunas = ["posicao", "ra", "fase", "idade", "defasagem", "ida", "ieg", "ips", "ipv", "probabilidade", "classificacao"]
        st.markdown(f"**{len(filtro)} alunos na lista**" + (f" · primeiros de {total_filtro}" if len(filtro) < total_filtro else ""))
        st.dataframe(filtro[colunas], width="stretch", height=320, hide_index=True, column_config=COLUNAS_TABELA)
        st.download_button("Baixar lista (CSV)", filtro[colunas].to_csv(index=False).encode("utf-8"),
                           file_name=f"risco_defasagem_{ano_recente + 1}.csv", mime="text/csv",
                           type="primary", icon=":material/download:")

# --------------------------------------------------------------------------- arquivo
with aba_arquivo:
    preparar, enviar = st.columns(2, gap="large")
    with preparar:
        with st.container(border=True):
            st.markdown("**Preparar o arquivo**")
            st.markdown(
                "Uma linha por aluno, com os dados do ano atual e as colunas abaixo. "
                "Colunas extras, como `ra` ou `nome`, são mantidas no resultado."
            )
            st.code(", ".join(COLUNAS_ENTRADA), language=None, wrap_lines=True)
            modelo_csv = base[base["ano"] == ano_recente][["ra"] + COLUNAS_ENTRADA].head(5)
            st.download_button("Baixar modelo de arquivo", modelo_csv.to_csv(index=False).encode("utf-8"),
                               file_name="modelo_entrada.csv", mime="text/csv", icon=":material/description:")
    with enviar:
        with st.container(border=True):
            st.markdown("**Enviar e pontuar**")
            arquivo = st.file_uploader("Arquivo CSV", type="csv")

    if arquivo is not None:
        entrada_csv = pd.read_csv(arquivo)
        faltando = [c for c in COLUNAS_ENTRADA if c not in entrada_csv.columns]
        if faltando:
            st.error(f"Colunas ausentes no arquivo: {', '.join(faltando)}", icon=":material/error:")
        else:
            pontuado = pontuar(entrada_csv)
            st.success(f"{len(pontuado)} alunos pontuados, {int((pontuado['classificacao'] == 'Acompanhar').sum())} sinalizados.",
                       icon=":material/check_circle:")
            st.dataframe(pontuado, width="stretch", hide_index=True, column_config=COLUNAS_TABELA)
            st.download_button("Baixar resultado (CSV)", pontuado.to_csv(index=False).encode("utf-8"),
                               file_name="resultado_risco.csv", mime="text/csv", type="primary", icon=":material/download:")

# --------------------------------------------------------------------------- sobre o modelo
with aba_modelo:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Casos de risco identificados (recall)", f"{metricas['recall']:.0%}", border=True)
    m2.metric("Acerto entre sinalizados (precisão)", f"{metricas['precisao']:.0%}", border=True)
    m3.metric("Acerto na ordenação (AUC)", f"{metricas['roc_auc']:.0%}", border=True,
              help="Em quantas de cada 100 comparações entre um aluno que entrou em risco e um que não entrou "
                   "o modelo deu pontuação maior ao primeiro. Um sorteio acertaria 50%.")
    m4.metric("Alunos sinalizados no teste", f"{metricas['pct_sinalizados']:.0%}", border=True)
    st.caption(f"Taxa de risco na base de teste: {metricas['taxa_base']:.0%}. Um sorteio aleatório teria precisão igual a essa taxa.")

    como, importancia_col = st.columns(2, gap="large")
    with como:
        st.subheader("Como o modelo funciona")
        st.markdown(
            f"""
- **O que prevê:** se o aluno vai **entrar em defasagem ou aprofundar a defasagem** no ano seguinte.
  Defasagem é a fase atual menos a fase ideal para a idade; valores negativos indicam atraso.
- **Dados de treino:** {info['treinado_com']}.
- **Modelo:** {info['modelo']}.
- **Validação:** temporal. Treinado com a transição 2022 → 2023 e testado em 2023 → 2024, um ano que o modelo não viu.
- **Limiar:** {LIMIAR:.0%}, escolhido para identificar pelo menos 75% dos alunos que entram em risco.
"""
        )
    with importancia_col:
        st.subheader("Importância das variáveis")
        st.caption("Quanto o acerto na ordenação cai, em pontos, ao embaralhar cada variável.")
        nomes = {"idade": "Idade", "defasagem": "Defasagem atual", "ipv": "IPV", "anos_programa": "Anos no programa",
                 "ida": "IDA", "por": "Português", "gap_autoavaliacao": "Gap autoavaliação (IAA − IDA)", "mat": "Matemática",
                 "fase": "Fase", "ieg": "IEG", "iaa": "IAA", "ips": "IPS"}
        importancia = (pd.Series(info["importancia_permutacao"]).rename(index=nomes)
                       .mul(100).rename_axis("Variável").reset_index(name="Importância"))
        importancia["destaque"] = importancia["Importância"].rank(ascending=False) <= 2
        st.altair_chart(
            alt.Chart(importancia).mark_bar().encode(
                x=alt.X("Importância:Q", title=None),
                y=alt.Y("Variável:N", sort="-x", title=None, axis=alt.Axis(labelLimit=260)),
                color=alt.condition("datum.destaque", alt.value(ACENTO), alt.value(CINZA)),
                tooltip=["Variável", alt.Tooltip("Importância:Q", format=".1f", title="Queda (pontos)")],
            ).properties(height=340),
            width="stretch",
        )

    st.subheader("Modelos comparados")
    st.caption("Sete algoritmos avaliados do mesmo jeito. O modelo foi escolhido pela validação cruzada no treino; "
               "o teste só confirma a escolha. Os três conjuntos de árvores empatam dentro do intervalo de confiança.")
    comparacao = (pd.DataFrame(info["comparacao_modelos"]).T.rename_axis("Modelo")
                  .sort_values("AUC_cv", ascending=False))
    # vírgula decimal, como no resto do app
    for col in ["AUC_cv", "AUC_teste"]:
        comparacao[col] = comparacao[col].map(lambda v: f"{v:.0%}")
    for col in ["AP_cv", "AP_teste"]:
        comparacao[col] = comparacao[col].map(lambda v: f"{v:.3f}".replace(".", ","))
    st.dataframe(
        comparacao.reset_index(), width="stretch", hide_index=True,
        column_config={
            "AUC_cv": st.column_config.TextColumn("Acerto na ordenação (treino)",
                                                  help="AUC na validação cruzada do treino, usada para escolher o modelo."),
            "AP_cv": st.column_config.TextColumn("Precisão média (treino)"),
            "AUC_teste": st.column_config.TextColumn("Acerto na ordenação (teste 2023 → 2024)"),
            "AP_teste": st.column_config.TextColumn("Precisão média (teste 2023 → 2024)"),
        },
    )

    with st.container(border=True):
        st.markdown(
            """
**Limitações**
- Treinado com apenas duas transições de ano. O modelo deve ser retreinado a cada novo PEDE.
- Não usa IPP (inexistente em 2022) nem inglês (avaliado só em algumas fases).
- Alunos que deixam o programa não têm desfecho observado, então o modelo estima o risco de quem continua.
- O acerto varia por fase: no teste, o modelo identificou 92% dos casos da ALFA e 40% dos casos das fases 3 a 5.
- A probabilidade ordena bem os alunos, mas superestima o risco abaixo de 60%. Serve para decidir a ordem de atendimento.
- A lista apoia a equipe e não substitui a avaliação pedagógica e psicológica.
"""
        )

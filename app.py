"""
🏠 App Streamlit — Previsão de Preços Imobiliários
==================================================

Ponto de entrada da aplicação. Responsável apenas por:
    1. Configurar a página.
    2. Carregar dados e treinar o modelo (com cache).
    3. Renderizar a UI e orquestrar a interação com o usuário.

Toda a lógica pesada (dados, ML, componentes visuais) está em `src/`.

Como executar:
    streamlit run app.py
"""

import streamlit as st

from src.data_loader import load_dataset
from src.model import TrainedModel, predict_price, train_model
from src.ui_components import (
    get_current_theme,
    inject_custom_css,
    render_header,
    render_prediction_card,
    render_theme_selector,
)


# --- Configuração da página --------------------------------------------------
# Deve ser a PRIMEIRA chamada Streamlit do script.
st.set_page_config(
    page_title="Previsão de Preços Imobiliários",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",  # sidebar aberta exibe o seletor de tema.
)


# --- Cache: carregamento e treino --------------------------------------------
# `@st.cache_resource` é ideal para objetos "vivos" (modelos, conexões),
# pois eles NÃO são serializados — diferente de `cache_data`, que copia.
# Resultado: o modelo é treinado apenas UMA vez por sessão do servidor.
@st.cache_resource(show_spinner="🔄 Treinando o modelo de Machine Learning...")
def get_trained_model() -> TrainedModel:
    """Carrega o dataset e treina o modelo, retornando um objeto reutilizável."""
    X, y = load_dataset()
    return train_model(X, y)


def main() -> None:
    """Função principal: monta a interface e trata a interação."""
    # Seletor de tema (sidebar) deve vir antes do CSS para que a paleta
    # selecionada seja aplicada já no primeiro render desta interação.
    render_theme_selector()
    theme = get_current_theme()

    # CSS customizado parametrizado pelo tema + cabeçalho.
    inject_custom_css(theme)
    render_header()

    # Modelo treinado (cacheado entre interações).
    model = get_trained_model()

    # --- Formulário de entrada -----------------------------------------------
    # `st.container(border=True)` cria o "card" de forma nativa do Streamlit,
    # envolvendo de fato os widgets internos (diferente de um <div> em markdown,
    # que não consegue agrupar componentes posteriores).
    # `st.form` evita reruns a cada tecla digitada — só dispara no submit.
    with st.container(border=True):
        st.subheader("📊 Dados do Imóvel")

        with st.form(key="prediction_form", clear_on_submit=False):
            # Linha 1: distância MRT e nº de lojas (lado a lado).
            # `value=None` deixa o campo vazio; `placeholder` exibe a dica
            # de exemplo enquanto o usuário não digita. O `st.number_input`
            # já restringe a entrada a dígitos, vírgula e ponto por padrão.
            col1, col2 = st.columns(2)
            with col1:
                distance_to_mrt = st.number_input(
                    "🚇 Distância até MRT (metros)",
                    min_value=0.0,
                    value=None,
                    step=10.0,
                    placeholder="Ex: 500",
                    help="Distância em metros até a estação de metrô mais próxima.",
                )
            with col2:
                num_convenience_stores = st.number_input(
                    "🏪 Nº de Lojas de Conveniência",
                    min_value=0,
                    value=None,
                    step=1,
                    placeholder="Ex: 5",
                    help="Quantidade de lojas de conveniência na vizinhança.",
                )

            # Linha 2: coordenadas geográficas.
            col3, col4 = st.columns(2)
            with col3:
                latitude = st.number_input(
                    "📍 Latitude",
                    value=None,
                    format="%.6f",
                    placeholder="Ex: 25,012300",
                    help="Latitude do imóvel (ex.: 25,012300).",
                )
            with col4:
                longitude = st.number_input(
                    "📍 Longitude",
                    value=None,
                    format="%.6f",
                    placeholder="Ex: 121,567800",
                    help="Longitude do imóvel (ex.: 121,567800).",
                )

            submitted = st.form_submit_button("🔮 Estimar Preço do Imóvel")

    # --- Resultado da previsão -----------------------------------------------
    # Como agora os campos iniciam vazios (value=None), validamos antes de
    # chamar o modelo — `None` quebraria a montagem do DataFrame de features.
    inputs = {
        "Distância até MRT":            distance_to_mrt,
        "Nº de lojas de conveniência":  num_convenience_stores,
        "Latitude":                     latitude,
        "Longitude":                    longitude,
    }
    missing = [name for name, value in inputs.items() if value is None]

    if submitted and missing:
        st.warning(
            "⚠️ Preencha todos os campos antes de gerar a previsão. "
            f"Faltando: {', '.join(missing)}."
        )
    elif submitted:
        try:
            prediction = predict_price(
                model=model,
                distance_to_mrt=distance_to_mrt,
                num_convenience_stores=num_convenience_stores,
                latitude=latitude,
                longitude=longitude,
            )
            render_prediction_card(prediction, theme)
        except Exception as exc:
            # Captura genérica como rede de segurança — exibe mensagem amigável
            # e mantém o stack trace acessível via expander.
            st.error("❌ Erro ao processar a previsão. Verifique os dados inseridos.")
            with st.expander("Detalhes técnicos"):
                st.exception(exc)
    else:
        st.info("👆 Preencha os campos acima e clique no botão para obter sua previsão!")

    # --- Métricas do modelo (rodapé informativo) -----------------------------
    with st.expander("📈 Sobre o modelo"):
        c1, c2, c3 = st.columns(3)
        c1.metric("R² (teste)", f"{model.r2:.3f}")
        c2.metric("MAE (teste)", f"{model.mae:.2f}")
        c3.metric("Amostras treino/teste", f"{model.n_train}/{model.n_test}")
        st.caption(
            "Modelo: Regressão Linear (scikit-learn). "
            "R² mede o quanto da variância dos preços é explicada pelas features; "
            "MAE é o erro médio absoluto da previsão."
        )


if __name__ == "__main__":
    main()

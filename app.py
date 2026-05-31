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
import streamlit.components.v1 as components

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
st.set_page_config(
    page_title="Previsão de Preços Imobiliários",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",  # sidebar aberta exibe o seletor de tema.
)


@st.cache_resource(show_spinner="🔄 Treinando o modelo de Machine Learning...")
def get_trained_model() -> TrainedModel:
    """Carrega o dataset e treina o modelo, retornando um objeto reutilizável."""
    X, y = load_dataset()
    return train_model(X, y)


def main() -> None:
    """Função principal: monta a interface e trata a interação."""
    components.html("""
    <script>
    try {
        var d = window.parent.document;
        var re = /[^0-9.\\-]/g;
        function fix(el) {
            if (el._nf) return; el._nf = true;
            el.addEventListener('keydown', function(e) {
                if (e.ctrlKey || e.metaKey ||
                    [8,9,13,27,46,37,38,39,40,35,36].indexOf(e.keyCode) > -1) return;
                if (!/[0-9.\\-]/.test(e.key)) e.preventDefault();
            });
            el.addEventListener('input', function(e) {
                var v = e.target.value, c = v.replace(re, '');
                if (v !== c) e.target.value = c;
            });
        }
        function scan() { d.querySelectorAll('.stTextInput input').forEach(fix); }
        new MutationObserver(scan).observe(d.body, {childList:true, subtree:true});
        scan();
    } catch(e) {}
    </script>
    """, height=0)

    render_theme_selector()
    theme = get_current_theme()

    inject_custom_css(theme)
    render_header()

    model = get_trained_model()

    with st.container(border=True):
        st.subheader("📊 Dados do Imóvel")

        with st.form(key="prediction_form", clear_on_submit=False):
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

            col3, col4 = st.columns(2)
            with col3:
                latitude = st.number_input(
                    "📍 Latitude",
                    min_value=-90.0,
                    max_value=90.0,
                    value=None,
                    step=0.000001,
                    format="%g",
                    placeholder="Ex: 25.0123",
                    help="Latitude do imóvel. Valores válidos entre -90 e 90.",
                )
            with col4:
                longitude = st.number_input(
                    "📍 Longitude",
                    min_value=-180.0,
                    max_value=180.0,
                    value=None,
                    step=0.000001,
                    format="%g",
                    placeholder="Ex: 121.5678",
                    help="Longitude do imóvel. Valores válidos entre -180 e 180.",
                )

            submitted = st.form_submit_button("🔮 Estimar Preço do Imóvel")

    # --- Resultado da previsão -----------------------------------------------
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
            # Captura genérica como rede de segurança — exibe mensagem amigável e mantém o stack trace acessível via expander.
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

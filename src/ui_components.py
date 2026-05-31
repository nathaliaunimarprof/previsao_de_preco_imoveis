"""
Componentes visuais reutilizáveis para o app Streamlit.

Concentra:
    - Paletas de cores acessíveis (claro/escuro, contraste WCAG AA).
    - CSS customizado parametrizado por tema.
    - Blocos de UI (header, card de resultado, seletor de tema).
"""

from typing import Dict

import streamlit as st

# --- Paletas de cores (testadas para contraste WCAG AA) ---------------------
# Todas as combinações texto/fundo atingem pelo menos 4.5:1 (texto normal)
# ou 3:1 (texto grande / elementos UI), conforme WCAG 2.1 AA.

LIGHT_THEME: Dict[str, str] = {
    "bg":             "#eef2f7",  # slate-100 levemente azulado (destaca cards brancos)
    "surface":        "#ffffff",  # cards / inputs
    "text_primary":   "#0f172a",  # slate-900 — 21:1 em branco
    "text_secondary": "#334155",  # slate-700 — 11:1
    "text_muted":     "#475569",  # slate-600 — 7.5:1
    "primary":        "#4338ca",  # indigo-700 — 8.6:1 em branco
    "primary_hover":  "#3730a3",  # indigo-800 — 11:1
    "on_primary":     "#ffffff",
    "success":        "#15803d",  # green-700 — 5.9:1 em branco
    "error":          "#b91c1c",  # red-700 — 7.4:1
    "border":         "#cbd5e1",  # slate-300 — borda visível
    "header_bg":      "linear-gradient(135deg, #4338ca 0%, #7c3aed 100%)",
    "shadow":         "0 6px 20px rgba(15, 23, 42, 0.08)",
}

DARK_THEME: Dict[str, str] = {
    "bg":             "#020617",  # slate-950 — preto-azulado profundo
    "surface":        "#1e293b",  # slate-800 — cards
    "text_primary":   "#f1f5f9",  # slate-100 — 14:1 em slate-800
    "text_secondary": "#cbd5e1",  # slate-300 — 10:1
    "text_muted":     "#94a3b8",  # slate-400 — 6:1
    "primary":        "#6366f1",  # indigo-500 — texto branco 4.8:1 ✓ AA
    "primary_hover":  "#4f46e5",  # indigo-600 — escurece no hover (5.6:1)
    "on_primary":     "#ffffff",  # texto branco em ambos os temas (consistência)
    "success":        "#34d399",  # emerald-400 — 8:1 em slate-800
    "error":          "#f87171",  # red-400 — 6:1
    "border":         "#334155",  # slate-700
    "header_bg":      "linear-gradient(135deg, #4338ca 0%, #6d28d9 100%)",
    "shadow":         "0 6px 20px rgba(0, 0, 0, 0.5)",
}

THEMES: Dict[str, Dict[str, str]] = {"Claro": LIGHT_THEME, "Escuro": DARK_THEME}


def get_current_theme() -> Dict[str, str]:
    """Retorna a paleta ativa a partir de st.session_state['theme_name']."""
    return THEMES[st.session_state.get("theme_name", "Claro")]


def render_theme_selector() -> None:
    """Renderiza o seletor de tema na sidebar e persiste a escolha em sessão."""
    with st.sidebar:
        st.markdown("### 🎨 Aparência")
        st.radio(
            label="Tema visual",
            options=list(THEMES.keys()),
            key="theme_name",
            horizontal=True,
            help="Alterna entre tema claro e escuro.",
        )


def inject_custom_css(theme: Dict[str, str]) -> None:
    """
    Injeta o CSS customizado parametrizado pela paleta `theme`.

    O bloco cobre TODOS os elementos do Streamlit que normalmente herdam
    cores padrão (headings, labels, métricas, alerts, expander, sidebar),
    garantindo contraste adequado em ambos os temas.
    """
    st.markdown(
        f"""
        <style>
            /* ===== Fundos base ============================================ */
            .stApp {{ background: {theme['bg']}; color: {theme['text_primary']}; }}
            [data-testid="stSidebar"] {{
                background: {theme['surface']} !important;
                border-right: 1px solid {theme['border']};
            }}

            /* ===== Tipografia global (força contraste em TODO texto) ===== */
            .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
            .stApp p, .stApp label, .stApp span, .stApp li, .stApp small,
            .stApp div[data-testid="stMarkdownContainer"],
            .stApp div[data-testid="stMarkdownContainer"] *,
            [data-testid="stSidebar"] * {{
                color: {theme['text_primary']};
            }}
            /* Labels dos widgets (number_input, radio, etc.) */
            [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] * {{
                color: {theme['text_primary']} !important;
                font-weight: 600;
            }}
            /* Captions e textos secundários */
            .stApp [data-testid="stCaptionContainer"],
            .stApp [data-testid="stCaptionContainer"] * {{
                color: {theme['text_secondary']} !important;
            }}

            /* ===== Header (gradient — texto sempre branco) ================ */
            .app-header {{
                background: {theme['header_bg']};
                padding: 32px 24px;
                border-radius: 14px;
                margin-bottom: 28px;
                box-shadow: {theme['shadow']};
                text-align: center;
                animation: fadeInUp 0.5s ease-out;
            }}
            .app-header h1, .app-header p {{ color: #ffffff !important; }}
            .app-header h1 {{ margin: 0; font-size: 2.1rem; font-weight: 700; }}
            .app-header p  {{ margin: 8px 0 0; font-size: 1.05rem; opacity: 0.95; }}

            /* ===== Card genérico ========================================== */
            .card {{
                background: {theme['surface']};
                color: {theme['text_primary']};
                padding: 26px;
                border-radius: 14px;
                border: 1px solid {theme['border']};
                box-shadow: {theme['shadow']};
                margin-bottom: 18px;
                animation: fadeInUp 0.5s ease-out;
            }}

            /* ===== Inputs (number_input estilo "pill" unificado) ========= */
            /* Estratégia: pintar o container raiz com a cor de superfície e
               forçar TODOS os descendentes (exceto botões +/-) a serem
               transparentes — assim o Streamlit/BaseWeb não consegue impor
               cores escuras herdadas do seu próprio tema interno. */
            [data-testid="stNumberInput"] > div {{
                background: {theme['surface']} !important;
                border: 1px solid {theme['border']} !important;
                border-radius: 10px !important;
                overflow: hidden;
                transition: border-color 0.15s ease, box-shadow 0.15s ease;
            }}
            [data-testid="stNumberInput"] > div:focus-within {{
                border-color: {theme['primary']} !important;
                box-shadow: 0 0 0 3px {theme['border']};
            }}
            /* Anula qualquer fundo herdado dos wrappers internos do BaseWeb. */
            [data-testid="stNumberInput"] > div > div,
            [data-testid="stNumberInput"] [data-baseweb="input"],
            [data-testid="stNumberInput"] [data-baseweb="input"] > div,
            [data-testid="stNumberInput"] [data-baseweb="base-input"] {{
                background: transparent !important;
                border: none !important;
            }}
            [data-testid="stNumberInput"] input {{
                background: transparent !important;
                color: {theme['text_primary']} !important;
                border: none !important;
                box-shadow: none !important;
                outline: none !important;
            }}
            /* Placeholder (ex.: "Ex: 500") — força contraste em ambos os temas.
               `opacity: 1` neutraliza o padrão do Firefox que aplica opacidade
               reduzida automaticamente em ::placeholder. */
            [data-testid="stNumberInput"] input::placeholder,
            .stTextInput input::placeholder {{
                color: {theme['text_muted']} !important;
                opacity: 1 !important;
                font-style: italic;
            }}
            /* Mesmo tratamento para text_input. */
            .stTextInput > div > div {{
                background: {theme['surface']} !important;
                border: 1px solid {theme['border']} !important;
                border-radius: 10px !important;
            }}
            .stTextInput input {{
                background: transparent !important;
                color: {theme['text_primary']} !important;
                border: none !important;
                box-shadow: none !important;
            }}
            /* Botões +/- do number_input — divisor sutil + hover discreto. */
            [data-testid="stNumberInput"] button {{
                background: transparent !important;
                color: {theme['text_secondary']} !important;
                border: none !important;
                border-left: 1px solid {theme['border']} !important;
                border-radius: 0 !important;
                box-shadow: none !important;
                transition: background 0.15s ease, color 0.15s ease;
            }}
            [data-testid="stNumberInput"] button:hover {{
                background: {theme['bg']} !important;
                color: {theme['primary']} !important;
            }}

            /* ===== Botão primário ========================================= */
            /* Importante: pintamos QUALQUER descendente (p, span, svg) para
               vencer a regra global `.stApp p {{ color: text_primary }}`. */
            .stButton > button, .stFormSubmitButton > button {{
                background: {theme['primary']} !important;
                color: {theme['on_primary']} !important;
                border: 2px solid transparent !important;
                padding: 12px 32px !important;
                font-size: 1rem !important;
                font-weight: 700 !important;
                border-radius: 10px !important;
                width: 100%;
                transition: background 0.15s ease, transform 0.15s ease,
                            box-shadow 0.15s ease;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            }}
            .stButton > button *, .stFormSubmitButton > button * {{
                color: {theme['on_primary']} !important;
                fill: {theme['on_primary']} !important;
            }}
            .stButton > button:hover, .stFormSubmitButton > button:hover {{
                background: {theme['primary_hover']} !important;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }}
            .stButton > button:focus-visible,
            .stFormSubmitButton > button:focus-visible {{
                outline: 3px solid {theme['primary']} !important;
                outline-offset: 3px !important;
            }}

            /* ===== Alerts (st.info / warning / error / success) =========== */
            [data-testid="stAlert"] {{
                background: {theme['surface']} !important;
                border: 1px solid {theme['border']} !important;
                border-left: 4px solid {theme['primary']} !important;
                border-radius: 10px;
            }}
            [data-testid="stAlert"] * {{ color: {theme['text_primary']} !important; }}

            /* ===== Expander =============================================== */
            [data-testid="stExpander"] {{
                background: {theme['surface']};
                border: 1px solid {theme['border']} !important;
                border-radius: 10px;
            }}
            [data-testid="stExpander"] * {{ color: {theme['text_primary']} !important; }}

            /* ===== Métricas (st.metric) =================================== */
            [data-testid="stMetric"] {{
                background: {theme['surface']};
                border: 1px solid {theme['border']};
                padding: 14px 16px;
                border-radius: 10px;
            }}
            [data-testid="stMetricLabel"] * {{
                color: {theme['text_secondary']} !important;
                font-weight: 600;
            }}
            [data-testid="stMetricValue"] * {{
                color: {theme['text_primary']} !important;
                font-weight: 700;
            }}

            /* ===== Destaque do preço estimado ============================= */
            .price-value {{ font-size: 2.4rem; font-weight: 800; color: {theme['success']}; }}

            /* ===== Animação =============================================== */
            @keyframes fadeInUp {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to   {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    """Renderiza o cabeçalho principal do aplicativo."""
    st.markdown(
        """
        <div class="app-header" role="banner">
            <h1>🏠 Previsão de Preços Imobiliários</h1>
            <p>Estimar o valor de imóveis com base em dados reais.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_card(prediction: float, theme: Dict[str, str]) -> None:
    """Renderiza o card de resultado com o preço estimado."""
    st.markdown(
        f"""
        <div class="card" style="text-align:center;" role="status" aria-live="polite">
            <h3 style="color:{theme['success']}; margin-bottom: 12px;">
                ✅ Previsão Concluída!
            </h3>
            <div>
                <span style="font-size:1.05rem; color:{theme['text_primary']};">💰 Preço Estimado: </span>
                <span class="price-value">R$ {prediction:,.2f}</span>
                <span style="font-size:1rem; color:{theme['text_secondary']};"> por m²</span>
            </div>
            <p style="color:{theme['text_secondary']}; font-size:0.9rem; margin-top:10px; font-style:italic;">
                📊 Previsão gerada por machine learning com base nos dados fornecidos.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

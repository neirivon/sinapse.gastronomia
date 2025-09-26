# /home/neirivon/SINAPSE2.0/GASTRONOMIA/pages/05_Indicadores.py

import streamlit as st
import pandas as pd
import altair as alt

# ==== CSS Global (legibilidade/consistência) ====
st.markdown("""
<style>
h1 { font-size: 42px !important; font-weight: 700 !important; }
h2, h3 { font-size: 30px !important; font-weight: 600 !important; }
p, li, div, span { font-size: 22px !important; }
.caption { font-size: 18px !important; color: #444 !important; }
.stTable table { font-size: 22px !important; }
.stTable th, .stTable td { font-size: 22px !important; }
</style>
""", unsafe_allow_html=True)

# ==== Cabeçalho ====
st.markdown("""
<div style="padding:16px; border-radius:16px; background:#eef6ff; border:1px solid #d0e2f0; margin-bottom:12px;">
  <h1 style="margin:0;">📊 Indicadores</h1>
  <p style="margin:6px 0 0 0;">Acompanhamento de permanência e engajamento comunidade-escola (dados ilustrativos).</p>
</div>
""", unsafe_allow_html=True)

# ==== KPIs (exemplo ilustrativo) ====
c1, c2, c3 = st.columns(3)
c1.metric("Participação comunitária (último mês)", "38%", "+7 pp")
c2.metric("Evasão (semestre)", "5,8%", "-1,2 pp")
c3.metric("Projetos/Feiras ativos", "12", "+3")

st.divider()

# ==== Série temporal (Altair) ====
st.subheader("📈 Tendência de participação comunitária (%)")
df = pd.DataFrame({
    "Mês": pd.date_range("2025-01-01", periods=12, freq="MS"),
    "Participação (%)": [18,19,20,22,21,24,25,27,30,33,36,38]
})
linha = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(
        x=alt.X("Mês:T", title="Mês"),
        y=alt.Y("Participação (%):Q", title="Participação comunitária (%)"),
        tooltip=[alt.Tooltip("Mês:T", title="Mês"), alt.Tooltip("Participação (%):Q", title="%")]
    )
    .properties(height=320)
)
st.altair_chart(linha, use_container_width=True)

st.divider()

# ==== Tabela-resumo com tooltips nos cabeçalhos ====
st.subheader("📋 Resumo por dimensão (último bimestre)")
res = pd.DataFrame({
    "Dimensão": ["Participação Comunitária", "Currículo Regionalizado", "Projetos & Parcerias", "Permanência & Êxito", "Inovação (IA)"],
    "Meta": ["≥ 35%", "≥ 30% do currículo", "≥ 8 ações", "Evasão ≤ 6%", "2 painéis + relatórios"],
    "Status": ["38%", "28% do currículo", "12 ações", "5,8%", "MVP pronto"],
    "Risco": ["baixo", "médio", "baixo", "médio-baixo", "baixo"]
})
st.dataframe(
    res,
    use_container_width=True,
    column_config={
        "Dimensão": st.column_config.TextColumn("Dimensão", help="Eixo avaliado"),
        "Meta": st.column_config.TextColumn("Meta", help="Patamar desejado"),
        "Status": st.column_config.TextColumn("Status", help="Valor mais recente"),
        "Risco": st.column_config.TextColumn("Risco", help="Baixo / Médio / Alto"),
    }
)

st.caption("Observação: valores ilustrativos para fins de protótipo. Substituir por dados reais quando disponíveis.")


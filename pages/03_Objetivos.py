# /home/neirivon/SINAPSE2.0/GASTRONOMIA/pages/03_Objetivos.py

import streamlit as st
import pandas as pd

# ==== CSS Global (legibilidade/consistência) ====
st.markdown("""
<style>
h1 { font-size: 42px !important; font-weight: 700 !important; }
h2, h3 { font-size: 30px !important; font-weight: 600 !important; }
p, li, div, span { font-size: 22px !important; }
.caption { font-size: 18px !important; color: #444 !important; }
/* Cartõezinhos */
.card {
  padding:16px; border-radius:14px; border:1px solid #e6e6e6;
  background:#fafafa; margin-bottom:14px;
}
.card-ok    { border-left:6px solid #2e7d32; }
.card-warn  { border-left:6px solid #f9a825; }
.card-info  { border-left:6px solid #1565C0; }
.card-ia    { border-left:6px solid #8e24aa; }
</style>
""", unsafe_allow_html=True)

# ==== Cabeçalho ====
st.markdown("""
<div style="padding:18px; border-radius:16px; background:#e7f3ff; border:1px solid #cfe3ff; margin-bottom:16px;">
  <h1 style="margin:0;">🎯 Objetivos</h1>
  <p style="margin:6px 0 0 0;">Estudo de Caso 8 — <b>Falta de Diálogo com a Comunidade na Gastronomia</b></p>
</div>
""", unsafe_allow_html=True)

# ==== Objetivo Geral ====
st.subheader("🎯 Objetivo Geral")
st.markdown("""
<div class="card card-info">
Promover, no **Curso Técnico em Gastronomia** (IFRS – Campus Central), a **integração sistemática com a comunidade**,
valorizando saberes locais e fortalecendo a **permanência e o êxito discente**, por meio de **projetos de extensão,
currículo regionalizado** e **uso responsável de tecnologias (IA em WhatsApp/Telegram)** para escuta e devolutivas.
</div>
""", unsafe_allow_html=True)

st.divider()

# ==== Objetivos Específicos (agrupados por dimensão da rubrica) ====
st.subheader("📌 Objetivos Específicos (por dimensão da rubrica)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **1) Participação Comunitária**
    - Instituir **Conselho Consultivo Comunitário** com encontros bimestrais e **atas públicas**.
    - Criar **canais de escuta** (formulário + **chatbot WhatsApp/Telegram**) para coletar sugestões e demandas.
    - Garantir **devolutivas** às contribuições (relatórios semestrais e reuniões abertas).
    """)
    st.markdown("""
    **2) Currículo Regionalizado**
    - Mapear **receitas, práticas e ingredientes locais** e incorporar **≥30%** do currículo a partir desse repertório.
    - Convidar **mestres de ofício** e produtores locais para oficinas e aulas demonstrativas.
    """)

with col2:
    st.markdown("""
    **3) Projetos & Parcerias**
    - Planejar **feiras e oficinas semestrais** integradas ao calendário do município.
    - Firmar **parcerias** com produtores, restaurantes, turismo e instituições culturais (≥ 8 ativas/ano).
    """)
    st.markdown("""
    **4) Permanência & Êxito Discente**
    - Implantar **Tutoria de Acolhimento** (ingressantes) e **Tutoria de Percurso** (veteranos).
    - Monitorar engajamento e **sinais de evasão** com indicadores e atendimentos proativos.
    """)
    st.markdown("""
    **5) Inovação Tecnológica (IA)**
    - Operar **chatbot comunitário** (WhatsApp/Telegram) para **escuta, FAQs** e convites para eventos.
    - Consolidar dados em **painel Streamlit** (feedback, indicadores e relatórios ao NDE/Coordenação).
    """)

st.divider()

# ==== Metas SMART (2025/1 → 2025/2) ====
st.subheader("✅ Metas SMART (horizonte de 2 semestres)")
st.markdown("""
<div class="card card-ok">
<b>M1. Conselho ativo:</b> realizar <b>≥ 4 reuniões</b> com atas públicas e plano de acompanhamento.
<br/><b>M2. Currículo regional:</b> alcançar <b>≥ 30%</b> de componentes/práticas com conteúdo regional até o final de 2025/2.
<br/><b>M3. Parcerias:</b> firmar <b>≥ 8 parcerias</b> registradas (produtores/empreendedores/secretarias/ONGs).
<br/><b>M4. Eventos:</b> executar <b>2 feiras/oficinas</b> por ano com público externo ≥ 200 pessoas (soma).
<br/><b>M5. Permanência:</b> reduzir a evasão em <b>20%</b> vs. linha de base 2024, com tutoria e alertas precoces.
<br/><b>M6. IA/Comunicação:</b> chatbot ativo com <b>≥ 300 interações</b> válidas/semestre e taxa de resposta ≥ 90%.
<br/><b>M7. Devolutivas:</b> publicar <b>2 relatórios</b> semestrais de retorno à comunidade (PDF/streamlit).
</div>
""", unsafe_allow_html=True)

st.divider()

# ==== Alinhamento objetivos x Rubrica ====
st.subheader("🧭 Alinhamento com a Rubrica (dimensão ↔ ação alvo)")
mapa = pd.DataFrame({
    "Dimensão da Rubrica": [
        "1. Participação Comunitária",
        "2. Currículo Regionalizado",
        "3. Projetos & Parcerias",
        "4. Permanência & Êxito Discente",
        "5. Inovação Tecnológica (IA)"
    ],
    "Ação/Resultado Esperado": [
        "Conselho ativo, escuta contínua e devolutivas públicas.",
        "≥30% do currículo com eixo regional e mestres locais convidados.",
        "Feiras/oficinas semestrais e ≥8 parcerias registradas.",
        "Tutoria de acolhimento+percurso; redução de 20% da evasão.",
        "Chatbot WhatsApp/Telegram + painel Streamlit com relatórios."
    ],
    "Indicador-chave (KPI)": [
        "Nº reuniões/atas; participação externa; nº sugestões respondidas.",
        "% de componentes regionais; nº convidados locais por semestre.",
        "Nº eventos e público; nº parcerias ativas; satisfação (NPS).",
        "Taxa de evasão; atendimentos de tutoria; presença/participação.",
        "Interações no chatbot; tempo de resposta; relatórios publicados."
    ]
})
mapa.index = pd.Index(range(1, len(mapa)+1), name="Nº")
st.table(mapa.style.set_properties(**{"font-size": "22px"}))

st.divider()

# ==== Observação didática ====
st.info(
    "Os **objetivos** orientam o **Plano de Ação**: para cada objetivo específico, "
    "definiremos tarefas, responsáveis, prazos, recursos e indicadores (página **Plano de Ação**)."
)

st.caption("Nota: a IA proposta limita-se a chatbot de escuta (WhatsApp/Telegram) e consolidação de dados em painel Streamlit.")


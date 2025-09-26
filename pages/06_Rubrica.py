# /home/neirivon/SINAPSE2.0/GASTRONOMIA/pages/06_Rubrica.py

import streamlit as st
import pandas as pd

# ==== CSS Global (legibilidade/consistência) ====
st.markdown("""
<style>
h1 { font-size: 42px !important; font-weight: 700 !important; }
h2, h3 { font-size: 30px !important; font-weight: 600 !important; }
/* Texto geral */
p, li, div, span { font-size: 22px !important; }
/* Tabelas estáticas (st.table) */
.stTable table { font-size: 22px !important; }
.stTable th { font-size: 22px !important; font-weight: 700 !important; }
.stTable td { font-size: 22px !important; }
/* Legendas */
.caption { font-size: 18px !important; color: #444 !important; }
</style>
""", unsafe_allow_html=True)

# ==== Banner inicial ====
st.markdown("""
<div style="padding:18px; border-radius:16px; background:#eef6ff; border:1px solid #d0e2f0; margin-bottom:16px;">
  <h1 style="margin:0;">📊 Rubrica Pedagógica — Curso Técnico em Gastronomia</h1>
  <p style="margin:6px 0 0 0;"><b>Instituição:</b> Instituto Federal do Rio Grande do Sul — Campus Central</p>
  <p style="margin:2px 0 0 0;"><b>Eixo:</b> Superação da Falta de Diálogo com a Comunidade (Caso 8)</p>
  <p style="margin:2px 0 0 0;"><b>Objetivo:</b> avaliar o nível de maturidade do curso em 5 dimensões, de <i>Emergente</i> até <i>Avançado</i>.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### O que é esta rubrica?")
st.markdown("""
É um **instrumento pedagógico** para avaliar **processos institucionais e participativos** do curso,
**não** o desempenho individual de alunos. Ela ajuda a identificar **onde estamos** e **como avançar**
em cada dimensão-chave relacionada ao diálogo com a comunidade.
""")

st.divider()
st.subheader("🔎 Dimensões avaliadas — explicação didática")

with st.expander("📢 1) Participação Comunitária", expanded=True):
    st.markdown("""
    Mede como a **comunidade local participa das decisões e atividades** do curso:
    conselho consultivo, reuniões abertas, escuta ativa e retorno das decisões.
    - **Exemplo:** Conselho Consultivo com atas mensais, escuta via formulário/chatbot, devolutiva pública.
    """)

with st.expander("🥘 2) Currículo Regionalizado"):
    st.markdown("""
    Observa o quanto o **currículo, as práticas e as receitas** refletem a **cultura alimentar do território**.
    - **Exemplo:** componentes com conteúdos regionais, técnicas, ingredientes e saberes locais.
    """)

with st.expander("🤝 3) Projetos & Parcerias com a Comunidade"):
    st.markdown("""
    Verifica a existência e qualidade de **parcerias**, **eventos**, **oficinas** e **projetos de extensão**
    com atores do território (produtores, empreendedores, festivais).
    """)

with st.expander("🎓 4) Permanência & Êxito Discente"):
    st.markdown("""
    Avalia **acolhimento**, **engajamento** e **resultados**: prevenção de evasão, tutoria, apoio socioemocional,
    aprendizagem ativa, e satisfação de estudantes e comunidade.
    """)

with st.expander("🤖 5) Inovação Tecnológica (IA)"):
    st.markdown("""
    Olha para o uso **responsável** de **IA e ferramentas digitais** para **ouvir a comunidade**,
    **organizar feedback**, **gerar relatórios**, **personalizar trilhas** e **monitorar indicadores**.

    **Canais propostos:** inicialmente por meio de **chatbots no WhatsApp e no Telegram** (acesso simples para a comunidade,
    sem necessidade de instalar novos apps). Em fases futuras, os dados alimentam o painel Streamlit para relatórios.
    """)

st.divider()
st.subheader("🪜 Níveis de maturidade — do básico ao avançado")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**1) Emergente**")
    st.progress(25, text="Iniciativas pontuais, sem sistematização.")
    st.caption("- Contatos esporádicos com a comunidade\n- Currículo pouco regionalizado\n- Parcerias informais")
with col2:
    st.markdown("**2) Intermediário**")
    st.progress(50, text="Ações isoladas, início de organização.")
    st.caption("- Reuniões esparsas\n- Experimentos de atividades regionais\n- Alguns projetos/feiras isolados")

col3, col4 = st.columns(2)
with col3:
    st.markdown("**3) Proficiente**")
    st.progress(75, text="Processos recorrentes e integrados.")
    st.caption("- Conselho ativo com atas\n- ≥30% do currículo com eixo regional\n- Projetos/feiras semestrais, parcerias registradas")
with col4:
    st.markdown("**4) Avançado (IA)**")
    st.progress(100, text="Institucionalização + IA para escala e qualidade.")
    st.caption("- **Chatbot comunitário no WhatsApp/Telegram** + análise automática de feedback\n- Relatórios para o conselho\n- Recomendação de atividades\n- Monitoramento preditivo de permanência")

st.divider()
st.subheader("📐 Rubrica completa (5 dimensões × 4 níveis)")

# ==== Tabela da rubrica (com índice começando em 1) ====
rubrica = pd.DataFrame({
    "Dimensão": [
        "1. Participação Comunitária",
        "2. Currículo Regionalizado",
        "3. Projetos & Parcerias",
        "4. Permanência & Êxito Discente",
        "5. Inovação Tecnológica (IA)"
    ],
    "Emergente": [
        "Contatos pontuais; sem registro.",
        "Disciplinas genéricas; pouca referência local.",
        "Parcerias informais; ações esparsas.",
        "Acolhimento mínimo; sem monitoramento.",
        "Uso restrito a tarefas administrativas."
    ],
    "Intermediário": [
        "Reuniões esporádicas; pouca sistematização.",
        "Inserções pontuais de conteúdos/receitas regionais.",
        "Projetos de extensão isolados; pouca continuidade.",
        "Tutoria/ações isoladas; dados pouco utilizados.",
        "Experimentos isolados de tecnologia em disciplinas."
    ],
    "Proficiente": [
        "Conselho consultivo ativo; atas periódicas; devolutivas.",
        "≥30% do currículo com eixo regional; práticas e ingredientes locais.",
        "Feiras/oficinas semestrais; parcerias registradas e ativas.",
        "Plano estruturado de permanência; relatórios bimestrais; metas.",
        "Plataformas digitais apoiando eventos, registros e indicadores."
    ],
    "Avançado (IA)": [
        "**Conselho + chatbot de escuta no WhatsApp/Telegram**; relatórios automáticos ao NDE/Coord.",
        "Currículo atualizado com dados da comunidade (tags/sugestões via IA).",
        "IA mapeia parceiros; recomenda colaborações e calendário de eventos.",
        "Análise preditiva de risco de evasão; alertas para tutores e acolhimento.",
        "Painel interativo + IA: feedback, relatórios, trilhas personalizadas, KPIs."
    ],
})

# índice 1..N com rótulo "Nº"
rubrica.index = pd.Index(range(1, len(rubrica) + 1), name="Nº")

# === Tooltips e estilos (st.dataframe) ===
# Dica: column_config habilita tooltips nos cabeçalhos
colcfg = {
    "Dimensão": st.column_config.TextColumn("Dimensão", help="Eixo avaliado (o 'o quê' da qualidade)."),
    "Emergente": st.column_config.TextColumn("Emergente", help="Início: iniciativas pontuais, sem sistematização."),
    "Intermediário": st.column_config.TextColumn("Intermediário", help="Organização inicial; ações ainda isoladas."),
    "Proficiente": st.column_config.TextColumn("Proficiente", help="Processos recorrentes e integrados; resultados visíveis."),
    "Avançado (IA)": st.column_config.TextColumn("Avançado (IA)", help="Escala e qualidade com apoio de IA e institucionalização."),
}

# Cabeçalhos com cor sutil por nível (apenas efeito visual leve)
st.markdown("""
<style>
/* A cor no cabeçalho pode variar entre temas; mantemos leve e neutro */
thead tr th:nth-child(2){background:#fff7e6;}  /* Emergente */
thead tr th:nth-child(3){background:#f3f9ff;}  /* Intermediário */
thead tr th:nth-child(4){background:#eefcf0;}  /* Proficiente */
thead tr th:nth-child(5){background:#f5f0ff;}  /* Avançado (IA) */
</style>
""", unsafe_allow_html=True)

st.dataframe(
    rubrica,
    use_container_width=True,
    hide_index=False,
    column_config=colcfg
)

# ==== Notas de ética/LGPD ====
st.info("**Uso responsável de IA**: anonimização, consentimento, finalidade pedagógica, transparência e opção de não participação.")

st.markdown("""
<div style="margin-top:10px; padding:12px; border-radius:12px; background:#fff7b2;">
<b>Como ler e usar a rubrica:</b> identifique o nível atual em cada dimensão, defina metas para o próximo nível
(e.g., de Intermediário → Proficiente) e registre evidências (atas, PPC, registros de projetos, indicadores).
</div>
""", unsafe_allow_html=True)

st.caption("Nota para a equipe: apresentar esta rubrica antes do Plano de Ação ajuda a contextualizar por que cada ação existe e como será avaliada.")


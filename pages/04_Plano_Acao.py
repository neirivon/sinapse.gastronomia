# /home/neirivon/SINAPSE2.0/GASTRONOMIA/pages/04_Plano_Acao.py

import streamlit as st
import pandas as pd

# ==== CSS Global (legibilidade/consistência) ====
st.markdown("""
<style>
h1 { font-size: 42px !important; font-weight: 700 !important; }
h2, h3 { font-size: 30px !important; font-weight: 600 !important; }
p, li, div, span { font-size: 22px !important; }
.caption { font-size: 18px !important; color: #444 !important; }
.stTable table { font-size: 22px !important; }
.stTable th, .stTable td { font-size: 22px !important; }
.card { padding:16px; border-radius:14px; border:1px solid #e6e6e6; background:#fafafa; margin-bottom:14px; }
.card-info{ border-left:6px solid #1565C0; }
.card-ok  { border-left:6px solid #2e7d32; }
.card-warn{ border-left:6px solid #f9a825; }
.card-ia  { border-left:6px solid #8e24aa; }
.badge { display:inline-block; padding:2px 8px; border-radius:8px; background:#e8f0fe; border:1px solid #c7dafc; font-size:18px; }
</style>
""", unsafe_allow_html=True)

# ==== Cabeçalho ====
st.markdown("""
<div style="padding:18px; border-radius:16px; background:#eef9f1; border:1px solid #cde9d6; margin-bottom:16px;">
  <h1 style="margin:0;">🛠️ Plano de Ação</h1>
  <p style="margin:6px 0 0 0;">Desdobramento dos objetivos em tarefas, responsáveis, prazos, recursos e indicadores.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card card-info">
<b>Escopo:</b> IFRS – Campus Central · Curso Técnico em Gastronomia · Estudo de Caso 8 (Falta de diálogo com a comunidade).<br/>
<b>Horizonte:</b> 2 semestres (2025/1 e 2025/2).<br/>
<b>Alinhamento:</b> Dimensões da <i>Rubrica</i> (Participação, Currículo, Projetos/Parcerias, Permanência/Êxito, Inovação/IA).
</div>
""", unsafe_allow_html=True)

# ==== Plano mestre (tabela principal) ====
st.subheader("📋 Plano mestre (tarefas, prazos e indicadores)")

plano = pd.DataFrame([
    # Nº, Dimensão, Ação, Responsável, Co-responsáveis, Início, Fim, Entregáveis, Indicadores, Evidências
    [1, "1. Participação Comunitária",
     "Instituir Conselho Consultivo Comunitário e calendário bimestral",
     "Neirivon", "Gerson; Profa. Juliene", "2025-03-01", "2025-12-15",
     "Portaria do Conselho; calendário; 4 atas públicas",
     "≥4 reuniões/ano; participação externa ≥ 25 pessoas/semestre",
     "Portaria; atas; lista de presença; relatórios de devolutiva"],

    [2, "1. Participação Comunitária",
     "Canais de escuta: formulário + chatbot WhatsApp/Telegram",
     "Gerson", "Neirivon; Profa. Juliene", "2025-03-15", "2025-06-30",
     "QR code; link; bot operacional; base de dados",
     "≥300 interações/semestre; tempo médio de resposta ≤ 24h",
     "Prints do bot; logs; planilhas de feedback; relatório semestral"],

    [3, "2. Currículo Regionalizado",
     "Mapear repertório local (receitas, técnicas, ingredientes; mestres de ofício)",
     "Neirivon", "Gerson", "2025-03-10", "2025-05-30",
     "Catálogo regional (PDF/Streamlit); lista de convidados",
     "≥30 itens mapeados; ≥6 convidados/ano",
     "Catálogo; termos de convite; registros fotográficos"],

    [4, "2. Currículo Regionalizado",
     "Inserir ≥30% de conteúdos/práticas regionais no PPC/planos de ensino",
     "Profa. Juliene", "NDE; Colegiado", "2025-06-01", "2025-10-30",
     "Propostas de alteração; aprovação em ata",
     "≥30% dos componentes adaptados; plano de acompanhamento",
     "Propostas; pareceres; atas do NDE/Colegiado"],

    [5, "3. Projetos & Parcerias",
     "Feiras/oficinas semestrais integradas ao calendário municipal",
     "Gerson", "Neirivon; parceiros externos", "2025-06-15", "2025-12-10",
     "2 eventos (2025/1 e 2025/2) com programação",
     "Público total ≥ 200 pessoas/ano; satisfação ≥ 85%",
     "Programação; ofícios; lista de presença; pesquisa NPS"],

    [6, "3. Projetos & Parcerias",
     "Firmar parcerias com produtores/restaurantes/turismo/ONGs",
     "Neirivon", "Gerson", "2025-04-01", "2025-11-30",
     "≥8 termos de parceria/ano (MOUs) registrados",
     "≥8 parcerias ativas; ≥1 ação por parceria",
     "MOUs assinados; relatórios de ação; registro fotográfico"],

    [7, "4. Permanência & Êxito",
     "Implantar Tutoria de Acolhimento (ingressantes) e de Percurso (veteranos)",
     "Profa. Juliene", "Coordenação; Assistência Estudantil", "2025-03-20", "2025-12-15",
     "Plano de tutoria; agenda; registro de atendimentos",
     "Redução de evasão em 20% vs. 2024; presença ≥ 80%",
     "Planilhas de tutoria; relatórios bimestrais; SIGAA"],

    [8, "4. Permanência & Êxito",
     "Alerta precoce: monitorar faltas e engajamento (dash simples)",
     "Gerson", "Neirivon", "2025-04-10", "2025-06-30",
     "Painel Streamlit com dados de presença/participação",
     "Alertas gerados; atendimentos realizados ≥ 80% dos casos",
     "Dash; prints; registros de atendimento"],

    [9, "5. Inovação Tecnológica (IA)",
     "Consolidar feedback do chatbot em painel Streamlit + relatório ao NDE",
     "Neirivon", "Gerson", "2025-06-01", "2025-12-05",
     "Painel de feedback; 2 relatórios/ano (devolutiva pública)",
     "2 relatórios publicados; issues priorizadas",
     "Relatórios PDF; link do painel; evidências de resposta à comunidade"]
], columns=[
    "Nº", "Dimensão", "Ação", "Responsável", "Co-responsáveis",
    "Início", "Fim", "Entregáveis", "Indicadores", "Evidências"
])

plano.index = pd.Index(range(1, len(plano) + 1), name="Nº")
st.table(plano.style.set_properties(**{"font-size": "22px"}))

# ==== Download do plano em CSV ====
csv_bytes = plano.to_csv(index=True).encode("utf-8")
st.download_button(
    label="⬇️ Baixar plano (CSV)",
    data=csv_bytes,
    file_name="plano_de_acao_gastronomia.csv",
    mime="text/csv"
)

st.divider()

# ==== Cronograma por semestre (visão macro) ====
st.subheader("🗓️ Cronograma macro (2025/1 → 2025/2)")
cronograma = pd.DataFrame({
    "Frente": [
        "Conselho Consultivo", "Canais de Escuta (Form + Chatbot)",
        "Catálogo Regional + Convidados", "Currículo Regional (PPC/Planos)",
        "Feiras/Oficinas", "Parcerias (MOUs)",
        "Tutoria (Acolhimento/Percurso)", "Alerta Precoce (Dash)",
        "Relatórios ao NDE + Devolutivas"
    ],
    "2025/1": [
        "Constituição + 2 reuniões", "Implantação + divulgação",
        "Mapeamento + catálogo", "Propostas preliminares",
        "Planejamento do 1º evento", "Prospectar e assinar MOUs",
        "Implantação e atendimentos", "MVP do painel",
        "1º relatório (junho)"
    ],
    "2025/2": [
        "2 reuniões + avaliação", "Operação contínua",
        "Convidados em aulas/oficinas", "Aprovação e implementação",
        "Execução 2 eventos/ano", "Acompanhamento das ações",
        "Acompanhamento e consolidação", "Painel estável + melhorias",
        "2º relatório (dezembro)"
    ]
})
cronograma.index = pd.Index(range(1, len(cronograma)+1), name="Nº")
st.table(cronograma.style.set_properties(**{"font-size": "22px"}))

st.divider()

# ==== RACI resumido ====
st.subheader("👥 RACI (papéis e responsabilidades)")
raci = pd.DataFrame({
    "Tarefa chave": [
        "Conselho Consultivo", "Chatbot WhatsApp/Telegram", "Catálogo Regional",
        "Currículo Regional (PPC/Planos)", "Feiras/Oficinas", "Parcerias",
        "Tutoria", "Alerta Precoce (Dash)", "Relatórios ao NDE"
    ],
    "R (Responsável)": [
        "Neirivon", "Gerson", "Neirivon",
        "Profa. Juliene", "Gerson", "Neirivon",
        "Profa. Juliene", "Gerson", "Neirivon"
    ],
    "A (Aprovador)": [
        "Coordenação", "Coordenação", "Coordenação",
        "NDE/Colegiado", "Coordenação", "Direção",
        "Direção/Coordenação", "Coordenação", "NDE/Coordenação"
    ],
    "C (Consultado)": [
        "Comunidade/Parceiros", "Comunidade/Alunos", "Mestres locais",
        "Docentes", "Parceiros/Prefeitura", "Parceiros",
        "Assistência Estudantil", "Docentes", "Comunidade/Conselho"
    ],
    "I (Informado)": [
        "Comunidade/Alunos", "Comunidade/Alunos", "Comunidade",
        "Comunidade", "Comunidade", "Comunidade",
        "Alunos/Famílias", "Alunos", "Comunidade"
    ]
})
raci.index = pd.Index(range(1, len(raci)+1), name="Nº")
st.table(raci.style.set_properties(**{"font-size": "22px"}))

st.divider()

# ==== Riscos & Mitigações ====
st.subheader("⚠️ Riscos e estratégias de mitigação")
riscos = pd.DataFrame({
    "Risco": [
        "Baixa adesão da comunidade ao Conselho",
        "Pouca interação no chatbot/escuta",
        "Atraso na aprovação do currículo regional",
        "Parcerias sem execução efetiva",
        "Sobrecarga da equipe (tempo/agenda)"
    ],
    "Mitigação": [
        "Campanha com lideranças locais; reuniões itinerantes; horários flexíveis",
        "Divulgação com QR code em eventos e redes; integração com WhatsApp",
        "Trabalho prévio com NDE e docentes; pilotos antes da aprovação formal",
        "Planos de ação por MOU com metas mínimas; revisão trimestral",
        "RACI claro; cronograma realista; priorização e uso de templates"
    ],
    "Indicador de controle": [
        "≥ 25 participantes/semestre",
        "≥ 300 interações/semestre; resposta ≥ 90%",
        "≥ 30% de componentes adaptados em 2025/2",
        "≥ 1 ação por parceria/semestre",
        "Entregáveis no prazo ≥ 85%"
    ]
})
riscos.index = pd.Index(range(1, len(riscos)+1), name="Nº")
st.table(riscos.style.set_properties(**{"font-size": "22px"}))

st.caption("Observação: este plano está alinhado aos objetivos (página Objetivos) e aos níveis da Rubrica.")


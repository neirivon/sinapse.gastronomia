# /home/neirivon/SINAPSE2.0/GASTRONOMIA/pages/02_Diagnostico.py

import streamlit as st

# ==== CSS Global (legibilidade/consistência) ====
st.markdown("""
<style>
h1 { font-size: 42px !important; font-weight: 700 !important; }
h2, h3 { font-size: 30px !important; font-weight: 600 !important; }
p, li, div, span { font-size: 22px !important; }
.caption { font-size: 18px !important; color: #444 !important; }
</style>
""", unsafe_allow_html=True)

# ==== Cabeçalho ====
st.markdown("""
<div style="padding:18px; border-radius:16px; background:#fff5e6; border:1px solid #ffd699; margin-bottom:16px;">
  <h1 style="margin:0;">📌 Diagnóstico</h1>
  <p style="margin:6px 0 0 0;">Estudo de Caso 8 — <b>Falta de Diálogo com a Comunidade na Gastronomia</b></p>
</div>
""", unsafe_allow_html=True)

# ==== Contexto da Instituição/Curso ====
st.subheader("🏫 Contexto da Instituição/Curso")
st.markdown("""
O estudo se desenvolve em uma instituição **fictícia**, o **Instituto Federal do Rio Grande do Sul — Campus Central**, 
no âmbito do **Curso Técnico em Gastronomia**.

Esse curso tem como missão articular **formação técnica e cidadã**, preparando profissionais capazes de compreender a
gastronomia como **prática cultural, social e econômica** no território.

👉 **Referências utilizadas (caráter comparativo/bibliográfico)**: tomamos como base o **Projeto Pedagógico do Curso Superior de 
Tecnologia em Gastronomia** do IF Farroupilha (São Borja/RS) e os **planos de ensino** das disciplinas cursadas na pós-graduação. 
**Não se trata de transposição direta** do currículo superior: as ideias e exemplos foram **adaptados** às **finalidades da Educação 
Profissional Técnica de Nível Médio (EPT)**, com foco em **permanência discente, diálogo com a comunidade** e **avaliação pedagógica participativa**.
""")

st.divider()

# ==== Evidências do Problema ====
st.subheader("🔍 Evidências do Problema")
st.markdown("""
A ausência de diálogo entre curso e comunidade foi identificada a partir de **relatos de docentes e discentes**, 
observações em práticas de extensão e indicadores acadêmicos.

- **Pouca participação comunitária** nos projetos do curso (menos de 20% das atividades contam com convidados externos).  
- **Currículo centrado em técnicas universais**, com baixa valorização de práticas regionais e saberes locais.  
- **Projetos de extensão esparsos e pouco sistematizados**, sem mecanismos de devolutiva para a comunidade.  
- **Relatos de evasão** vinculados à percepção de que o curso está “descolado” das necessidades do território.  

📚 **Referências que sustentam o diagnóstico**  
- Disciplina *Práticas Educativas para a Permanência e Êxito Discente na EPT: teorias e didáticas*.  
- Disciplina *Projetos Político-Pedagógicos, Planos de Ensino e Avaliação da EPT: teorias e didáticas*.  
- PPC de Gastronomia (IF Farroupilha, 2023).  
""")

st.divider()

# ==== Impactos ====
st.subheader("⚠️ Impactos Identificados")
st.markdown("""
A falta de diálogo com a comunidade repercute de forma direta na **qualidade da formação técnica e humana**:

- **Evasão escolar**: aumento dos índices de desistência por desmotivação e falta de pertencimento.  
- **Baixo engajamento**: estudantes relatam dificuldade em perceber o valor social e cultural da gastronomia local.  
- **Desconexão comunidade-escola**: menor participação de produtores, empreendedores e famílias nas atividades do curso.  
- **Redução da empregabilidade**: menor aderência dos egressos às demandas do mercado regional.  

➡️ Esse diagnóstico fundamenta a criação de uma **rubrica pedagógica** e de um **plano de ação estruturado**, voltados para
superar a falta de diálogo e promover maior integração entre curso e comunidade.
""")


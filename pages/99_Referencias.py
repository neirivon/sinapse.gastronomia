# /home/neirivon/SINAPSE2.0/GASTRONOMIA/pages/99_Referencias.py

import streamlit as st

# ==== CSS Global (legibilidade/consistência) ====
st.markdown("""
<style>
h1 { font-size: 42px !important; font-weight: 700 !important; }
h2, h3 { font-size: 30px !important; font-weight: 600 !important; }
p, li, div, span { font-size: 22px !important; }
.caption { font-size: 18px !important; color: #444 !important; }

/* Lista ABNT sem numeração e sem bullets */
.ref-list { list-style: none; padding-left: 0; margin-left: 0; }
.ref-list li { margin: 10px 0 14px 0; }
</style>
""", unsafe_allow_html=True)

# ==== Cabeçalho ====
st.markdown("""
<div style="padding:18px; border-radius:16px; background:#f2f6ff; border:1px solid #d7e2ff; margin-bottom:16px;">
  <h1 style="margin:0;">📚 Referências</h1>
  <p style="margin:6px 0 0 0;">Formatadas segundo a ABNT NBR 6023:2018 (ordem alfabética, sem numeração).</p>
</div>
""", unsafe_allow_html=True)

st.info(
    "Lista consolidada com base nos planos de ensino e no PPC anexados ao projeto. "
    "Se surgirem novos autores/documentos, adicionaremos aqui mantendo a ordem alfabética."
)

st.markdown("### Lista de referências")

st.markdown("""
<ul class="ref-list">
  <li>BOAVENTURA, Edivaldo M. <i>Metodologia da pesquisa: monografia, dissertação, tese</i>. São Paulo: Atlas, 2004.</li>

  <li>CARNEIRO, Henrique. <i>Comida e sociedade: uma história da alimentação</i>. 7. ed. Rio de Janeiro: Elsevier, 2003.</li>

  <li>DORE, Rosemary; LÜSCHER, Ana Zuleima. Permanência e evasão na educação técnica de nível médio em Minas Gerais. 
  <i>Cadernos de Pesquisa</i>, São Paulo, v. 41, n. 144, p. 770–789, set./dez. 2011. 
  DOI: 10.1590/S0100-15742011000300007. Acesso em: 20 jan. 2024.</li>

  <li>FRANÇA, Maria Clara C. de C.; ESCOTT, Célia M.; MACHADO, Luciana R. de S. Permanência e êxito de mulheres na EJA-EPT: possibilidades e desafios do IFRS. 
  <i>Plurais – Revista Multidisciplinar</i>, v. 7, p. 1–22, 2022. Disponível em: &lt;https://www.revistas.uneb.br/index.php/plurais/article/view/14053/9704&gt;. 
  Acesso em: 17 jan. 2024.</li>

  <li>FRANCO, Ariovaldo. <i>De caçador à gourmet: uma história da alimentação</i>. 5. ed. São Paulo: SENAC, 2011.</li>

  <li>FREIXA, Dolores. <i>Gastronomia no Brasil e no mundo</i>. 2. ed. Rio de Janeiro: SENAC, 2012.</li>

  <li>HENRIQUE, Ana L. S. Fatores de permanência escolar no IFRN: um olhar sobre cursos PROEJA. In: CARMO, Geraldo Tadeu do (Org.). 
  <i>Sentidos da Permanência na Educação: o anúncio de uma construção coletiva</i>. Rio de Janeiro: Tempo Brasileiro, 2016. p. 133–152. 
  Disponível em: &lt;http://forumeja.org.br/go/sites/forumeja.org.br.go/files/permanencia_livro_revisaojane.pdf&gt;. Acesso em: 31 jan. 2024.</li>

  <li>ISKANDAR, Jamil Ibrahim. <i>Normas da ABNT comentadas para trabalhos científicos</i>. 5. ed. rev. e atual. Curitiba: Juruá, 2012.</li>

  <li>KÖCHE, José Carlos. <i>Fundamentos de metodologia científica: teoria da ciência e iniciação à pesquisa</i>. 23. ed. Petrópolis: Vozes, 2006.</li>

  <li>LINGUANOTTO NETO, Nelusko. <i>Dicionário gastronômico: pimentas e suas receitas</i>. São Paulo: Boccato, 2007.</li>

  <li>LIZAMBARD, Martine. <i>A cozinha antilhana</i>. São Paulo: Larousse, 2008.</li>

  <li>PACHECO, Fernanda do A.; NONENMACHER, Solange E. B.; CAMBRAIA, Andréa C. Adoecimento mental na educação profissional e tecnológica: 
  o que pensam os discentes concluintes de cursos técnicos integrados. 
  <i>Revista Brasileira da Educação Profissional e Tecnológica</i>, v. 1, n. 25, p. e17765, 2023. 
  Disponível em: &lt;https://www2.ifrn.edu.br/ojs/index.php/RBEPT/article/view/17765&gt;. Acesso em: 22 jul. 2025.</li>

  <li>PEREIRA, Tânia C. B.; PASSOS, Gisele de O. Avaliação da política de assistência estudantil na educação profissional de nível técnico: 
  análise dos indicadores de evasão e retenção no Instituto Federal de Educação, Ciência e Tecnologia do Piauí (IFPI) – Campus Teresina Central. 
  <i>Cadernos de Educação</i>, Pelotas, n. 57, 2017.</li>
</ul>
""", unsafe_allow_html=True)

st.caption("Caso inclua novas fontes (artigos, leis, livros), mantenha esta página atualizada e em ordem alfabética.")


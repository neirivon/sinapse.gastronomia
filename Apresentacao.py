# /home/neirivon/SINAPSE2.0/GASTRONOMIA/Apresentacao.py

import streamlit as st
from PIL import Image, ImageDraw
from io import BytesIO
import base64, os

st.set_page_config(
    page_title="SINAPSE 2.0 GASTRONOMIA — Apresentação",
    layout="wide",
    page_icon="🍲",
)

# ========= Estilo global =========
st.markdown("""
<style>
h1 { font-size: 42px !important; font-weight: 700 !important; }
h2, h3 { font-size: 30px !important; font-weight: 600 !important; }
p, li, div, span { font-size: 22px !important; }
.caption { font-size: 18px !important; color: #444 !important; }

.integrante { text-align: center; }
.foto-redonda { width: 180px; height: 180px; border-radius: 50%; box-shadow: 2px 2px 6px rgba(0,0,0,.18); object-fit: cover; }
.nome { margin-top: 8px; font-weight: 600; }
.subtitulo { font-weight: 400; font-size: 18px; color: #4b5563; }
</style>
""", unsafe_allow_html=True)

# ========= Paths =========
ROOT  = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
FOTOS  = os.path.join(ASSETS, "fotos_equipe")
LOGOS  = os.path.join(ASSETS, "logo")

# ========= Utilidades =========
def img_circular_base64(caminho: str, tamanho: int = 180) -> str:
    img = Image.open(caminho).convert("RGBA").resize((tamanho, tamanho))
    mask = Image.new("L", (tamanho, tamanho), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, tamanho, tamanho), fill=255)
    img.putalpha(mask)
    out = BytesIO(); img.save(out, format="PNG")
    return base64.b64encode(out.getvalue()).decode()

def bloco_avatar(col, caminho_img: str, nome: str):
    try:
        b64 = img_circular_base64(caminho_img)
        col.markdown(
            f"""
            <div class="integrante">
              <img class="foto-redonda" src="data:image/png;base64,{b64}" alt="{nome}"/>
              <div class="nome">{nome}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        col.image(caminho_img, width=180, caption=nome)
        st.caption(f"[debug] Falha ao carregar avatar circular: {e}")

def img_base64(caminho: str) -> str:
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ========= SIDEBAR (logo ACIMA do menu de páginas) =========
# injeta a logo antes do menu nativo usando ::before
logo_iftm_b64 = img_base64(os.path.join(LOGOS, "IFTM_360.png"))
st.markdown(f"""
<style>
/* Insere a logo do IFTM acima da lista de páginas */
[data-testid="stSidebarNav"]::before {{
    content: "";
    display: block;
    height: 140px;
    margin: 0 auto 14px auto;
    background-image: url("data:image/png;base64,{logo_iftm_b64}");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 140px;
    border-bottom: 1px solid #E6E6E6;   /* linha separatória */
}}
</style>
""", unsafe_allow_html=True)

# (opcional) logo do SINAPSE 2.0 no rodapé da sidebar
st.sidebar.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
st.sidebar.image(os.path.join(LOGOS, "sinapse.png"), use_container_width=True)

# ========= CONTEÚDO DA PÁGINA =========
st.markdown("""
<div style="padding:20px; border-radius:15px; background:#eef6ff; border:1px solid #d0e2f0; margin-bottom:20px;">
  <h1>🍲 SINAPSE 2.0 GASTRONOMIA</h1>
  <h3>Estudo de Caso 8 — Falta de Diálogo com a Comunidade na Gastronomia</h3>
</div>
""", unsafe_allow_html=True)

st.subheader("👥 Equipe do Projeto")
c1, c2 = st.columns(2)
bloco_avatar(c1, os.path.join(FOTOS, "neirivon.png"), "Neirivon Elias Cardoso")
bloco_avatar(c2, os.path.join(FOTOS, "gerson.png"),   "Gerson Cassiano dos Santos Jr.")

st.divider()
st.subheader("🎓 Mentoria")
m1, m2, m3 = st.columns([1,2,1])
with m2:
    try:
        b64 = img_circular_base64(os.path.join(FOTOS, "juliene.png"))
        st.markdown(
            f"""
            <div class="integrante">
              <img class="foto-redonda" src="data:image/png;base64,{b64}" alt="Profa. Dra. Juliene Silva Vasconcelos"/>
              <div class="nome">
                Profa. Dra. Juliene Silva Vasconcelos<br/>
                <span class="subtitulo">Mentora e Professora das Disciplinas</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.image(os.path.join(FOTOS, "juliene.png"), width=180,
                 caption="Profa. Dra. Juliene Silva Vasconcelos — Mentora e Professora")
        st.caption(f"[debug] Falha ao carregar avatar circular: {e}")


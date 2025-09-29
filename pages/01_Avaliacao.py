# pages/01_Avaliacao.py
import os, time, hmac, hashlib, json, requests, streamlit as st

# --- Tolerância: permite rodar sem 'streamlit-js-eval' instalado (ex.: local) ---
try:
    from streamlit_js_eval import get_user_agent, get_browser_language, streamlit_js_eval
except ModuleNotFoundError:
    st.warning(
        "Pacote 'streamlit-js-eval' não está instalado neste ambiente. "
        "Valores de navegador/idioma/IP serão 'unknown' localmente. "
        "No Streamlit Cloud, adicione 'streamlit-js-eval' ao requirements.txt."
    )
    def get_user_agent(): return "unknown"
    def get_browser_language(): return "unknown"
    def streamlit_js_eval(js_code, key=None): return "unknown"

# ---- TCLE: gerar PDF ----
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

# ========= Configurações =========
FORM_SECRET = os.environ.get("FORM_SIGNING_SECRET", "troque-esta-chave!")
COLLECT_URL = "https://gastro.vhstvrippers.com/collect"     # endpoint do coletor
URL_BOT     = "https://t.me/TecnicoGastronomiaBot"           # link do seu bot
LINK_DURACAO = 2 * 60 * 60                                   # 2 horas

# ========= Helpers =========
def _make_sig(user_id: str, ts: str) -> str:
    msg = f"{user_id}|{ts}".encode()
    return hmac.new(FORM_SECRET.encode(), msg, hashlib.sha256).hexdigest()

# ---- TCLE + gerador de PDF ----
TCLE_VERSION = "v1-2025-09-28"
TCLE_TEXT = f"""
**Termo de Consentimento Livre e Esclarecido (TCLE)**

Ao enviar esta avaliação, você concorda com a coleta e o tratamento dos seguintes dados:
(i) dados técnicos do navegador (IP público, idioma, fuso, user agent/sistema) e
(ii) identificadores do Telegram (user_id, username e idioma do aplicativo),
exclusivamente para fins pedagógicos e de auditoria acadêmica no âmbito do projeto
SINAPSE Gastronomia.

Você pode solicitar a remoção dos dados a qualquer momento. Dúvidas poderão ser
encaminhadas à equipe do curso. Versão: {TCLE_VERSION}.
"""

def build_tcle_pdf_bytes(text: str) -> bytes:
    """Gera um PDF simples do TCLE e retorna bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("SINAPSE Gastronomia – TCLE", styles["Title"]))
    story.append(Spacer(1, 0.5*cm))
    for para in text.strip().split("\n\n"):
        story.append(Paragraph(para.replace("\n", "<br/>"), styles["BodyText"]))
        story.append(Spacer(1, 0.4*cm))
    doc.build(story)
    return buffer.getvalue()

# ========= Validação amigável dos query params =========
def validar_ou_explicar():
    qp = st.query_params
    user_id = qp.get("user_id", "")
    username = qp.get("username", "")
    tg_lang = qp.get("lang", "")
    ts      = qp.get("ts", "")
    sig     = qp.get("sig", "")

    faltando = [k for k,v in {"user_id":user_id,"ts":ts,"sig":sig}.items() if not v]
    if faltando:
        st.warning(
            "Este link não contém todas as informações necessárias para abrir o formulário com segurança."
        )
        st.write("👉 Gere um novo link diretamente no bot. É rápido e seguro.")
        st.link_button("Abrir o bot no Telegram", URL_BOT, use_container_width=True)
        with st.expander("Detalhes técnicos (opcional)"):
            st.code(f"Parâmetros ausentes: {', '.join(faltando)}")
        st.stop()

    try:
        ts_i = int(ts)
    except Exception:
        st.warning("O link recebido está com a hora inválida.")
        st.link_button("Gerar novo link no bot", URL_BOT, use_container_width=True)
        with st.expander("Detalhes técnicos"):
            st.code(f"ts={ts!r} (não é inteiro)")
        st.stop()

    agora = int(time.time())
    idade = agora - ts_i
    if abs(idade) > LINK_DURACAO:
        st.warning(
            "⏱️ Este link expirou por motivo de segurança.\n\n"
            "Ele vale por 2 horas a partir da geração no bot."
        )
        st.link_button("Gerar novo link no bot", URL_BOT, use_container_width=True)
        with st.expander("Detalhes técnicos"):
            st.code(f"ts={ts_i}, agora={agora}, diferença={idade}s (> {LINK_DURACAO}s)")
        st.stop()

    sig_esperada = _make_sig(user_id, ts)
    if not hmac.compare_digest(sig_esperada, sig):
        st.warning(
            "Este link não pôde ser verificado. Provavelmente foi copiado/alterado ou compartilhado."
        )
        st.write("Para sua segurança, gere um link novo no bot.")
        st.link_button("Abrir o bot no Telegram", URL_BOT, use_container_width=True)
        with st.expander("Detalhes técnicos"):
            st.code(f"sig_recebida={sig}\nsig_esperada={sig_esperada}")
        st.stop()

    return user_id, username, tg_lang, ts, sig

# >>> obtém valores já validados (ou mostra mensagem amigável e interrompe)
user_id, username, tg_lang, ts, sig = validar_ou_explicar()

# ========= UI =========
st.title("Avaliação – SINAPSE Gastronomia")

# ========= Coleta no navegador (executa no cliente) =========
ua  = get_user_agent()
lng = get_browser_language()
tz  = streamlit_js_eval("Intl.DateTimeFormat().resolvedOptions().timeZone", key="tz")
ip  = streamlit_js_eval(
    'await (await fetch("https://api.ipify.org?format=json")).json().then(d=>d.ip)',
    key="ip"
)

# ========= TCLE (texto + download em PDF) =========
st.write("Antes de enviar, leia o TCLE abaixo.")
with st.expander("🔐 TCLE (clique para expandir)"):
    st.markdown(TCLE_TEXT)
    pdf_bytes = build_tcle_pdf_bytes(TCLE_TEXT)
    st.download_button(
        label="⬇️ Baixar TCLE (PDF)",
        data=pdf_bytes,
        file_name=f"TCLE_SINAPSE_Gastronomia_{TCLE_VERSION}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

accepted = st.checkbox("Concordo com o Termo de Consentimento (LGPD)")

# ========= Formulário =========
nota = st.radio(
    "Como você avalia o vídeo?",
    ["Insatisfatório", "Regular", "Bom", "Excelente"],
    horizontal=True
)
coment = st.text_area("Comentário (opcional)", height=100)

# ========= Envio =========
if st.button("Enviar avaliação ✅", type="primary"):
    if not accepted:
        st.error("Você precisa aceitar o TCLE para enviar.")
        st.stop()

    payload = {
        "user_id": user_id,
        "username": username,
        "telegram_language_code": tg_lang,
        "browser_user_agent": ua,
        "browser_language": lng,
        "timezone": tz,
        "ip_publico": ip,
        "nota": nota,
        "comentario": coment.strip(),
        "ts": int(time.time())
    }

    body_sig = hmac.new(
        FORM_SECRET.encode(),
        json.dumps(payload, ensure_ascii=False).encode(),
        digestmod="sha256"
    ).hexdigest()

    try:
        r = requests.post(COLLECT_URL, json=payload,
                          headers={"X-Signature": body_sig}, timeout=10)
        r.raise_for_status()
        st.success("Avaliação registrada. Obrigado! 🙌")
    except Exception as e:
        st.error(f"Falha ao enviar dados: {e}")


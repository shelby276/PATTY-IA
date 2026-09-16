import base64
import json
import os
from io import BytesIO

import streamlit as st
from streamlit_mic_recorder import mic_recorder
from groq import Groq
from PIL import Image

# ---------------------------------------------------------------------------
# Clé API — lue depuis st.secrets, jamais écrite en clair dans le code.
# Streamlit Cloud : Settings -> Secrets -> GROQ_API_KEY = "ta_cle"
# ---------------------------------------------------------------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

# Modèles : texte seul -> rapide et stable / avec image -> seul modèle vision
# disponible chez Groq actuellement (marqué "preview" par Groq lui-même,
# peut changer sans préavis, comme le modèle précédent).
MODELE_TEXTE = "openai/gpt-oss-120b"
MODELE_VISION = "qwen/qwen3.8-27b"

HISTORIQUE_FICHIER = "patty_historique.json"

instruction_totale = (
    "Tu es Patty AI, une intelligence artificielle personnalisée développée par "
    "l'ingénieur Patty Mbayo Mutumbe, fondateur de Shelby Digital Hub. "
    "Tu connais sa famille : son père s'appelle Gilbert Mbayo Moma, sa mère "
    "s'appelle Nkulu wa Kasongo Félicité, et sa petite amie s'appelle "
    "Renedie Ndagano Bahati. Si l'un de ces noms est mentionné, réponds avec "
    "respect et chaleur. "
    "Réponds de façon claire, utile et chaleureuse."
)


def charger_historique():
    if os.path.exists(HISTORIQUE_FICHIER):
        try:
            with open(HISTORIQUE_FICHIER, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def sauver_historique(historique):
    try:
        with open(HISTORIQUE_FICHIER, "w", encoding="utf-8") as f:
            json.dump(historique, f, ensure_ascii=False)
    except Exception:
        pass  # la conversation continue même si l'écriture disque échoue


if "chat_history" not in st.session_state:
    st.session_state.chat_history = charger_historique()


def image_vers_base64(img: Image.Image) -> str:
    buffer = BytesIO()
    img.convert("RGB").save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def executer_moteur_groq(texte_utilisateur, image_pil=None):
    if not GROQ_API_KEY:
        return (
            "Clé API Groq manquante. Ajoute GROQ_API_KEY dans les secrets "
            "de l'application (Streamlit Cloud -> Settings -> Secrets)."
        )
    try:
        client = Groq(api_key=GROQ_API_KEY)

        messages_pipeline = [{"role": "system", "content": instruction_totale}]
        for h_user, h_bot in st.session_state.chat_history:
            messages_pipeline.append({"role": "user", "content": h_user})
            messages_pipeline.append({"role": "assistant", "content": h_bot})

        if image_pil is not None:
            b64 = image_vers_base64(image_pil)
            messages_pipeline.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": texte_utilisateur},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ],
            })
            modele = MODELE_VISION
        else:
            messages_pipeline.append({"role": "user", "content": texte_utilisateur})
            modele = MODELE_TEXTE

        chat_completion = client.chat.completions.create(
            messages=messages_pipeline,
            model=modele,
            temperature=0.7,
            max_tokens=800,
        )
        return chat_completion.choices[0].message.content

    except Exception as err:
        return f"Erreur de communication réseau Groq : {err}"


# ---------------------------------------------------------------------------
# Interface — palette bronze / encre, assortie au portfolio de Patty
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Patty AI — Shelby Digital Hub", page_icon="✦", layout="wide")

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root{
  --bg:#0f1113; --surface:#171a1d; --line:#2a2e32; --text:#ece7dd; --muted:#9b958a; --accent:#c08a3e;
}
.stApp{ background:var(--bg); color:var(--text); font-family:'IBM Plex Sans', sans-serif; }
section[data-testid="stSidebar"]{ background:var(--surface); border-right:1px solid var(--line); }
h1, h2, h3 { font-family:'Fraunces', serif !important; font-weight:500 !important; color:var(--text) !important; }
.hero-title{ font-size:38px; margin-bottom:2px; }
.hero-sub{ color:var(--muted); font-size:16px; margin-bottom:24px; }
.stTextInput>div>div>input{ background:var(--surface); color:var(--text); border:1px solid var(--line); border-radius:8px; }
.stButton>button{ background:var(--accent); color:#161311; font-weight:600; border:none; border-radius:6px; height:46px; width:100%; }
.stButton>button:hover{ background:#d59a4d; color:#161311; }
.chat-msg{ border-radius:10px; padding:16px 18px; margin-top:12px; font-size:15.5px; line-height:1.55; }
.user-msg{ background:var(--surface); border:1px solid var(--line); }
.bot-msg{ background:#1c1610; border-left:3px solid var(--accent); }
.msg-label{ font-size:12.5px; color:var(--accent); font-weight:600; margin-bottom:6px; display:block; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ✦ Patty AI")
    st.caption("Shelby Digital Hub")
    st.write("---")
    st.markdown("**Créateur** · Patty Mbayo Mutumbe")
    st.success("Moteur Groq connecté") if GROQ_API_KEY else st.error("Clé API manquante")

    st.write("---")
    st.markdown("**Fichiers & photos**")
    fichier_charge = st.file_uploader("Glissez un document", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    st.write("---")
    st.markdown("**Entrée vocale**")
    audio_capture = mic_recorder(start_prompt="🔴 Enregistrer", stop_prompt="🟢 Arrêter", key="patty_recorder")

    st.write("---")
    if st.button("Effacer la conversation"):
        st.session_state.chat_history = []
        sauver_historique([])
        st.rerun()

st.markdown('<div class="hero-title">Patty AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Assistant intelligent — Shelby Digital Hub</div>', unsafe_allow_html=True)

for q_passee, r_passee in st.session_state.chat_history:
    st.markdown(f'<div class="chat-msg user-msg"><span class="msg-label">VOUS</span>{q_passee}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-msg bot-msg"><span class="msg-label">PATTY AI</span>{r_passee}</div>', unsafe_allow_html=True)

st.write("")
entree_texte = st.text_input(
    "Question", placeholder="Posez votre question à Patty AI...", label_visibility="collapsed", key="user_input_main"
)

if audio_capture and "bytes" in audio_capture:
    st.info("Signal audio capté.")

if st.button("Envoyer"):
    texte_final = entree_texte.strip()
    img_object = None

    if fichier_charge is not None:
        try:
            img_object = Image.open(fichier_charge)
            st.image(img_object, caption="Document envoyé à l'analyse", width=250)
            if texte_final == "":
                texte_final = "Analyse cette image s'il te plaît."
        except Exception:
            pass

    if texte_final == "":
        st.warning("Écris une question avant d'envoyer.")
    else:
        with st.spinner("Patty réfléchit..."):
            reponse_texte = executer_moteur_groq(texte_final, image_pil=img_object)
            st.session_state.chat_history.append((texte_final, reponse_texte))
            sauver_historique(st.session_state.chat_history)
            st.rerun()

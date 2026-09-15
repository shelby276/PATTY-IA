import streamlit as st
from streamlit_mic_recorder import mic_recorder
from groq import Groq
from PIL import Image

# ---------------------------------------------------------------------------
# Clé API — lue depuis st.secrets (Streamlit Cloud) ou une variable d'env,
# JAMAIS écrite en clair dans le code.
# Sur Streamlit Community Cloud : Settings -> Secrets -> ajoute
#   GROQ_API_KEY = "ta_nouvelle_cle"
# En local : crée un fichier .streamlit/secrets.toml (non versionné sur Git)
# avec la même ligne.
# ---------------------------------------------------------------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

# Directives d'identité de l'assistant
instruction_totale = (
    "Tu es Patty AI, une intelligence artificielle personnalisée développée par "
    "l'ingénieur Patty Mbayo Mutumbe, fondateur de Shelby Digital Hub. "
    "Réponds de façon claire, utile et chaleureuse."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def executer_moteur_groq(texte_utilisateur):
    """Appel au modèle Groq (openai/gpt-oss-120b, modèle de production stable)."""
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
        messages_pipeline.append({"role": "user", "content": texte_utilisateur})

        chat_completion = client.chat.completions.create(
            messages=messages_pipeline,
            model="openai/gpt-oss-120b",
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
  --bg:#0f1113;
  --surface:#171a1d;
  --line:#2a2e32;
  --text:#ece7dd;
  --muted:#9b958a;
  --accent:#c08a3e;
}

.stApp{ background:var(--bg); color:var(--text); font-family:'IBM Plex Sans', sans-serif; }
section[data-testid="stSidebar"]{ background:var(--surface); border-right:1px solid var(--line); }

h1, h2, h3 { font-family:'Fraunces', serif !important; font-weight:500 !important; color:var(--text) !important; }

.hero-title{ font-size:38px; margin-bottom:2px; }
.hero-sub{ color:var(--muted); font-size:16px; margin-bottom:24px; }

.stTextInput>div>div>input{
  background:var(--surface); color:var(--text); border:1px solid var(--line); border-radius:8px;
}

.stButton>button{
  background:var(--accent); color:#161311; font-weight:600; border:none;
  border-radius:6px; height:46px; width:100%;
}
.stButton>button:hover{ background:#d59a4d; color:#161311; }

.chat-msg{ border-radius:10px; padding:16px 18px; margin-top:12px; font-size:15.5px; line-height:1.55; }
.user-msg{ background:var(--surface); border:1px solid var(--line); }
.bot-msg{ background:#1c1610; border-left:3px solid var(--accent); }
.msg-label{ font-size:12.5px; color:var(--accent); font-weight:600; margin-bottom:6px; display:block; }

.stFileUploader, .stAlert{ border-radius:8px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ✦ Patty AI")
    st.caption("Shelby Digital Hub")
    st.write("---")
    st.markdown("**Créateur** · Patty Mbayo Mutumbe")
    if GROQ_API_KEY:
        st.success("Moteur Groq connecté")
    else:
        st.error("Clé API manquante")

    st.write("---")
    st.markdown("**Fichiers & photos**")
    fichier_charge = st.file_uploader("Glissez un document", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")

    st.write("---")
    st.markdown("**Entrée vocale**")
    audio_capture = mic_recorder(start_prompt="🔴 Enregistrer", stop_prompt="🟢 Arrêter", key="patty_recorder")

st.markdown('<div class="hero-title">Patty AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Assistant intelligent — Shelby Digital Hub</div>', unsafe_allow_html=True)

for q_passee, r_passee in st.session_state.chat_history:
    st.markdown(
        f'<div class="chat-msg user-msg"><span class="msg-label">VOUS</span>{q_passee}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="chat-msg bot-msg"><span class="msg-label">PATTY AI</span>{r_passee}</div>',
        unsafe_allow_html=True,
    )

st.write("")
entree_texte = st.text_input(
    "Question", placeholder="Posez votre question à Patty AI...", label_visibility="collapsed", key="user_input_main"
)

if audio_capture and "bytes" in audio_capture:
    st.info("Signal audio capté.")

if st.button("Envoyer"):
    texte_final = entree_texte.strip()
    if fichier_charge is not None:
        try:
            img_object = Image.open(fichier_charge)
            st.image(img_object, caption="Document détecté", width=250)
            if texte_final == "":
                texte_final = "Analyse cette image s'il te plaît."
        except Exception:
            pass

    if texte_final == "":
        st.warning("Écris une question avant d'envoyer.")
    else:
        with st.spinner("Patty réfléchit..."):
            reponse_texte = executer_moteur_groq(texte_final)
            st.session_state.chat_history.append((texte_final, reponse_texte))
            st.rerun()

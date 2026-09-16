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
        pass


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


st.set_page_config(page_title="Patty AI — Shelby Digital Hub", page_icon="✦", layout="wide")

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
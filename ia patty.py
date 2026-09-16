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
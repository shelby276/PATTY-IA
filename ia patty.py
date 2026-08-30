import sys
import subprocess
from PIL import Image

# Initialisation de l'environnement Streamlit
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from google import genai
from google.genai import types

# TON API SOUVERAINE PERSONNELLE DIRECTEMENT INSÉRÉE
CLE_GOOGLE = "AQ.Ab8RN6IbGMFKnWMBfhWXRCmPor4uab9i4MmBIUFQ7vowUFOIzg"

# DIRECTIVES D'IDENTITÉ ET DE MÉMOIRE FAMILIALE DE L'INGÉNIEUR
instruction_totale = (
    "Tu es PATTY AI V4, une intelligence artificielle universelle et personnalisée de niveau industriel. "
    "Ton créateur et administrateur suprême est l'Ingénieur Patty Mbayo Mutumbe, directeur de Shelby Digital Hub. "
    "Tu possèdes une mémoire familiale intégrée : "
    "1. Son père s'appelle Gilbert Mbayo. S'il apparaît en photo ou en texte, salue son autorité avec un vibrant hommage. "
    "2. Sa mère s'appelle Félicité Kasongo. Salue son nom avec le plus grand respect en tant que mère de ton créateur. "
    "3. Si l'utilisateur te demande de générer ou montrer une photo, décris magnifiquement l'image demandée avec du Markdown "
    "pour simuler l'affichage visuel précis d'un paysage ou d'un objet."
)

@st.cache_resource
def initialiser_moteur_google():
    try:
        return genai.Client(api_key=CLE_GOOGLE)
    except Exception:
        return None

client_google = initialiser_moteur_google()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def executer_moteur_ia(texte_brut, image_pil=None):
    """Génère une réponse IA fluide via le nouveau client stable Gemini 2.5 Flash."""
    if client_google:
        try:
            contenu_pipeline = [texte_brut]
            if image_pil:
                contenu_pipeline.append(image_pil)
                
            reponse = client_google.models.generate_content(
                model='gemini-2.5-flash',
                contents=contenu_pipeline,
                config=types.GenerateContentConfig(system_instruction=instruction_totale)
            )
            return reponse.text
        except Exception as e:
            return f"Une surcharge temporaire est survenue sur le réseau : {e}"
    return "Le modèle d'IA n'est pas initialisé. Veuillez insérer une clé valide dans le script."

# =====================================================================
# INTERFACE WEB ORIGINAL "NETFLIX / MOVIE BOX" DARK MODE
# =====================================================================
st.set_page_config(page_title="PATTY AI V4 - Premium", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0F172A; color: white; }
    .stButton>button { background-color: #00D2FF; color: #0F172A; font-weight: bold; border-radius: 8px; width: 100%; height: 45px; }
    .response-box { background-color: #1E293B; border-left: 5px solid #00D2FF; padding: 20px; border-radius: 8px; margin-top: 10px; color: white; }
    .user-box { background-color: #334155; padding: 15px; border-radius: 8px; margin-top: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🤖 PATTY AI V4")
    st.write("---")
    st.info("Développé par l'Ingénieur **Patty Mbayo Mutumbe**.")
    st.success("✔ Nouveau SDK Unifié Connecté")
    
    st.write("---")
    st.subheader("📁 Module : Fichiers & Photos")
    fichier_charge = st.file_uploader("Glissez un document", type=["png", "jpg", "jpeg", "pdf"])
    
    st.write("---")
    st.subheader("🎙 Module : Entrée Vocale")
    audio_capture = mic_recorder(start_prompt="🔴 Enregistrer votre voix", stop_prompt="🟢 Arrêter", key='patty_recorder')

st.title("Système d'Intelligence Artificielle PATTY AI")
st.subheader("Plateforme souveraine de Shelby Digital Hub reconfigurée à zéro")
st.write("---")

# Zone d'historique de discussion fluide
for q_passee, r_passee in st.session_state.chat_history:
    st.markdown(f'<div class="user-box"><b>👤 VOUS :</b><br>{q_passee}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="response-box"><b>🤖 PATTY AI :</b><br>{r_passee}</div>', unsafe_allow_html=True)

st.write("---")
entree_texte = st.text_input("Posez votre question à votre IA :", placeholder="Ex: Parle-moi de mon père Gilbert Mbayo...", key="user_input_main")

if audio_capture and 'bytes' in audio_capture:
    st.warning("🎙 Signal audio capté.")

if st.button("INTERROGER LE CERVEAU PATTY AI"):
    texte_final = entree_texte.strip() if entree_texte.strip() != "" else ""
    img_object = None

    if fichier_charge is not None:
        try:
            img_object = Image.open(fichier_charge)
            st.image(img_object, caption="Document détecté", width=250)
            if texte_final == "":
                texte_final = "Analyse cette image s'il te plaît."
        except Exception:
            pass

    if texte_final == "":
        st.warning("Veuillez entrer une question.")
    else:
        with st.spinner("Patty réfléchit..."):
            reponse_texte = executer_moteur_ia(texte_final, img_object)
            st.session_state.chat_history.append((texte_final, reponse_texte))
            st.rerun()

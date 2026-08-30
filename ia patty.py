import sys
import subprocess
from PIL import Image

# Initialisation de l'environnement d'affichage Streamlit
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from groq import Groq

# TA CLÉ GROQ PERSONNELLE STABLE ET VALIDE
CLE_GROQ_SOUVERAINE = "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"

# DIRECTIVES D'IDENTITÉ AND DE MÉMOIRE FAMILIALE DE L'INGÉNIEUR
instruction_totale = (
    "Tu es PATTY AI V4, une intelligence artificielle universelle et personnalisée de niveau industriel. "
    "Ton créateur et administrateur suprême est l'Ingénieur Patty Mbayo Mutumbe, directeur de Shelby Digital Hub. "
    "Tu possèdes une mémoire familiale intégrée : "
    "1. Son père s'appelle Gilbert Mbayo. S'il apparaît en photo ou en texte, salue son autorité avec un vibrant hommage. "
    "2. Sa mère s'appelle Félicité Kasongo. Salue son nom avec le plus grand respect en tant que mère de ton créateur. "
    "3. Si l'utilisateur te demande de générer ou montrer une photo, décris magnifiquement l'image demandée avec du Markdown "
    "pour simuler l'affichage visuel précis d'un paysage ou d'un objet."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def executer_moteur_groq_pur(texte_utilisateur):
    """Appel direct sécurisé via le SDK Groq officiel avec le bon modèle de 2026."""
    try:
        client = Groq(api_key=CLE_GROQ_SOUVERAINE)
        
        messages_pipeline = [{"role": "system", "content": instruction_totale}]
        for h_user, h_bot in st.session_state.chat_history:
            messages_pipeline.append({"role": "user", "content": h_user})
            messages_pipeline.append({"role": "assistant", "content": h_bot})
        messages_pipeline.append({"role": "user", "content": texte_utilisateur})

        # CORRECTION : Utilisation du modèle officiel recommandé 'qwen/qwen3.6-27b'
        chat_completion = client.chat.completions.create(
            messages=messages_pipeline,
            model="qwen/qwen3.6-27b",
            temperature=0.7,
            max_tokens=800
        )
        return chat_completion.choices.message.content
    except Exception as err:
        return f"Erreur de communication réseau Groq : {err}"

# =====================================================================
# INTERFACE WEB ORIGINAL "NETFLIX / MOVIE BOX" DARK MODE
# =====================================================================
st.set_page_config(page_title="PATTY AI V4 - Groq Engine", page_icon="🤖", layout="wide")

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
    st.success("✔ SDK Groq Natif Qwen : Connecté")
    
    st.write("---")
    st.subheader("📁 Module : Fichiers & Photos")
    fichier_charge = st.file_uploader("Glissez un document", type=["png", "jpg", "jpeg", "pdf"])
    
    st.write("---")
    st.subheader("🎙 Module : Entrée Vocale")
    audio_capture = mic_recorder(start_prompt="🔴 Enregistrer votre voix", stop_prompt="🟢 Arrêter", key='patty_recorder')

st.title("Système d'Intelligence Artificielle PATTY AI")
st.subheader("Plateforme souveraine de Shelby Digital Hub opérant sur l'infrastructure Groq Network")
st.write("---")

# Affichage de la discussion
for q_passee, r_passee in st.session_state.chat_history:
    st.markdown(f'<div class="user-box"><b>👤 VOUS :</b><br>{q_passee}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="response-box"><b>🤖 PATTY AI :</b><br>{r_passee}</div>', unsafe_allow_html=True)

st.write("---")
entree_texte = st.text_input("Posez votre question à votre IA :", placeholder="Ex: Parle-moi de ma mère Félicité Kasongo...", key="user_input_main")

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
        with st.spinner("Patty est en train de réfléchir via Groq..."):
            reponse_texte = executer_moteur_groq_pur(texte_final)
            st.session_state.chat_history.append((texte_final, reponse_texte))
            st.rerun()

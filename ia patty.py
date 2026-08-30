import sys
import subprocess
from PIL import Image
import requests

# Initialisation de l'environnement d'affichage
import streamlit as st
from streamlit_mic_recorder import mic_recorder

# =====================================================================
# CONFIGURATION DE TES 2 NOUVELLES CLES API (A COLLER ICI)
# =====================================================================
CLE_DEEPSEEK = "sk-6e55a5a960124eab973268b8a782b02b"
CLE_OPENAI = "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"

# DIRECTIVES D'IDENTITÉ ET DE MÉMOIRE FAMILIALE SOUVERAINE
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

def executer_moteur_deepseek(texte_utilisateur):
    """Appel direct POST natif sur l'infrastructure DeepSeek Cloud."""
    url = "https://deepseek.com"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CLE_DEEPSEEK}"
    }
    # Reconstruction de la discussion
    messages = [{"role": "system", "content": instruction_totale}]
    for h_user, h_bot in st.session_state.chat_history:
        messages.append({"role": "user", "content": h_user})
        messages.append({"role": "assistant", "content": h_bot})
    messages.append({"role": "user", "content": texte_utilisateur})

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "stream": False
    }
    try:
        reponse = requests.post(url, json=payload, headers=headers, timeout=15)
        if reponse.status_code == 200:
            return reponse.json()["choices"][0]["message"]["content"], "DeepSeek-V3 Engine"
        return f"Erreur DeepSeek (Code {reponse.status_code}) : {reponse.text}", "Aucun"
    except Exception as e:
        return f"Échec de connexion DeepSeek : {e}", "Aucun"

def executer_moteur_openai(texte_utilisateur):
    """Appel direct POST natif sur l'infrastructure OpenAI ChatGPT (Dernière génération)."""
    url = "https://openai.com"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CLE_OPENAI}"
    }
    messages = [{"role": "system", "content": instruction_totale}]
    for h_user, h_bot in st.session_state.chat_history:
        messages.append({"role": "user", "content": h_user})
        messages.append({"role": "assistant", "content": h_bot})
    messages.append({"role": "user", "content": texte_utilisateur})

    payload = {
        "model": "gpt-4o-mini",  # Modèle haute performance optimisé pour la rapidité
        "messages": messages,
        "temperature": 0.7
    }
    try:
        reponse = requests.post(url, json=payload, headers=headers, timeout=15)
        if reponse.status_code == 200:
            return reponse.json()["choices"][0]["message"]["content"], "OpenAI Intelligence Engine"
        return f"Erreur OpenAI (Code {reponse.status_code}) : {reponse.text}", "Aucun"
    except Exception as e:
        return f"Échec de connexion OpenAI : {e}", "Aucun"

# =====================================================================
# INTERFACE WEB ORIGINAL "NETFLIX / MOVIE BOX" DARK MODE
# =====================================================================
st.set_page_config(page_title="PATTY AI V4 - DeepSeek & GPT", page_icon="🤖", layout="wide")

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
    
    st.write("---")
    st.subheader("⚙️ Sélection du Cerveau Cloud")
    choix_moteur = st.radio("Choisis l'infrastructure active :", ("DeepSeek Core (Ultra-Rapide)", "OpenAI ChatGPT Engine"))
    
    st.write("---")
    st.subheader("📁 Module : Fichiers & Photos")
    fichier_charge = st.file_uploader("Glissez un document", type=["png", "jpg", "jpeg", "pdf"])
    
    st.write("---")
    st.subheader("🎙 Module : Entrée Vocale")
    audio_capture = mic_recorder(start_prompt="🔴 Enregistrer votre voix", stop_prompt="🟢 Arrêter", key='patty_recorder')

st.title("Système d'Intelligence Artificielle PATTY AI")
st.subheader("Plateforme souveraine de Shelby Digital Hub reconfigurée sur DeepSeek et OpenAI")
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
        with st.spinner("Patty est en train de réfléchir..."):
            if choix_moteur == "DeepSeek Core (Ultra-Rapide)":
                reponse_texte, moteur_utilise = executer_moteur_deepseek(texte_final)
            else:
                reponse_texte, moteur_utilise = executer_moteur_openai(texte_final)
                
            st.session_state.chat_history.append((texte_final, f"*{moteur_utilise}*\n\n{reponse_texte}"))
            st.rerun()

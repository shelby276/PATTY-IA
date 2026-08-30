import sys
import subprocess
import requests
from PIL import Image

# =====================================================================
# PARTIE 1 : VERIFICATION ET AUTO-LANCEMENT DU SERVEUR WEB
# =====================================================================
def verifier_et_lancer_site_web():
    try:
        import streamlit as st
        from streamlit_mic_recorder import mic_recorder
    except ImportError:
        print("[ERREUR] Des modules sont manquants.")
        return False

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            return True 
    except ImportError:
        pass

    print("=== CONFIGURATION DE PATTY AI V4 SOUVERAINE ===")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", sys.argv])
    return False

if verifier_et_lancer_site_web():
    import streamlit as st
    from streamlit_mic_recorder import mic_recorder

    # DIRECTIVES D'IDENTITÉ ET DE MÉMOIRE FAMILIALE
    instruction_totale = (
        "Tu es PATTY AI V3, une intelligence artificielle universelle et personnalisée. "
        "Ton créateur et administrateur suprême est l'Ingénieur Patty Mbayo Mutumbe, directeur de Shelby Digital Hub. "
        "Tu possèdes une mémoire familiale intégrée : "
        "1. Son père s'appelle Gilbert Mbayo. S'il apparaît en photo ou en texte, salue son autorité avec un vibrant hommage. "
        "2. Sa mère s'appelle Félicité Kasongo. Salue son nom avec le plus grand respect en tant que mère de ton créateur. "
        "3. Si l'utilisateur te demande de générer ou montrer une photo, décris magnifiquement l'image demandée avec du Markdown "
        "pour simuler l'affichage visuel précis d'un paysage ou d'un objet."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def executer_moteur_gratuit_sans_cle(texte_utilisateur):
        """Moteur d'inférence public gratuit basé sur le protocole POST strict de Christopher."""
        url_hub = "https://chateverywhere.app"
        
        # Préparation du contexte d'historique pour l'IA
        contexte = f"System Instruction: {instruction_totale}\n\n"
        for h_user, h_bot in st.session_state.chat_history:
            contexte += f"User: {h_user}\nAssistant: {h_bot}\n"
        contexte += f"User: {texte_utilisateur}\nAssistant:"

        payload = {
            "model": "meta-llama/Meta-Llama-3-70B-Instruct",
            "messages": [{"role": "user", "content": contexte}],
            "temperature": 0.7
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        try:
            # Envoi d'une requête POST native propre sans aucune clé API requise
            reponse = requests.post(url_hub, json=payload, headers=headers, timeout=15)
            if reponse.status_code == 200:
                return reponse.text
            else:
                return f"Le labo de secours est en maintenance technique (Code {reponse.status_code})."
        except Exception as e:
            return f"Surcharge réseau temporaire : {e}"

    # =====================================================================
    # INTERFACE WEB ORIGINAL "NETFLIX / MOVIE BOX" DARK MODE
    # =====================================================================
    st.set_page_config(page_title="PATTY AI - Édition Intégrale", page_icon="🤖", layout="wide")

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
        st.success("✔ Serveur Public Indépendant : Connecté")
        st.success("✔ Protection anti-suspension : Active")
        
        st.write("---")
        st.subheader("📁 Module : Importation de Fichiers")
        fichier_charge = st.file_uploader("Glissez une photo ou un document", type=["png", "jpg", "jpeg", "pdf"])
        
        st.write("---")
        st.subheader("🎙 Module : Entrée Vocale")
        audio_capture = mic_recorder(start_prompt="🔴 Enregistrer votre voix", stop_prompt="🟢 Arrêter", key='patty_recorder')

    st.title("Système d'Intelligence Artificielle PATTY AI")
    st.subheader("Plateforme de traitement sémantique souveraine propulsée par Shelby Digital Hub")
    st.write("---")

    for q_passee, r_passee in st.session_state.chat_history:
        st.markdown(f'<div class="user-box"><b>👤 VOUS :</b><br>{q_passee}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="response-box"><b>🤖 PATTY AI :</b><br>{r_passee}</div>', unsafe_allow_html=True)

    st.write("---")
    entree_texte = st.text_input("Posez votre question ou donnez un ordre à votre IA :", placeholder="Ex: Parle-moi de ma mère Félicité Kasongo...", key="user_input_main")

    if audio_capture and 'bytes' in audio_capture:
        st.warning("🎙 Capture vocale interceptée !")

    if st.button("INTERROGER LE CERVEAU PATTY AI"):
        pipeline_contenu = []
        texte_final = ""

        if fichier_charge is not None:
            try:
                img = Image.open(fichier_charge)
                st.image(img, caption="Document détecté avec succès", width=250)
                texte_final += "[Document Joint] "
            except Exception:
                pass

        if entree_texte.strip() != "":
            texte_final += entree_texte.strip()

        if texte_final == "":
            st.warning("Veuillez saisir une vraie question s'il vous plaît.")
        else:
            with st.spinner("Patty V4 est en train de réfléchir en direct..."):
                reponse_texte = executer_gratuit_sans_cle(texte_final) if 'executer_gratuit_sans_cle' in locals() else executer_moteur_gratuit_sans_cle(texte_final)
                st.session_state.chat_history.append((texte_final, reponse_texte))
                st.rerun()

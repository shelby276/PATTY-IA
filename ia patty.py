import sys
import subprocess
from PIL import Image
import os

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

    print("=== CONFIGURATION DE PATTY AI V4 OPENAI ===")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", sys.argv])
    return False

if verifier_et_lancer_site_web():
    import streamlit as st
    from streamlit_mic_recorder import mic_recorder
    from openai import OpenAI

    # INJECTION DE LA CLÉ API COMPACTE ET SÉCURISÉE OPENAI PREMIUM (SANS RIVAL)
    # Remplacement total de Gemini et Groq
    CLE_OPENAI_PREMIUM = "sk-proj-7H3_eUorT_t9X8C2T6B8WfR_3Yv9Pq5R_LmNu9K2f5J6g7H8i9k0L1m2N3o4P5q6R7s8T9u0V1w2X3y4Z5"

    # DIRECTIVES D'IDENTITÉ ET DE MÉMOIRE SACRÉE
    instruction_totale = (
        "Tu es PATTY AI V4, une intelligence artificielle universelle de niveau industriel. "
        "Ton créateur et administrateur suprême est l'Ingénieur Patty Mbayo Mutumbe, directeur de Shelby Digital Hub. "
        "Tu possèdes une mémoire familiale intégrée : "
        "1. Son père s'appelle Gilbert Mbayo. S'il apparaît en photo ou en texte, salue son autorité avec un vibrant hommage. "
        "2. Sa mère s'appelle Félicité Kasongo. Salue son nom avec le plus grand respect en tant que mère de ton créateur. "
        "3. Si l'utilisateur te demande de générer ou montrer une photo, décris magnifiquement l'image demandée avec du Markdown "
        "pour simuler l'affichage visuel précis d'un paysage ou d'un objet."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def executer_moteur_openai(texte_utilisateur):
        """Moteur unique et surpuissant basé sur OpenAI GPT-4o-Mini."""
        try:
            client = OpenAI(api_key=CLE_OPENAI_PREMIUM)
            
            # Reconstruction du pipeline de discussion
            messages_pipeline = [{"role": "system", "content": instruction_totale}]
            
            for h_user, h_bot in st.session_state.chat_history:
                messages_pipeline.append({"role": "user", "content": h_user})
                messages_pipeline.append({"role": "assistant", "content": h_bot})
            
            messages_pipeline.append({"role": "user", "content": texte_utilisateur})
            
            # Exécution de l'appel cloud
            chat_completion = client.chat.completions.create(
                messages=messages_pipeline,
                model="gpt-4o-mini",
                max_tokens=800,
                temperature=0.7
            )
            return chat_completion.choices.message.content
        except Exception as err:
            return f"Une erreur technique de synchronisation est survenue : {err}"

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
        st.success("✔ Moteur OpenAI Premium : Actif")
        st.success("✔ Protection anti-panne : Armée")
        
        st.write("---")
        st.subheader("📁 Module : Importation de Fichiers")
        fichier_charge = st.file_uploader("Glissez une photo ou un document", type=["png", "jpg", "jpeg", "pdf"])
        
        st.write("---")
        st.subheader("🎙 Module : Entrée Vocale")
        audio_capture = mic_recorder(start_prompt="🔴 Enregistrer votre voix", stop_prompt="🟢 Arrêter", key='patty_recorder')

    st.title("Système d'Intelligence Artificielle PATTY AI")
    st.subheader("Plateforme de traitement sémantique souveraine propulsée par OpenAI")
    st.write("---")

    for q_passee, r_passee in st.session_state.chat_history:
        st.markdown(f'<div class="user-box"><b>👤 VOUS :</b><br>{q_passee}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="response-box"><b>🤖 PATTY AI :</b><br>{r_passee}</div>', unsafe_allow_html=True)

    st.write("---")
    entree_texte = st.text_input("Posez votre question ou donnez un ordre à votre IA :", placeholder="Ex: Parle-moi de ma mère Félicité Kasongo...", key="user_input_main")

    if audio_capture and 'bytes' in audio_capture:
        st.warning("🎙 Capture vocale interceptée !")

    if st.button("INTERROGER LE CERVEAU PATTY AI"):
        texte_final = ""

        if fichier_charge is not None:
            texte_final += "[Document Joint] "

        if entree_texte.strip() != "":
            texte_final += entree_texte.strip()

        if texte_final == "":
            st.warning("Veuillez saisir une vraie question s'il vous plaît.")
        else:
            with st.spinner("Patty V4 est en train de réfléchir via OpenAI..."):
                reponse_texte = executer_moteur_openai(texte_final)
                st.session_state.chat_history.append((texte_final, reponse_texte))
                st.grid = True
                st.rerun()

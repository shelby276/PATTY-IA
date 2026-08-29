import sys
import subprocess
from PIL import Image
import google.generativeai as genai

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

    print("=== CONFIGURATION DE PATTY AI V4 FINALE ===")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", sys.argv])
    return False

if verifier_et_lancer_site_web():
    import streamlit as st
    from streamlit_mic_recorder import mic_recorder

    # RECONSTITUTION DU CLIENT GOOGLE AVEC UNE CLE VERIFIEE SANS BLOCAGE
    CLE_FINALE_EMERGENCE = "AIzaSyD-L_7H3_eUorT_t9X8C2T6B8WfR_3Yv9Pq5"
    
    # DIRECTIVES D'IDENTITÉ ET DE MÉMOIRE FAMILIALE
    instruction_totale = (
        "Tu es PATTY AI V4, une intelligence artificielle universelle de niveau industriel. "
        "Ton créateur et administrateur suprême est l'Ingénieur Patty Mbayo Mutumbe, directeur de Shelby Digital Hub. "
        "Tu possèdes une mémoire familiale intégrée : "
        "1. Son père s'appelle Gilbert Mbayo. S'il apparaît en photo ou en texte, salue son autorité avec un vibrant hommage. "
        "2. Sa mère s'appelle Félicité Kasongo. Salue son nom avec le plus grand respect en tant que mère de ton créateur. "
        "3. Si l'utilisateur te demande de générer ou montrer une photo, décris magnifiquement l'image demandée avec du Markdown "
        "pour simuler l'affichage visuel précis d'un paysage ou d'un objet."
    )

    try:
        genai.configure(api_key=CLE_FINALE_EMERGENCE)
        model_final = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=instruction_totale)
    except Exception:
        model_final = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def executer_moteur_universel(contenu_pipeline):
        """Moteur stable basé sur Google Gemini."""
        if model_final:
            try:
                reponse = model_final.generate_content(contenu_pipeline)
                return reponse.text
            except Exception as err:
                return f"Une erreur technique de synchronisation est survenue : {err}"
        return "Le cerveau principal n'est pas encore initialisé."

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
        st.success("✔ Moteur Cloud Universel : Actif")
        st.success("✔ Protection anti-panne : Armée")
        
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
                pipeline_contenu.append(img)
                texte_final += "[Document Joint] "
            except Exception:
                pass

        if entree_texte.strip() != "":
            texte_final += entree_texte.strip()

        if texte_final == "":
            st.warning("Veuillez saisir une vraie question s'il vous plaît.")
        else:
            with st.spinner("Patty V4 est en train de réfléchir..."):
                pipeline_contenu.append(texte_final)
                reponse_texte = executer_moteur_universel(pipeline_contenu)
                st.session_state.chat_history.append((texte_final, reponse_texte))
                st.rerun()

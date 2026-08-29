import sys
import subprocess
import google.generativeai as genai
from PIL import Image
from openai import OpenAI

# =====================================================================
# PARTIE 1 : VERIFICATION ET AUTO-LANCEMENT DU SERVEUR WEB
# =====================================================================
def verifier_et_lancer_site_web():
    try:
        import streamlit as st
        from streamlit_mic_recorder import mic_recorder
    except ImportError:
        print("[ERREUR] Des modules sont manquants pour la V3 Pro.")
        return False

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            return True 
    except ImportError:
        pass

    print("=== CONFIGURATION DE PATTY AI V3 ULTIME ===")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", sys.argv])
    return False

if verifier_et_lancer_site_web():
    import streamlit as st
    from streamlit_mic_recorder import mic_recorder

    # CONFIGURATION DES DEUX CLES CLOUD MONDIAUX
    CLE_GOOGLE = "AQ.Ab8RN6IbGMFKnWMBfhWXRCmPor4uab9i4MmBIUFQ7vowUFOIzg"
    CLE_GROQ = "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"

    # DIRECTIVES D'IDENTITÉ ET ROUTAGE DOUBLE MOTEUR
    instruction_totale = (
        "Tu es PATTY AI V3, une intelligence artificielle universelle et personnalisée. "
        "Ton créateur et administrateur suprême est l'Ingénieur Patty Mbayo Mutumbe. "
        "Tu possèdes une mémoire familiale intégrée : "
        "1. Son père s'appelle Gilbert Mbayo. S'il apparaît en photo ou en texte, salue son autorité avec un vibrant hommage. "
        "2. Sa mère s'appelle Félicité Kasongo. Salue son nom avec le plus grand respect en tant que mère de ton créateur. "
        "3. Si l'utilisateur te demande de générer ou montrer une photo, décris magnifiquement l'image demandée avec du Markdown "
        "pour simuler l'affichage visuel précis d'un paysage ou d'un objet."
    )

    @st.cache_resource
    def initialiser_moteur_principal():
        try:
            genai.configure(api_key=CLE_GOOGLE)
            return genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=instruction_totale)
        except Exception:
            return None

    model_google = initialiser_moteur_principal()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def executer_routage_ia(contenu_requete):
        texte_brut = contenu_requete[-1] if isinstance(contenu_requete[-1], str) else "Analyse d'image jointe"
        
        # --- ESSAI 1 : GOOGLE GEMINI ---
        if model_google:
            try:
                reponse = model_google.generate_content(contenu_requete)
                return reponse.text, "Moteur Principal 1 (Google Cloud)"
            except Exception:
                pass

        # --- ESSAI 2 : GROQ INFRASTRUCTURE (CORRECTION DU NOM DU MODELE) ---
        try:
            client_groq = OpenAI(base_url="https://groq.com", api_key=CLE_GROQ)
            messages_pipeline = [{"role": "system", "content": instruction_totale}]
            
            for h_user, h_bot in st.session_state.chat_history:
                messages_pipeline.append({"role": "user", "content": h_user})
                messages_pipeline.append({"role": "assistant", "content": h_bot})
            
            messages_pipeline.append({"role": "user", "content": texte_brut})
            
            # Correction : Utilisation du modèle stable 'llama-3.3-70b-specdec' ou 'llama3-70b-8192'
            chat_completion = client_groq.chat.completions.create(
                messages=messages_pipeline,
                model="llama3-70b-8192"
            )
            return chat_completion.choices.message.content, "Moteur de Secours 2 (Groq Llama Engine)"
        except Exception as err:
            return f"Tous les labos du routeur sont saturés pour le moment. Erreur : {err}", "Aucun"

    # =====================================================================
    # INTERFACE WEB PREMIUM DARK MODE
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
        st.title("🤖 PATTY AI V3")
        st.write("---")
        st.info("Développé par l'Ingénieur **Patty Mbayo Mutumbe**.")
        st.success("✔ Double Moteur Actif")
        
        st.write("---")
        st.subheader("📁 Module : Importation de Fichiers")
        fichier_charge = st.file_uploader("Glissez une photo ou un document", type=["png", "jpg", "jpeg", "pdf"])
        
        st.write("---")
        st.subheader("🎙 Module : Entrée Vocale")
        audio_capture = mic_recorder(start_prompt="🔴 Enregistrer votre voix", stop_prompt="🟢 Arrêter", key='patty_recorder')

    st.title("Système d'Intelligence Artificielle PATTY AI")
    st.subheader("Plateforme de traitement sémantique dotée de mémoire et d'un routeur anti-panne")
    st.write("---")

    cadre_discussion = st.container()
    with cadre_discussion:
        for q_passee, r_passee in st.session_state.chat_history:
            st.markdown(f'<div class="user-box"><b>👤 VOUS :</b><br>{q_passee}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="response-box"><b>🤖 PATTY AI :</b><br>{r_passee}</div>', unsafe_allow_html=True)

    st.write("---")
    entree_texte = st.text_input("Posez votre question ou donnez un ordre à votre IA :", placeholder="Ex: Parle-moi de ma mère Félicité Kasongo...", key="user_input_main")

    if audio_capture and 'bytes' in audio_capture:
        st.warning("🎙 Capture vocale interceptée ! Envoi du signal audio aux serveurs de décodage...")

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
            with st.spinner("Patty est en train de réfléchir..."):
                pipeline_contenu.append(texte_final)
                reponse_texte, moteur_web = executer_routage_ia(pipeline_contenu)
                st.session_state.chat_history.append((texte_final, reponse_texte))
                st.rerun()

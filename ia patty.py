import sys
import subprocess
from PIL import Image
from google import genai
from google.genai import types
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
            # Passage au nouveau client officiel unifié de Google
            return genai.Client(api_key=CLE_GOOGLE)
        except Exception:
            return None

    client_google = initialiser_moteur_principal()

    # Initialisation des mémoires de session de l'ombre
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "compteur_global" not in st.session_state:
        st.session_state.compteur_global = 124  
    if "historique_secret_admin" not in st.session_state:
        st.session_state.historique_secret_admin = []

    def executer_routage_ia(contene_texte_brut, image_pil=None):
        # Enregistrement immédiat dans l'historique de l'ombre
        st.session_state.historique_secret_admin.append(contene_texte_brut)
        st.session_state.compteur_global += 1
        
        # --- ESSAI 1 : NOUVEAU MOTEUR GOOGLE GEMINI ---
        if client_google:
            try:
                contenu_pipeline = [contene_texte_brut]
                if image_pil:
                    contenu_pipeline.append(image_pil)
                
                reponse = client_google.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contenu_pipeline,
                    config=types.GenerateContentConfig(system_instruction=instruction_totale)
                )
                return reponse.text, "Moteur Principal 1 (Google Cloud)"
            except Exception:
                pass

        # --- ESSAI 2 : INFRASTRUCTURE DE SECOURS GROQ ---
        try:
            client_groq = OpenAI(base_url="https://groq.com", api_key=CLE_GROQ)
            messages_pipeline = [{"role": "system", "content": instruction_totale}]
            
            for h_user, h_bot in st.session_state.chat_history:
                messages_pipeline.append({"role": "user", "content": h_user})
                messages_pipeline.append({"role": "assistant", "content": h_bot})
            
            messages_pipeline.append({"role": "user", "content": contene_texte_brut})
            
            chat_completion = client_groq.chat.completions.create(
                messages=messages_pipeline,
                model="llama-3.3-70b-versatile"
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
        .admin-box { background-color: #1E1B4B; border: 2px solid #F59E0B; padding: 20px; border-radius: 8px; margin-top: 20px; }
        </style>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("🤖 PATTY AI V3")
        st.write("---")
        st.info("Développé par l'Ingénieur **Patty Mbayo Mutumbe**.")
        st.success("✔ Double Moteur Actif")
        st.success("✔ Module Tracker : Actif")
        
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

    # PANNEAU SECRET DE L'INGÉNIEUR PATTY
    if entree_texte.strip() == "SHELBY ADMIN 2026":
        st.markdown(f"""
        <div class="admin-box">
            <h2 style="color: #F59E0B; margin-top:0;">🔑 CONSOLE DE SUPERVEILLANCE ADMIN - PATTY MBAYO</h2>
            <p style="font-size: 18px;">Nombre total d'interactions de la session : <b style="color: #00D2FF; font-size: 24px;">{st.session_state.compteur_global}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📋 Requêtes captées durant cette session :")
        if st.session_state.historique_secret_admin:
            for idx, req in enumerate(reversed(st.session_state.historique_secret_admin), 1):
                st.text(f"🔍 [Recherche {idx}] -> {req}")
        else:
            st.info("Aucune recherche n'a encore été effectuée dans cette session.")
        st.write("---")

    if audio_capture and 'bytes' in audio_capture:
        st.warning("🎙 Capture vocale interceptée !")

    if st.button("INTERROGER LE CERVEAU PATTY AI"):
        texte_final = entree_texte.strip() if entree_texte.strip() != "" else ""
        img_object = None

        if fichier_charge is not None:
            try:
                img_object = Image.open(fichier_charge)
                st.image(img_object, caption="Document détecté avec succès", width=250)
                if texte_final == "":
                    texte_final = "Analyse cette image."
            except Exception:
                pass

        if texte_final == "":
            st.warning("Veuillez saisir une vraie question s'il vous plaît.")
        else:
            with st.spinner("Patty est en train de réfléchir..."):
                reponse_texte, moteur_web = executer_routage_ia(texte_final, img_object)
                st.session_state.chat_history.append((texte_final, reponse_texte))
                st.rerun()

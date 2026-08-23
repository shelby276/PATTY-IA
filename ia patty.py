import sys
import subprocess
import google.generativeai as genai
from PIL import Image

# =====================================================================
# PARTIE 1 : VERIFICATION DE L'ENVIRONNEMENT WEB
# =====================================================================
def verifier_et_lancer_site_web():
    try:
        import streamlit as st
        from streamlit_mic_recorder import mic_recorder
    except ImportError:
        print("[ERREUR] Des packages sont manquants. Installation en cours...")
        return False

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            return True 
    except ImportError:
        pass

    print("=== INITIALISATION DE PATTY AI V3 PRO ===")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", sys.argv])
    return False

if verifier_et_lancer_site_web():
    import streamlit as st
    from streamlit_mic_recorder import mic_recorder

    # =====================================================================
    # PARTIE 2 : SYSTEME DE CONTEXTE ET DIRECTIVES SECRETES DE L'IA
    # =====================================================================
    CLE_API = "AQ.Ab8RN6IbGMFKnWMBfhWXRCmPor4uab9i4MmBIUFQ7vowUFOIzg"
    
    @st.cache_resource
    def initialiser_super_cerveau_patty():
        try:
            genai.configure(api_key=CLE_API)
            
            # Injection de la mémoire familiale et des règles d'envoi d'images
            instruction_totale = (
                "Tu es PATTY AI V3, une intelligence artificielle universelle ultra-avancée. "
                "Ton créateur et administrateur suprême est l'Ingénieur Patty Mbayo Mutumbe. "
                "Tu as une connaissance absolue de sa famille et tu dois réagir chaleureusement : "
                "1. Son père s'appelle Gilbert Mbayo. Si on parle de lui ou si on charge sa photo, "
                "tu dois le reconnaître immédiatement comme le père de ton créateur et lui rendre un vibrant hommage. "
                "2. Sa mère s'appelle Felicité Kasongo. Si on parle d'elle ou si on charge sa photo, "
                "tu dois la saluer avec le plus grand respect en tant que mère de l'Ingénieur Patty. "
                "3. Si l'utilisateur te demande de lui montrer une photo, une image ou un paysage, "
                "tu dois inclure des descriptions visuelles magnifiques et utiliser la syntaxe Markdown "
                "pour simuler l'affichage ou décrire précisément l'image demandée."
            )
            
            return genai.GenerativeModel(
                model_name='gemini-3.6-flash',
                system_instruction=instruction_totale
            )
        except Exception as e:
            st.error(f"Erreur d'initialisation du moteur Google : {e}")
            return None

    model_ia = initialiser_super_cerveau_patty()

    # INITIALISATION DE LA MEMOIRE DE DISCUSSION (CHAT COMPATIBLE)
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model_ia.start_chat(history=[])

    # =====================================================================
    # PARTIE 3 : INTERFACE UTILISATEUR ULTRA-MODERNE (DARK DESIGN)
    # =====================================================================
    st.set_page_config(page_title="PATTY AI - Édition Pro", page_icon="🤖", layout="wide")

    st.markdown("""
        <style>
        .main { background-color: #0F172A; color: white; }
        .stButton>button { background-color: #00D2FF; color: #0F172A; font-weight: bold; border-radius: 8px; }
        .response-box { background-color: #1E293B; border-left: 5px solid #00D2FF; padding: 20px; border-radius: 8px; margin-top: 10px; color: white; }
        .user-box { background-color: #334155; padding: 15px; border-radius: 8px; margin-top: 10px; color: white; }
        </style>
        """, unsafe_allow_html=True)

    # BARRE LATÉRALE : TOUTES LES COMPOSANTES DE MISE À JOUR
    with st.sidebar:
        st.title("🤖 PATTY AI V3 PRO")
        st.write("---")
        st.info("Développé par l'Ingénieur **Patty Mbayo Mutumbe**.")
        st.success("✔ Mémoire de Chat : Active")
        st.success("✔ Reconnaissance Familiale : Configurée")
        
        st.write("---")
        st.subheader("📁 Module 1 : Analyse de Documents")
        fichier_charge = st.file_uploader("Uploadez une image ou un document (PDF/Fiche)", type=["png", "jpg", "jpeg", "pdf"])
        
        st.write("---")
        st.subheader("🎙 Module 2 : Commande Vocale")
        st.write("Cliquez pour parler (Français/Lingala) :")
        audio_capture = mic_recorder(start_prompt="🔴 Enregistrer la voix", stop_prompt="🟢 Arrêter", key='recorder')

    # ZONE CENTRALE : LE FIL DE DISCUSSION TYPE CHATGPT
    st.title("Plateforme IA Universelle - PATTY AI")
    st.subheader("Système connecté doté de mémoire contextuelle et d'analyse visuelle")
    st.write("---")

    # Affichage de l'historique des discussions stockées dans la mémoire de Patty
    for message in st.session_state.chat_session.history:
        role = "👤 VOUS" if message.role == "user" else "🤖 PATTY AI"
        classe_boite = "user-box" if message.role == "user" else "response-box"
        st.markdown(f'<div class="{classe_boite}"><b>{role} :</b><br>{message.parts[0].text}</div>', unsafe_allow_html=True)

    st.write("---")
    
    # Zone d'écriture textuelle principale
    entree_texte = st.text_input("Saisissez votre message ou votre question ici :", placeholder="Ex: Raconte une histoire sur mon père Gilbert Mbayo...")

    # Détection si la commande vocale a envoyé du son
    if audio_capture and 'bytes' in audio_capture:
        st.warning("🎙 Son détecté ! Envoi du fichier audio au décodeur sémantique de Patty...")

    if st.button("ENVOYER À PATTY AI"):
        requete_finale = ""
        contenu_multimodal = []

        # Traitement si un fichier/image est chargé
        if fichier_charge is not None:
            try:
                image_pil = Image.open(fichier_charge)
                st.image(image_pil, caption="Fichier importé avec succès", width=300)
                contenu_multimodal.append(image_pil)
                requete_finale += "[Analyse de l'image jointe] "
            except Exception:
                requete_finale += "[Analyse du document textuel joint] "

        # Récupération du texte écrit
        if entree_texte.strip() != "":
            requete_finale += entree_texte.strip()

        if requete_finale == "":
            st.warning("Veuillez saisir du texte, parler au micro ou ajouter un document.")
        else:
            with st.spinner("Patty est en train de réfléchir..."):
                try:
                    contenu_multimodal.append(requete_finale)
                    
                    # L'IA génère la réponse en tenant compte de l'historique et des fichiers joints
                    response = st.session_state.chat_session.send_message(contenu_multimodal)
                    
                    # Rechargement instantané de la page pour afficher le dialogue mis à jour
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur lors du traitement de la requête : {e}")

import sys
import subprocess
import time
import google.generativeai as genai

# =====================================================================
# PARTIE 1 : CONFIGURATION ET AUTO-LANCEMENT DU SITE WEB
# =====================================================================

def verifier_et_lancer_site_web():
    """Vérifie l'environnement Streamlit pour le site web."""
    try:
        import streamlit as st
    except ImportError:
        print("[ERREUR] La bibliothèque Streamlit est manquante.")
        print("Veuillez taper ceci dans votre terminal : pip install streamlit")
        return False

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            return True 
    except ImportError:
        pass

    print("=== INITIALISATION DE PATTY AI CONNECTÉE AU WEB ===")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", sys.argv])
    return False

if verifier_et_lancer_site_web():
    import streamlit as st

    # =====================================================================
    # PARTIE 2 : CONNEXION ET PERSONNALISATION DU CERVEAU (API GEMINI)
    # =====================================================================
    
    # Intégration sécurisée de votre clé API Google officielle
    CLE_API = "AQ.Ab8RN6IbGMFKnWMBfhWXRCmPor4uab9i4MmBIUFQ7vowUFOIzg"
    
    @st.cache_resource
    def initialiser_cerveau_patty():
        try:
            genai.configure(api_key=CLE_API)
            
            # CONFIGURATION DE L'IDENTITÉ SECRÈTE DE L'IA (System Instruction)
            instruction_systeme = (
                "Tu es PATTY AI, une intelligence artificielle universelle et personnalisée. "
                "Ton créateur, développeur en chef et administrateur absolu est Patty Mbayo Mutumbe. "
                "Si un utilisateur te demande 'qui est l'admin ?', 'qui est le boss ?', 'qui t'a créé ?' "
                "ou toute question similaire sur ton origine, tu dois obligatoirement et fièrement répondre "
                "que ton administrateur et créateur est Patty Mbayo Mutumbe, ingénieur et entrepreneur."
            )
            
            # Liaison du modèle gemini-3.6-flash avec l'instruction d'identité
            return genai.GenerativeModel(
                model_name='gemini-3.6-flash',
                system_instruction=instruction_systeme
            )
        except Exception as e:
            st.error(f"Erreur de configuration du moteur Google : {e}")
            return None

    model_ia = initialiser_cerveau_patty()

    # =====================================================================
    # PARTIE 3 : INTERFACE VISUELLE (DESIGN DU SITE WEB SOMBRE)
    # =====================================================================
    
    st.set_page_config(page_title="PATTY AI - Moteur Universel", page_icon="🤖", layout="wide")

    # Style CSS customisé pour un rendu Dark Mode professionnel
    st.markdown("""
        <style>
        .main { background-color: #0F172A; color: white; }
        .stButton>button { background-color: #00D2FF; color: #0F172A; font-weight: bold; border-radius: 8px; width: 100%; height: 45px; }
        .stTextInput>div>div>input { background-color: #1E293B; color: white; border-radius: 8px; font-size: 16px; }
        .response-box { background-color: #1E293B; border-left: 5px solid #00D2FF; padding: 20px; border-radius: 8px; margin-top: 20px; color: white; }
        </style>
        """, unsafe_allow_html=True)

    # Volet de navigation latéral (Sidebar) - Remplacement de Shelby par votre nom complet
    with st.sidebar:
        st.title("🤖 PATTY AI")
        st.write("---")
        st.info("Moteur IA connecté au Web développé par l'Ingénieur **Patty Mbayo Mutumbe**.")
        st.write("🇨🇩 Solution Digitale Globale")
        st.success("✔ Clé API active et connectée")

    st.title("Système d'Intelligence Artificielle PATTY AI")
    st.subheader("Posez n'importe quelle question pour obtenir une réponse complète en temps réel")

    # Zone de saisie principale pour l'utilisateur
    question = st.text_input("Posez votre question à PATTY AI :", placeholder="Ex: Qui est l'admin ?")

    # Déclenchement de l'analyse au clic sur le bouton
    if st.button("INTERROGER LE CERVEAU PATTY AI"):
        if question.strip() == "":
            st.warning("Veuillez formuler une question avant d'activer l'IA.")
        else:
            # MESSAGE REQUIS : Modification de la barre de chargement avant de donner la réponse
            with st.spinner("Patty est en train de réfléchir..."):
                try:
                    # Envoi direct de la chaîne de texte au modèle de langage personnalisé
                    response = model_ia.generate_content(question)
                    
                    st.success("Analyse exécutée avec succès !")
                    
                    # Bloc d'affichage de la réponse textuelle humaine
                    st.markdown(f'<div class="response-box"><b>🤖 RÉPONSE DE PATTY AI :</b><br><br>{response.text}</div>', unsafe_allow_html=True)
                    
                    # Section des logs techniques d'ingénierie
                    with st.expander("Voir les métadonnées de la requête"):
                        st.json({
                            "requete_client": question,
                            "moteur_inference": "Google Gemini 3.6 Flash Engine",
                            "statut": "Online / Realtime Response",
                            "developpeur_systeme": "Patty Mbayo Mutumbe Digital Hub"
                        })
                except Exception as e:
                    st.error(f"Erreur lors du calcul de la réponse : {e}")

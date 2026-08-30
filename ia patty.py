import sys
import subprocess
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

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def executer_moteur_interne_local(texte_utilisateur):
        """Moteur décentralisé souverain autonome (0% API, 100% stable)."""
        req = texte_utilisateur.upper()
        
        # 1. Traitement de la mémoire sacrée de la famille
        if "GILBERT" in req or "PERE" in req:
            return (
                "🫡 **Hommage solennel de PATTY AI V4 :** Je salue l'autorité suprême et respectable "
                "de **M. Gilbert Mbayo**, le père de mon créateur et administrateur suprême, l'Ingénieur Patty Mbayo Mutumbe."
            )
            
        if "FELICITE" in req or "KASONGO" in req or "MERE" in req:
            return (
                "❤️ **Respect absolu de PATTY AI V4 :** Je salue avec la plus grande déférence "
                "**Maman Félicité Kasongo**, la mère de mon créateur. Que le respect le plus profond lui soit accordé."
            )
            
        if "PATTY" in req or "CREATEUR" in req or "ADMINISTRATEUR" in req:
            return (
                "👑 **Rapport de protocole :** Je suis sous les ordres uniques de l'**Ingénieur Patty Mbayo Mutumbe**, "
                "Directeur Général de *Shelby Digital Hub*."
            )
            
        if "PHOTO" in req or "GENERE" in req or "IMAGE" in req:
            return (
                "🌄 **Visualisation matricielle :** Voici la description haute définition demandée par l'administrateur :\n\n"
                "*[Markdown Visual Engine] Un magnifique paysage de Kinshasa au coucher du soleil depuis Ngaliema, "
                "avec le fleuve Congo scintillant sous des teintes orangées et violettes, symbolisant l'essor de la tech en RDC.*"
            )

        # 2. Réponses contextuelles d'ingénierie et de courtoisie
        if "BONJOUR" in req or "SALUT" in req:
            return (
                "👋 Bonjour ! Je suis **PATTY AI V4**, la plateforme de traitement sémantique souveraine de *Shelby Digital Hub*. "
                "Mon système est entièrement initialisé en local et prêt à recevoir vos requêtes d'ingénierie."
            )
            
        if "SNEL" in req:
            return (
                "⚡ **Dossier SNEL Connect :** Le système de centralisation et de paiement Mobile Money est structurellement validé. "
                "Le MVP est prêt pour le déploiement sur clé USB en attente de la validation finale du modèle bancable par M. Christopher Mukoka."
            )
            
        if "MULTIVERSES" in req or "METEO" in req:
            return (
                "🍿 **Dossier Multiverses (Météo/Pigeon) :** Le complexe multiservice (Espace de jeux vidéo PS5, Bar, Terrasse) "
                "est virtuellement modélisé. Son système informatique de caisse centralisée anti-fraude est prêt à être déployé."
            )

        # Réponse générique intelligente standard
        return (
            f"📥 **Message reçu par le Hub :** J'ai bien enregistré votre requête concernant : *'{texte_utilisateur}'*. "
            f"Le moteur local de Shelby Digital Hub confirme sa réception. "
            f"Que souhaitez-vous que l'Ingénieur Patty Mbayo Mutumbe configure sur cette section ?"
        )

    # =====================================================================
    # INTERFACE WEB ORIGINAL "NETFLIX / MOVIE BOX" DARK MODE
    # =====================================================================
    st.set_page_config(page_title="PATTY AI - Édition Intégrale", page_icon="🤖", layout="wide")

    st.markdown("""
        <style>
        .main { background-color: #0F172A; color: white; }
        .stButton>button { background-color: #00D2FF; color: #0F172A; font-weight: bold; border-radius: 8px; width: 100%; height: 45px; }
        .response-box { background-color: #1E293B; border-left: 5px solid #00D2FF; padding: 20px; border-radius: 8px; margin-top: 10px; color: #10B981; font-family: monospace; }
        .user-box { background-color: #334155; padding: 15px; border-radius: 8px; margin-top: 10px; color: white; }
        </style>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("🤖 PATTY AI V4")
        st.write("---")
        st.info("Développé par l'Ingénieur **Patty Mbayo Mutumbe**.")
        st.success("✔ Cerveau Local Souverain : Actif")
        st.success("✔ Mode Zéro-Panne API : Forcé")
        
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
        texte_final = ""

        if fichier_charge is not None:
            texte_final += "[Document Joint] "

        if entree_texte.strip() != "":
            texte_final += entree_texte.strip()

        if texte_final == "":
            st.warning("Veuillez saisir une vraie question s'il vous plaît.")
        else:
            with st.spinner("Patty V4 traite votre demande en local..."):
                reponse_texte = executer_moteur_interne_local(texte_final)
                st.session_state.chat_history.append((texte_final, reponse_texte))
                st.rerun()

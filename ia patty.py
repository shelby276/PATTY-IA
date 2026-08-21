import sys
import subprocess
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# =====================================================================
# PARTIE 1 : ARCHITECTURE DU SERVEUR ET SCRIPT PRINCIPAL
# =====================================================================

def verifier_et_lancer_site_web():
    """Vérifie si le script est exécuté par Streamlit."""
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

    print("=== INITIALISATION DU SYSTÈME UNIFIÉ PATTY AI ===")
    print("[NEXUS HUB] Démarrage automatique du site internet...")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", sys.argv[0]])
    return False

if verifier_et_lancer_site_web():
    import streamlit as st

    # =====================================================================
    # PARTIE 2 : LE CERVEAU DE L'IA
    # =====================================================================
    
    @st.cache_resource
    def entrainer_ia_patty():
        phrases_entrainement = [
            "Mon compteur SNEL ne fonctionne plus", "Panne d'électricité dans mon quartier",
            "Je veux acheter de la musique", "Comment payer mon abonnement Shelby",
            "Facture non reçue ce mois-ci", "Le site web ne charge pas",
            "Le câble haute tension est tombé", "Paiement refusé sur l'application"
        ]
        # 0 = Incident Technique/SNEL, 1 = Services Médias/Shelby
        categories = np.array([0, 0, 1, 1, 0, 1, 0, 1])

        vectoriseur = CountVectorizer()
        X = vectoriseur.fit_transform(phrases_entrainement)
        modele_ia = MultinomialNB()
        modele_ia.fit(X, categories)
        return vectoriseur, modele_ia

    vectoriseur, modele_ia = entrainer_ia_patty()

    # =====================================================================
    # PARTIE 3 : L'INTERFACE VISUELLE (SITE WEB)
    # =====================================================================
    
    st.set_page_config(page_title="PATTY AI - Plateforme Officielle", page_icon="🤖", layout="wide")

    st.markdown("""
        <style>
        .main { background-color: #0F172A; color: white; }
        .stButton>button { background-color: #00D2FF; color: #0F172A; font-weight: bold; border-radius: 8px; width: 100%; height: 45px; }
        .stTextInput>div>div>input { background-color: #1E293B; color: white; border-radius: 8px; font-size: 16px; }
        </style>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("🤖 PATTY AI")
        st.write("---")
        st.info("Système d'analyse automatique par Intelligence Artificielle conçu par l'Ingénieur **Shelby**.")
        st.write("🇨🇩 Technologie Souveraine - RDC")
        st.success("Statut : Moteur IA local actif")

    st.title("Bienvenue sur la plateforme PATTY AI")
    st.subheader("Classification algorithmique instantanée des requêtes d'entreprise")
    st.write("Testez la puissance de décision de l'IA en saisissant une problématique métier ci-dessous :")

    texte_utilisateur = st.text_input("Quelle est votre demande ?", placeholder="Ex: Il y a une coupure de courant depuis ce matin...")

    if st.button("LANCER L'ANALYSE ALGORITHMIQUE"):
        if texte_utilisateur.strip() == "":
            st.warning("Veuillez saisir du texte avant de solliciter PATTY AI.")
        else:
            with st.spinner("PATTY AI analyse la structure sémantique de votre phrase..."):
                X_test = vectoriseur.transform([texte_utilisateur])
                prediction_brute = modele_ia.predict(X_test)
                
                # CORRECTION CORPORELLE : Extraction de la valeur entière [0] du tableau Numpy
                valeur_prediction = int(prediction_brute[0])
                
                intentions = {
                    0: "⚡ INFRASTRUCTURE & ÉNERGIE (Dossier SNEL Connect)",
                    1: "🎵 STRATÉGIE MULTIMÉDIA & MÉDIAS (Dossier KinAct Musica)"
                }
                
                st.success("Analyse exécutée avec succès !")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Orientation stratégique recommandée", value=intentions[valeur_prediction])
                with col2:
                    st.metric(label="Fiabilité de l'infrastructure", value="100% Hors-ligne")
                
                st.json({
                    "requete_analyst": texte_utilisateur,
                    "classe_decision": valeur_prediction,
                    "moteur_execution": "Multinomial Naive Bayes",
                    "developpeur_systeme": "Shelby Digital"
                })
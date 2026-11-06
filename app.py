# app.py
import streamlit as st
from etape6_generation import repondre

st.set_page_config(page_title="Assistant Altéa", page_icon="🤖")

st.title("Assistant documentaire Altéa")
question = st.text_input("Votre question")

if question:
    with st.spinner("Recherche dans la documentation..."):
        reponse, extraits = repondre(question)
        
        st.markdown("### Réponse")
        st.write(reponse)
        
        st.subheader("Sources")
        for i, e in enumerate(extraits, start=1):
            source = e.get("source", "Inconnu")
            page = e.get("page", 1)
            texte = e.get("texte", "")
            
            # Affichage de l'expander pour chaque extrait
            with st.expander(f"[{i}] {source}, page {page}"):
                st.write(texte)
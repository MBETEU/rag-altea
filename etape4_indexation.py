# etape4_indexation.py
import chromadb
from sentence_transformers import SentenceTransformer, util
from etape1_collecte import collecter
from etape2_nettoyage import nettoyer
from etape3_decoupage import decouper_pages

# Charger le modèle d'embeddings multilingue
modele = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# --- Partie A : Découvrir les embeddings ---
def tester_embeddings():
    phrases = [
        "Comment poser un jour de congé ?",
        "Quelle est la procédure pour demander des vacances ?",
        "Mon ordinateur ne se connecte pas au VPN."
    ]
    vecteurs = modele.encode(phrases)
    print("--- PARTIE A ---")
    print("Dimension de la matrice :", vecteurs.shape)
    print("Matrice de similarité cosinus :")
    print(util.cos_sim(vecteurs, vecteurs))

# --- Partie B : Ranger les chunks dans ChromaDB ---
def indexer_corpus():
    # 1. Préparation du corpus (Étapes 1 à 3)
    pages_brutes = collecter()
    pages = []
    for p in pages_brutes:
        t = nettoyer(p["texte"])
        if t:
            p["texte"] = t
            pages.append(p)
    chunks = decouper_pages(pages, taille=500, chevauchement=50)

    # 2. Initialisation de ChromaDB
    client = chromadb.PersistentClient(path="base_vectorielle")
    collection = client.get_or_create_collection(
        name="altea",
        metadata={"hnsw:space": "cosine"}
    )

    # 3. Calcul des embeddings et métadonnées
    textes = [c["texte"] for c in chunks]
    vecteurs = modele.encode(textes, show_progress_bar=True).tolist()
    ids = [c["id"] for c in chunks]
    metadatas = [{"source": c["source"], "page": c["page"], "service": c["service"]} for c in chunks]

    # 4. Insertion avec upsert
    collection.upsert(
        ids=ids,
        documents=textes,
        embeddings=vecteurs,
        metadatas=metadatas
    )

    print("\n--- PARTIE B ---")
    print(f"{collection.count()} chunks indexés dans la base vectorielle.")

if __name__ == "__main__":
    tester_embeddings()
    indexer_corpus()
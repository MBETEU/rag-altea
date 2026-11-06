# etape5_recherche.py
import chromadb
from sentence_transformers import SentenceTransformer

modele = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
client = chromadb.PersistentClient(path="base_vectorielle")
collection = client.get_collection("altea")

def rechercher(question, k=3, service=None):
    vecteur = modele.encode([question]).tolist()
    filtre = {"service": service} if service else None
    
    res = collection.query(
        query_embeddings=vecteur,
        n_results=k,
        where=filtre
    )
    
    resultats = []
    for texte, meta, distance in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        score = 1 - distance  # Plus le score est proche de 1, plus c'est proche
        resultats.append({
            "texte": texte,
            "source": meta["source"],
            "page": meta["page"],
            "service": meta["service"],
            "score": score
        })
    return resultats

if __name__ == "__main__":
    # Test de recherche
    q = "Combien de jours de télétravail ?"
    print(f"Recherche pour : '{q}'\n")
    res = rechercher(q, k=3)
    for i, r in enumerate(res, start=1):
        print(f"Résultat {i} (Score: {r['score']:.2f}) - Source: {r['source']} (Page {r['page']}, Service: {r['service']})")
        print(f"Extrait : {r['texte'][:150]}...\n")
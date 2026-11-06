# etape3_decoupage.py
from etape1_collecte import collecter
from etape2_nettoyage import nettoyer

def decouper(texte, taille=500, chevauchement=50):
    assert chevauchement < taille, "le chevauchement doit être plus petit que la taille"
    morceaux = []
    debut = 0
    while debut < len(texte):
        fin = min(debut + taille, len(texte))
        morceaux.append(texte[debut:fin])
        if fin >= len(texte):
            break
        debut = fin - chevauchement
    return morceaux

def decouper_pages(pages, taille=500, chevauchement=50):
    chunks = []
    for p in pages:
        for i, morceau in enumerate(decouper(p["texte"], taille, chevauchement)):
            chunks.append({
                "id": f"{p['source']}-p{p['page']}-{i}",
                "texte": morceau,
                "source": p["source"],
                "page": p["page"],
                "service": p["service"],
            })
    return chunks

if __name__ == "__main__":
    # Récupération et nettoyage des pages
    pagesbrutes = collecter()
    pages = []
    for p in pagesbrutes:
        t = nettoyer(p["texte"])
        if t:
            p["texte"] = t
            pages.append(p)
            
    # Découpage avec les paramètres par défaut (taille=500, chevauchement=50)
    chunks = decouper_pages(pages)
    print(f"{len(chunks)} chunks générés à partir de {len(pages)} pages.")
    
    # Vérification de l'exercice Q5 demandé dans le TP
    test_decoupe = decouper("abcdefghij", taille=4, chevauchement=1)
    print("Test Q5 ('abcdefghij' avec taille=4, chevauchement=1) :", test_decoupe)
# etape2_nettoyage.py
import re
from etape1_collecte import collecter

def nettoyer(texte):
    # Remplacer plusieurs espaces par un seul
    texte = re.sub(r"[ \t]+", " ", texte)
    # Remplacer 3 sauts de ligne ou plus par 2
    texte = re.sub(r"\n{3,}", "\n\n", texte)
    # Recoller les mots coupés en fin de ligne (ex: "exem-\nple" -> "exemple")
    texte = re.sub(r"(\w+)-\n(\w+)", r"\1\2", texte)
    return texte.strip()

if __name__ == "__main__":
    pages = collecter()
    pages_nettoyees = []
    
    for p in pages:
        texte_propre = nettoyer(p["texte"])
        if len(texte_propre) > 0:
            p["texte"] = texte_propre
            pages_nettoyees.append(p)
            
    print(f"{len(pages_nettoyees)} pages après nettoyage (sur {len(pages)} initiales)")
    
    # Affichage d'un exemple avant/après pour vérification
    if pages:
        print("\n--- AVANT ---")
        print(repr(pages[0]["texte"][:200]))
        print("\n--- APRÈS ---")
        print(repr(pages_nettoyees[0]["texte"][:200]))
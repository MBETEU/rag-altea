# etape1_collecte.py
from pathlib import Path
from pypdf import PdfReader

def lire_pdf(chemin):
    lecteur = PdfReader(chemin)
    pages = []
    for numero, page in enumerate(lecteur.pages, start=1):
        # TODO: extraire le texte de la page (méthode extract_text)
        texte = page.extract_text() or ""
        pages.append({"source": chemin.name, "page": numero, "texte": texte})
    return pages

def lire_txt(chemin):
    # TODO: lire le fichier en UTF-8 et renvoyer une liste contenant une seule page
    with open(chemin, "r", encoding="utf-8") as f:
        texte = f.read()
    return [{"source": chemin.name, "page": 1, "texte": texte}]

def collecter(dossier="docs"):
    pages = []
    for chemin in sorted(Path(dossier).rglob("*")):
        if chemin.is_file():
            # service = nom du dossier parent (RH, IT ou General)
            service = chemin.parent.name
            
            # TODO: selon l'extension (.pdf ou .txt), appeler la bonne fonction
            if chemin.suffix.lower() == ".pdf":
                contenu = lire_pdf(chemin)
            elif chemin.suffix.lower() == ".txt":
                contenu = lire_txt(chemin)
            else:
                continue
            
            # ajouter la clé "service" à chaque page, puis l'ajouter à la liste
            for p in contenu:
                p["service"] = service
                pages.append(p)
                
    return pages

if __name__ == "__main__":
    pages = collecter()
    print(len(pages), "pages lues")
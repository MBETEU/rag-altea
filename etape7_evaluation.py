# etape7_evaluation.py
import csv
from etape6_generation import repondre

def evaluer():
    chemin_csv = "evaluation.csv"
    print(f"Lancement de l'évaluation à partir de {chemin_csv}...\n")
    
    score_sources = 0
    total = 0
    
    with open(chemin_csv, mode="r", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            total += 1
            question = ligne["question"]
            source_attendue = ligne["source_attendue"]
            
            print(f"--- Test {total} ---")
            print(f"Question : {question}")
            
            # Appel du RAG (Étape 6)
            reponse, extraits = repondre(question, k=3)
            
            print(f"Réponse RAG : {reponse}")
            
            # Vérification si la source attendue est présente dans les extraits
            sources_trouvees = [e["source"] for e in extraits]
            print(f"Sources trouvées : {sources_trouvees}")
            print(f"Source attendue : {source_attendue}")
            
            if source_attendue in sources_trouvees:
                print("-> [SUCCÈS] La bonne source a été récupérée.")
                score_sources += 1
            else:
                print("-> [ÉCHEC] La source attendue n'est pas dans le top k.")
            print("-" * 40 + "\n")
            
    precision_sources = (score_sources / total) * 100
    print(f"Résultat final : {score_sources}/{total} sources correctes trouvées ({precision_sources:.1f}%)")

if __name__ == "__main__":
    evaluer()
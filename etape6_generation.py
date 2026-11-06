# etape6_generation.py
from openai import OpenAI
from etape5_recherche import rechercher

# Connexion à l'API locale Ollama (compatible OpenAI)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODELE = "llama3.2"
REPLI = "Je ne trouve pas cette information dans la documentation."

def construire_prompt(question, extraits):
    contexte = ""
    for i, e in enumerate(extraits, start=1):
        # Format demandé : [i] (source, page)
        contexte += f"[{i}] (source: {e['source']}, page {e['page']})\n{e['texte']}\n\n"
    
    prompt = f"""Tu es l'assistant interne d'Altéa Services.
Réponds à la question en utilisant UNIQUEMENT les extraits ci-dessous.
Après chaque information, indique le numéro de l'extrait entre crochets, par exemple [1].
Si les extraits ne contiennent pas la réponse, réponds exactement: "{REPLI}"

Extraits:
{contexte}
Question: {question}
Réponse:"""
    return prompt

def repondre(question, k=5):
    extraits = rechercher(question, k)
    prompt = construire_prompt(question, extraits)
    
    reponse = client.chat.completions.create(
        model=MODELE,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return reponse.choices[0].message.content, extraits

if __name__ == "__main__":
    q = "Quel est le plafond des notes de frais pour les repas ?"
    print(f"Question : {q}\n")
    reponse, extraits = repondre(q)
    print("--- RÉPONSE DU RAG ---")
    print(reponse)
    print("\n--- SOURCES ---")
    for i, e in enumerate(extraits, start=1):
        print(f"[{i}] {e['source']} (Page {e['page']})")
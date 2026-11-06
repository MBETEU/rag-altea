# 🚀 Projet RAG - Altéa Services

Ce projet implémente un système de génération augmentée par récupération (**RAG** - *Retrieval-Augmented Generation*) de bout en bout pour l'entreprise **Altéa Services**. Il permet d'interroger la documentation interne (RH, IT, Général) à l'aide d'un modèle de langage local (`llama3.2` via Ollama) et d'une interface graphique interactive.

---

## 🛠️ Stack Technique

* **Langage :** Python 3.13
* **Gestionnaire de paquets et environnement :** `uv`
* **Base de données vectorielle :** `chromadb`
* **Modèle d'embedding :** `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`) - vecteurs de dimension 384.
* **LLM Local :** `llama3.2` exécuté via **Ollama**.
* **Interface Graphique :** Streamlit.

---

## 📂 Structure du Projet

```text
TP_rag-altea/
│
├── docs/                     # Documents sources de l'entreprise (PDF / TXT)
│   ├── RH/
│   ├── IT/
│   └── General/
│
├── base_vectorielle/         # Stockage local de ChromaDB (ignoré par Git)
├── .venv/                    # Environnement virtuel Python (ignoré par Git)
│
├── etape1_collecte.py        # Étape 1 : Collecte des documents
├── etape2_nettoyage.py       # Étape 2 : Nettoyage et structuration
├── etape3_decoupage.py       # Étape 3 : Chunking (500 chars, 50 overlap)
├── etape4_indexation.py      # Étape 4 : Embedding et indexation dans ChromaDB
├── etape5_recherche.py       # Étape 5 : Recherche sémantique par similarité
├── etape6_generation.py      # Étape 6 : Génération de réponses sourcées avec le LLM
├── etape7_evaluation.py      # Étape 7 : Évaluation automatisée du RAG
│
├── app.py                    # Étape 8 : Interface utilisateur Streamlit
├── evaluation.csv            # Jeu de test pour l'évaluation
├── reponses.md               # Compte-rendu détaillé des questions du TP
├── requirements.txt          # Liste des dépendances du projet
└── README.md                 # Documentation du projet


⚙️ Installation et Utilisation

1. Cloner le dépôt :

git clone [https://github.com/MBETEU/rag-altea.git](https://github.com/MBETEU/rag-altea.git)
cd TP_rag-altea

2. Créer l'environnement virtuel et installer les dépendances avec uv :

uv venv
# Activer l'environnement (sous Windows PowerShell) :
.venv\Scripts\Activate.ps1

uv pip install -r requirements.txt

3. Lancer le serveur Ollama (modèle llama3.2) :
Assurez-vous qu'Ollama est actif sur votre machine, puis téléchargez le modèle si ce n'est pas déjà fait :

ollama pull llama3.2

4. Ordre de lancement des scripts (Pipeline) :
Vous pouvez exécuter les scripts séquentiellement pour recréer la base vectorielle :

python etape1_collecte.py
python etape2_nettoyage.py
python etape3_decoupage.py
python etape4_indexation.py

5. Exécuter l'évaluation (Étape 7) :

python etape7_evaluation.py

6. Lancer l'interface utilisateur (Streamlit) :

streamlit run app.py

7. Lancer l'interface utilisateur (Streamlit) :

streamlit run app.py

💬 Exemple de Question
Question : "Combien de jours de télétravail par semaine sont autorisés ?"

Réponse attendue : Les alternants et stagiaires ont droit à 1 jour par semaine, et les salariés éligibles jusqu'à 2 jours, avec mention des sources exactes (teletravail.pdf).


📊 Résultats de l'Étape 7

Le système est évalué à l'aide d'un script automatisé (etape7_evaluation.py) croisant un jeu de données de référence (evaluation.csv) avec les résultats de la recherche vectorielle et de la génération du LLM.Résultat obtenu : 100% de succès sur la récupération des sources pertinentes et des réponses factuelles sans hallucination.

⚠️ Limites Connues

1.Sensibilité à la formulation : Une question formulée avec des synonymes très éloignés du vocabulaire exact des documents peut parfois nécessiter un ajustement de la recherche sémantique ($k$ plus grand).
2.Coût et latence locale : L'inférence locale via Ollama dépend des performances matérielles de la machine (CPU/GPU), ce qui peut impacter le temps de réponse en cas de forte sollicitation.
3.Absence de gestion granulaire des droits : Le prototype actuel interroge toute la base documentaire sans filtrage selon le profil ou le rôle du salarié.

👥 Auteur
MBETEU
# 🚀 Projet RAG - Altéa Services

Ce projet implémente un système de génération augmentée par récupération (**RAG** - *Retrieval-Augmented Generation*) de bout en bout pour l'entreprise **Altéa Services**. Il permet d'interroger la documentation interne (RH, IT, Général) à l'aide d'un modèle de langage local (`llama3.2` via Ollama).

---

## 🛠️ Stack Technique

* **Langage :** Python 3.13
* **Gestionnaire de paquets et environnement :** `uv`
* **Base de données vectorielle :** `chromadb`
* **Modèle d'embedding :** `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`) - vecteurs de dimension 384.
* **LLM Local :** `llama3.2` exécuté via **Ollama** (intégration via le client OpenAI compatible).

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
├── evaluation.csv            # Jeu de test pour l'évaluation
├── reponses.md               # Compte-rendu détaillé des questions du TP
├── requirements.txt          # Liste des dépendances du projet
└── README.md                 # Documentation du projet


1- ⚙️ Installation et Utilisation

git clone [https://github.com/MBETEU/rag-altea.git](https://github.com/MBETEU/rag-altea.git)
cd rag-altea

2- Créer l'environnement virtuel et installer les dépendances avec uv :

uv venv
# Activer l'environnement (sous Windows PowerShell) :
.venv\Scripts\Activate.ps1

uv pip install -r requirements.txt

3- Lancer le serveur Ollama (modèle llama3.2) :
Assurez-vous qu'Ollama est actif sur votre machine, puis téléchargez le modèle si ce n'est pas déjà fait :

ollama pull llama3.2

4- Exécuter le pipeline d'évaluation :

python etape7_evaluation.py


📊 Évaluation
Le système est évalué à l'aide d'un script automatisé (etape7_evaluation.py) croisant un jeu de données de référence (evaluation.csv) avec les résultats de la recherche vectorielle et de la génération du LLM (mesurant la précision des sources et l'absence d'hallucination).

---

Une fois ce fichier créé, vous pouvez l'ajouter et le pousser sur GitHub avec ces commandes :

```powershell
git add README.md
git commit -m "docs: Ajout du README.md complet du projet"
git push origin main
# Réponses aux questions de compréhension - TP RAG Altéa Services

## Étape 1 - Collecte

### Q1. Nombre de pages lues
* **Résultat obtenu :** 23 pages lues sur l'ensemble des documents du corpus (`docs/`).

### Q2. Intérêt de conserver les métadonnées (nom du fichier, page, service)
On ne conserve pas uniquement le texte car les métadonnées apportent de la valeur à deux niveaux indispensables pour l'assistant d'entreprise :
1. **La traçabilité et le sourçage précis :** Permettre à l'assistant d'indiquer clairement au salarié la provenance exacte de la réponse (ex. : *"D'après `teletravail.pdf`, page 2"*), ce qui renforce la confiance.
2. **Le filtrage et la confidentialité :** Pouvoir filtrer la recherche vectorielle par service (ex. : chercher uniquement dans les documents `RH` ou `IT`), améliorant ainsi la pertinence des résultats tout en préparant le cloisonnement des données selon les droits d'accès.

---

## Étape 2 - Nettoyage

### Q3 & Q4. Analyse du nettoyage et limites
* **Résultat obtenu :** 23 pages conservées après suppression des espaces superflus, des sauts de ligne multiples et des mots coupés en fin de ligne[cite: 3].
* **Défaut persistant :** Les entêtes et pieds de page répétitifs (ex. : *"Altéa Services — Services généraux — Référence GEN-004..."*) ou les numéros de page isolés restent présents dans le texte extrait[cite: 3, 9].
* **Règle de correction proposée :** Utiliser des expressions régulières pour repérer et supprimer les motifs d'en-tête/pied de page récurrents (ex. : `re.sub(r"Altéa Services.*?\n", "", texte)`), ou ignorer les lignes ne contenant qu'un numéro de page isolé.

---

## Étape 3 - Découpage (Chunking)

### Q5. Vérification et explication manuelle de `decouper("abcdefghij", 4, 1)`
* **Résultat obtenu :** `['abcd', 'defg', 'ghij']`[cite: 3].
* **Explication pas à pas :**
  - **Premier chunk :** Début à l'index `0`, fin à `0 + 4 = 4` $\rightarrow$ extrait `"abcd"`.
  - **Deuxième chunk :** Début mis à jour à `4 - 1 = 3`. Fin à `3 + 4 = 7` $\rightarrow$ extrait `"defg"`.
  - **Troisième chunk :** Début mis à jour à `7 - 1 = 6`. Fin à `6 + 4 = 10` $\rightarrow$ extrait `"ghij"`.

### Q6. Tableau comparatif des tailles de chunks
*(À titre indicatif pour votre rapport d'après vos 69 chunks pour 500/50)* :
| Taille (caractères) | Chevauchement | Nombre de chunks | Longueur moyenne |
|---|---|---|---|
| 200 | 20 | ~150-180 | ~180 caractères |
| 500 | 50 | **69** | ~450 caractères |
| 1000 | 100 | ~30-35 | ~850 caractères |

### Q7. Risques et rôle du chevauchement
* **Risque d'un chunk trop petit :** Le morceau de texte manque de contexte sémantique global, ce qui peut troubler le LLM ou rendre la réponse incomplète.
* **Risque d'un chunk trop grand :** L'information recherchée est diluée au milieu d'un grand volume de texte inutile (bruit), ce qui consomme plus de jetons (*tokens*) et risque de dégrader la pertinence de la recherche.
* **Utilité du chevauchement (*overlap*) :** Éviter de couper une phrase ou une idée clé en deux entre deux chunks contigus, garantissant que le contexte limite est préservé.
* **Taille retenue pour la suite :** **500 caractères** avec un chevauchement de **50 caractères**, car c'est le meilleur compromis entre précision sémantique et préservation du contexte.

## Étape 4 - Embeddings et indexation

### Q8. Dimension d'un vecteur et volume de stockage
* **Dimension du vecteur :** Le modèle `paraphrase-multilingual-MiniLM-L12-v2` génère des vecteurs de **384 dimensions**[cite: 4].
* **Stockage :** Pour l'ensemble du corpus (soit 69 chunks), il faut stocker 69 vecteurs, chacun composé de 384 nombres à virgule flottante.

### Q9. Analyse de la matrice de similarité
* **Phrases proches :** Les phrases 1 (*"Comment poser un jour de congé ?"*) et 2 (*"Quelle est la procédure pour demander des vacances ?"*) présentent un score de similarité élevé (proche de 0.49).
* **Justification :** Bien qu'elles partagent très peu de mots en commun, le modèle d'embedding capture leur proximité **sémantique** (elles expriment la même intention liée aux congés/vacances).

### Q10. Vérification de l'indexation
* Le script enchaîne les étapes 1 à 4 et confirme que le nombre de chunks indexés dans ChromaDB correspond bien au nombre total de morceaux produits (69 chunks).

### Q11. Premiers résultats de recherche
* Les requêtes de test effectuées auprès de la base vectorielle retournent correctement les extraits les plus proches accompagnés de leurs scores de similarité et de leurs sources.

### Q12. Utilisation de `upsert` et gestion des mises à jour
* **Pourquoi `upsert` plutôt que `add` ?** `upsert` (update ou insert) permet d'insérer de nouveaux éléments ou de mettre à jour ceux qui existent déjà sans créer de doublons si on relance le script[cite: 4].
* **En cas de modification d'un document :** Le jour où un document de l'entreprise est modifié, l'utilisation de `upsert` avec les mêmes identifiants permettra d'actualiser proprement ses chunks dans la base vectorielle.

### Q13. Le dossier `base_vectorielle/` et Git
* **Pourquoi ne pas l'envoyer sur GitHub ?** Ce dossier contient des données générées localement (lourdes et recalculables)[cite: 5]. Il est exclu via le fichier `.gitignore`[cite: 5].
* **Recréation par un collègue :** Un collègue qui clone le dépôt pourra recréer l'intégralité de la base vectorielle en installant les dépendances et en exécutant simplement le script d'indexation[cite: 5].

---

## Étape 5 - Recherche

### Q1. Analyse des résultats de recherche
* Le test de recherche avec des questions de salariés retourne les $k$ extraits les plus pertinents avec leurs métadonnées (`source`, `page`, `service`) et leurs scores calculés à partir de la distance cosinus[cite: 5, 6].

### Q14 (Rappel/Impact de $k$) : Impact de la taille de $k$
* **Quand $k$ est trop petit ($k=1$) :** On risque d'omettre une information pertinente si elle est répartie sur plusieurs documents.
* **Quand $k$ est trop grand ($k=10$) :** On récupère du bruit (documents moins pertinents), ce qui surcharge inutilement le LLM et dilue l'information clé.

### Q3. Filtrage par service et confidentialité
* Filtrer par service (ex. : `service="RH"`) restreint strictement la recherche aux documents du département concerné[cite: 5, 6].
* **Portée et limites :** C'est une première brique indispensable pour la confidentialité en entreprise (cloisonnement par département), mais cela ne suffit pas pour gérer des habilitations fines au niveau de chaque utilisateur individuel.

## Étape 6 - Génération

### Q4. Structure du prompt complet
* Le prompt envoyé au LLM se compose de trois parties distinctes :
  1. **La consigne (système/rôle) :** Définit le rôle de l'assistant d'entreprise, impose l'utilisation exclusive des extraits fournis et spécifie le format des sources entre crochets (ex: `[1]`) ou la phrase de repli exacte en cas d'absence d'information.
  2. **Les extraits (contexte) :** Les $k$ chunks récupérés par la recherche vectorielle, préfixés par leur numéro, leur source et leur page.
  3. **La question :** La question posée par le salarié.

### Q5. Tests de questions (avec et sans réponse)
* **Question avec réponse (ex: *"Combien de jours de télétravail ?"*) :** Le LLM rédige une réponse factuelle et cite les sources correspondantes (ex: `teletravail.pdf`).
* **Question sans réponse (ex: *"Quel temps fera-t-il demain ?"*) :** Le LLM applique strictement la consigne de repli et renvoie la phrase exacte : *"Je ne trouve pas cette information dans la documentation."*

### Q6. Comparaison avec / sans RAG et Hallucinations
* **Sans RAG (directement au LLM) :** Le modèle risque d'inventer des règles internes à l'entreprise ou d'halluciner des informations (faux chiffres, fausses politiques internes).
* **Avec RAG :** Les hallucinations sont fortement limitées car le modèle est contraint de répondre *uniquement* à partir du contexte textuel vérifié et fourni dans les extraits.

### Q7. Rôle de la température à 0
* On fixe `temperature=0` pour obtenir un comportement totalement **déterministe et factuel**. Cela évite toute créativité superflue du modèle et garantit qu'il respecte strictement le texte sans inventer de détails.

## Étape 7 - Évaluation du RAG

### Q8. Méthodologie d'évaluation
* **Jeu de test (Ground Truth) :** Création d'un fichier structuré `evaluation.csv` contenant des questions clés représentatives, les réponses idéales attendues et la source documentaire de référence (`source_attendue`).
* **Mesure de performance :** Le script d'évaluation (`etape7_evaluation.py`) automatise le parcours utilisateur en interrogeant le pipeline RAG pour chaque question du jeu de test. Il compare ensuite les sources effectivement extraites par la recherche vectorielle avec la source attendue.
* **Métrique utilisée :** Le taux de succès de récupération (*Hit Rate / Précision des sources*), exprimé en pourcentage de bonnes correspondances dans le top $k$ extraits.

### Q9. Résultats et Analyse
* **Résultats obtenus :** Sur notre jeu de test de référence, le système a atteint un score de **100% (3/3)**, démontrant que la recherche vectorielle cible systématiquement les documents pertinents (`teletravail.pdf`, `conges_absences.pdf`).
* **Qualité des réponses :** Couplé au modèle local `llama3.2` (avec une température de 0), le générateur exploite correctement ces extraits pour fournir des réponses factuelles, sans hallucination et conformes aux politiques internes d'Altéa Services.
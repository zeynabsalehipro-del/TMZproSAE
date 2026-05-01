# Partie B — Gestion des Destinations
**Auteur : Teodora — Membre B**
Projet SAE — Université Sorbonne Paris Nord

---

## Responsabilités

- **Backend** : Création des routes pour ajouter des étapes à un voyage
- **Base de données** : Modélisation de la relation One-to-Many (Voyage → Destinations)
- **DevOps** : Gestion des volumes Docker pour la persistance des données

---

## Fichiers

```
app/
├── models_b.py    → Modèle SQLAlchemy : table 'destinations'
├── schemas_b.py   → Schémas Pydantic  : validation et réponses API
├── crud_b.py      → Fonctions CRUD    : accès base de données
└── routes_b.py    → Routes FastAPI    : router à inclure dans main.py
```

---

## Relation implémentée : One-to-Many

```
voyages (Mathurin — Membre A)       destinations (Teodora — Membre B)
─────────────────────────────       ──────────────────────────────────
voyage_id  PK                  ←──  voyage_id  FK  (ON DELETE CASCADE)
date                                destination_id  PK
lieu                                nom             (obligatoire)
voyage_fini                         localisation    (optionnel)
prix                                categorie       hotel | activite | restaurant
                                    notes           (optionnel)
                                    ordre           position dans l'itinéraire
```

**Un voyage contient plusieurs destinations.**
Si un voyage est supprimé, toutes ses destinations sont supprimées automatiquement (CASCADE).

---

## Routes exposées

| Méthode  | URL                                   | Description                     | Code succès |
|----------|---------------------------------------|---------------------------------|-------------|
| `POST`   | `/voyages/{voyage_id}/destinations/`  | Ajouter une étape à un voyage   | 201         |
| `GET`    | `/voyages/{voyage_id}/destinations/`  | Lister les étapes d'un voyage   | 200         |
| `GET`    | `/destinations/{destination_id}`      | Détail d'une étape              | 200         |
| `PUT`    | `/destinations/{destination_id}`      | Modifier une étape (partiel)    | 200         |
| `DELETE` | `/destinations/{destination_id}`      | Supprimer une étape             | 200         |

---

## Validations (schemas_b.py)

- `nom` : obligatoire, ne peut pas être vide
- `categorie` : doit être `hotel`, `activite` ou `restaurant` (ou null)
- `ordre` : doit être >= 1 (ou null)
- Requête sur `voyage_id` inexistant → **404**
- Données invalides → **422 Validation Error**

---

## Intégration dans le projet commun

### 1. Ajouter le modèle dans `models.py`

```python
from .models_b import Destination  # ← ajouter avant create_all()
```

### 2. Ajouter les routes dans `main.py`

```python
from app.routes_b import router as router_destinations  # ← ajouter
app.include_router(router_destinations)                 # ← ajouter
```

### 3. Ajouter la table dans le script SQL commun

Ajouter après la création de la table `voyages` :

```sql
CREATE TABLE IF NOT EXISTS destinations (
    destination_id  SERIAL PRIMARY KEY,
    nom             VARCHAR(100)  NOT NULL,
    localisation    VARCHAR(100),
    categorie       VARCHAR(50)   CHECK (categorie IN ('hotel', 'activite', 'restaurant')),
    notes           VARCHAR(255),
    ordre           INTEGER       CHECK (ordre >= 1),
    voyage_id       INTEGER       NOT NULL,
    FOREIGN KEY (voyage_id) REFERENCES voyages(voyage_id) ON DELETE CASCADE
);
```

---

## Exemple d'utilisation

**Créer une destination :**
```json
POST /voyages/1/destinations/
{
    "nom": "Colisée",
    "localisation": "Rome, Italie",
    "categorie": "activite",
    "notes": "Réserver les billets en avance.",
    "ordre": 1
}
```

**Réponse (201) :**
```json
{
    "destination_id": 1,
    "nom": "Colisée",
    "localisation": "Rome, Italie",
    "categorie": "activite",
    "notes": "Réserver les billets en avance.",
    "ordre": 1,
    "voyage_id": 1
}
```

**Mise à jour partielle :**
```json
PUT /destinations/1
{
    "notes": "Billet gratuit le premier dimanche du mois."
}
```
Seul le champ `notes` est modifié. Les autres restent inchangés.

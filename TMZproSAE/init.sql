-- =============================================================
-- TMZproSAE — Script SQL complet
-- Crée les tables et insère des données de test
-- =============================================================

-- Membre A (Mathurin) — Tables originales
CREATE TABLE IF NOT EXISTS utilisateurs (
    utilisateur_id  SERIAL PRIMARY KEY,
    email           VARCHAR(100) NOT NULL UNIQUE,
    prenom          VARCHAR(100) NOT NULL,
    nom             VARCHAR(100) NOT NULL,
    age             INTEGER      NOT NULL CHECK (age >= 0),
    mdp             VARCHAR(255) NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS voyages (
    voyage_id   SERIAL  PRIMARY KEY,
    date        DATE    NOT NULL,
    lieu        VARCHAR(100) NOT NULL,
    voyage_fini BOOLEAN NOT NULL,
    prix        NUMERIC(10,2) NOT NULL CHECK (prix >= 0)
);

CREATE TABLE IF NOT EXISTS relation_utilisateur_voyage (
    utilisateur_id  INTEGER NOT NULL,
    voyage_id       INTEGER NOT NULL,
    PRIMARY KEY (utilisateur_id, voyage_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(utilisateur_id) ON DELETE CASCADE,
    FOREIGN KEY (voyage_id)      REFERENCES voyages(voyage_id)           ON DELETE CASCADE
);

-- Membre B — Destinations (One-to-Many avec voyages)
CREATE TABLE IF NOT EXISTS destinations (
    destination_id  SERIAL PRIMARY KEY,
    nom             VARCHAR(100) NOT NULL,
    localisation    VARCHAR(100),
    categorie       VARCHAR(50)  CHECK (categorie IN ('hotel', 'activite', 'restaurant')),
    notes           VARCHAR(255),
    ordre           INTEGER      CHECK (ordre >= 1),
    voyage_id       INTEGER      NOT NULL,
    FOREIGN KEY (voyage_id) REFERENCES voyages(voyage_id) ON DELETE CASCADE
);

-- Membre C (Zeynab) — Budget (One-to-One avec voyages)
CREATE TABLE IF NOT EXISTS budgets (
    id           SERIAL PRIMARY KEY,
    total_amount FLOAT,
    spent_amount FLOAT DEFAULT 0.0,
    trip_id      INTEGER UNIQUE,
    FOREIGN KEY (trip_id) REFERENCES voyages(voyage_id)
);

-- =============================================================
-- Données de test
-- =============================================================

INSERT INTO utilisateurs (email, prenom, nom, age, mdp) VALUES
    ('alice@example.com',   'Alice',   'Martin',  28, 'mdp_alice'),
    ('bob@example.com',     'Bob',     'Dupont',  34, 'mdp_bob'),
    ('charlie@example.com', 'Charlie', 'Bernard', 22, 'mdp_charlie');

INSERT INTO voyages (date, lieu, voyage_fini, prix) VALUES
    ('2024-06-15', 'Rome, Italie',       FALSE, 800.00),
    ('2024-07-20', 'Barcelone, Espagne', FALSE, 1200.00),
    ('2024-08-10', 'Paris, France',      TRUE,  650.00);

INSERT INTO relation_utilisateur_voyage (utilisateur_id, voyage_id) VALUES
    (1, 1), (2, 1),
    (1, 2), (2, 2), (3, 2),
    (3, 3);

INSERT INTO destinations (nom, localisation, categorie, notes, ordre, voyage_id) VALUES
    ('Colisée',           'Rome, Italie',       'activite',   'Réserver les billets en avance.',        1, 1),
    ('Hôtel Panthéon',    'Rome, Italie',       'hotel',      'Chambre double, petit-déjeuner inclus.', 2, 1),
    ('Trattoria da Enzo', 'Rome, Italie',       'restaurant', 'Spécialités romaines, réserver.',        3, 1),
    ('Sagrada Família',   'Barcelone, Espagne', 'activite',   'Visiter le matin pour éviter la foule.', 1, 2),
    ('Hotel Arts',        'Barcelone, Espagne', 'hotel',      'Vue sur la plage de la Barceloneta.',    2, 2),
    ('La Boqueria',       'Barcelone, Espagne', 'restaurant', 'Marché couvert, idéal pour le lunch.',   3, 2),
    ('Tour Eiffel',       'Paris, France',      'activite',   'Monter au 2ème étage.',                  1, 3),
    ('Hôtel Lutetia',     'Paris, France',      'hotel',      'Hôtel historique Saint-Germain.',        2, 3);

INSERT INTO budgets (total_amount, spent_amount, trip_id) VALUES
    (800.00,  320.50, 1),
    (1200.00, 675.00, 2),
    (650.00,  650.00, 3);

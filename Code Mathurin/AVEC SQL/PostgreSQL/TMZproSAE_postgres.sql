CREATE TABLE utilisateurs (
	utilisateur_id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    age INT NOT NULL CHECK (age >= 0),
    mdp VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE voyages (
    voyage_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    lieu VARCHAR(100) NOT NULL,
    voyage_fini BOOLEAN NOT NULL,
    prix NUMERIC(10,2) NOT NULL CHECK (prix >= 0)
);

CREATE TABLE relation_utilisateur_voyage (
    utilisateur_id INT NOT NULL,
    voyage_id INT NOT NULL,

    PRIMARY KEY (utilisateur_id, voyage_id),

    FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateurs(utilisateur_id)
        ON DELETE CASCADE,

    FOREIGN KEY (voyage_id)
        REFERENCES voyages(voyage_id)
        ON DELETE CASCADE
);

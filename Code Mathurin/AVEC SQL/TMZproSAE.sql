CREATE DATABASE TMZproSAE CHARACTER SET utf8mb4;
USE TMZproSAE;

CREATE TABLE utilisateurs (
	utilisateur_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    age INT NOT NULL CHECK (age >= 0),
    mdp VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE voyages (
    voyage_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    lieu VARCHAR(100) NOT NULL,
    voyage_fini BOOLEAN NOT NULL,
    prix INT NOT NULL CHECK (prix >= 0)
);

CREATE TABLE relation_utilisateur_voyage (
	email VARCHAR(100) NOT NULL,
    voyage_id INT NULL CHECK (voyage_id >= 0)
);

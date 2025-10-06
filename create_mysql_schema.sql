CREATE DATABASE IF NOT EXISTS vaccination_db;
USE vaccination_db;
SET NAMES utf8mb4;

-- Table utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    role ENUM('parent', 'médecin', 'admin'),
    email VARCHAR(100) UNIQUE,
    mot_de_passe VARCHAR(255)
);

-- Table enfants
CREATE TABLE IF NOT EXISTS enfants (
    id_enfant INT AUTO_INCREMENT PRIMARY KEY,
    prenom VARCHAR(50),
    nom VARCHAR(50),
    sexe ENUM('M', 'F'),
    date_naissance DATE,
    historique_medical TEXT,
    parent_id INT,
    FOREIGN KEY (parent_id) REFERENCES utilisateurs(id_utilisateur)
);

-- Table vaccins
CREATE TABLE IF NOT EXISTS vaccins (
    vaccin_id INT AUTO_INCREMENT PRIMARY KEY,
    nom_vaccin VARCHAR(100),
    age_recommande INT,
    nombre_doses INT,
    effets_secondaires TEXT,
    type_vaccin VARCHAR(50),
    maladies_ciblees TEXT
);

-- Table vaccinations
CREATE TABLE IF NOT EXISTS vaccinations (
    id_vaccination INT AUTO_INCREMENT PRIMARY KEY,
    id_enfant INT,
    vaccin_id INT,
    date_vaccination DATE,
    dose INT,
    statut_vaccination ENUM('à jour', 'en retard'),
    FOREIGN KEY (id_enfant) REFERENCES enfants(id_enfant),
    FOREIGN KEY (vaccin_id) REFERENCES vaccins(vaccin_id)
);

-- Données utilisateurs
INSERT INTO utilisateurs (role, email, mot_de_passe) VALUES
('parent', 'parent1@example.com', '$2b$12$5sYgJKtN1IbU/jMLxxZxGOy6Nf8jp9ceqfYtO4fwqtdChXqEz3ZTa'),
('parent', 'parent2@example.com', '$2b$12$5sYgJKtN1IbU/jMLxxZxGOy6Nf8jp9ceqfYtO4fwqtdChXqEz3ZTa'),
('parent', 'parent3@example.com', '$2b$12$5sYgJKtN1IbU/jMLxxZxGOy6Nf8jp9ceqfYtO4fwqtdChXqEz3ZTa'),
('médecin', 'medecin1@example.com', '$2b$12$A0jTQxlI1QLaHkIq7Q0AS.cMY2Zhz7I.9eZ2OT9.TCDmxWYY46Ymi'),
('admin', 'admin1@example.com', '$2b$12$FlIUdXlnFfJXgRMuzywTJuZFCmj8MxKXEVxPPr8oj9ItRvnhM9f6e');

-- Données enfants 
INSERT INTO enfants (prenom, nom, sexe, date_naissance, historique_medical, parent_id) VALUES
('Ali', 'Benali', 'M', '2017-05-10', 'Aucun', 1),
('Sara', 'Benali', 'F', '2019-08-22', 'Asthme', 1),
('Youssef', 'El Idrissi', 'M', '2018-03-15', 'Allergie au pollen', 2),
('Aya', 'Bennani', 'F', '2020-02-15', 'Diabète de type 1', 2),
('Hamza', 'Bouzid', 'M', '2016-09-01', 'Antécédents d''épilepsie', 3),
('Khadija', 'Makki', 'F', '2019-06-21', 'Antécédents familiaux d''asthme', 3);

-- Données vaccins 
INSERT INTO vaccins (nom_vaccin, age_recommande, nombre_doses, effets_secondaires, type_vaccin, maladies_ciblees) VALUES
('BCG', 0, 1, 'Rougeur locale, fièvre légère', 'Vaccin vivant atténué', 'Tuberculose'),
('Hépatite B', 0, 3, 'Fatigue, fièvre légère', 'Vaccin inactivé', 'Hépatite B'),
('VPO (Polio)', 0, 4, 'Nausée, fatigue', 'Vaccin vivant atténué', 'Poliomyélite'),
('DTC (Diphtérie, Tétanos, Coqueluche)', 2, 3, 'Fièvre, douleur', 'Vaccin inactivé', 'Diphtérie, Tétanos, Coqueluche'),
('Hib', 2, 3, 'Fièvre, irritabilité', 'Vaccin conjugué', 'Méningite, pneumonie'),
('Pneumocoque', 2, 3, 'Fièvre, douleur locale', 'Vaccin conjugué', 'Infections à pneumocoque'),
('Rotavirus', 2, 2, 'Diarrhée, irritabilité', 'Vaccin oral vivant atténué', 'Gastro-entérite à rotavirus'),
('Rougeole', 9, 1, 'Fièvre, éruption', 'Vaccin vivant atténué', 'Rougeole'),
('ROR', 12, 1, 'Fièvre, ganglions', 'Vaccin vivant atténué', 'Rougeole, Oreillons, Rubéole'),
('Varicelle', 12, 1, 'Éruption, fièvre', 'Vaccin vivant atténué', 'Varicelle');

-- Données vaccinations 
INSERT INTO vaccinations (id_enfant, vaccin_id, date_vaccination, dose, statut_vaccination) VALUES
(1, 1, '2017-05-20', 1, 'à jour'),
(1, 2, '2017-07-20', 1, 'à jour'),
(1, 3, '2017-09-20', 1, 'à jour'),
(2, 1, '2019-08-30', 1, 'à jour'),
(2, 4, '2019-10-01', 1, 'en retard'),
(3, 5, '2018-04-01', 1, 'à jour'),
(3, 6, '2018-06-01', 1, 'à jour'),
(4, 7, '2020-04-10', 1, 'à jour'),
(4, 8, '2021-01-10', 1, 'à jour'),
(5, 9, '2017-12-10', 1, 'en retard'),
(5, 10, '2018-01-20', 1, 'à jour'),
(6, 2, '2019-07-01', 1, 'à jour'),
(6, 3, '2019-09-01', 1, 'à jour');

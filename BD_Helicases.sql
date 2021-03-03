/* Commande utiles (dans le terminal):
sudo mysql -> lance mysql
show databases; -> montre les bdd exixtantes
use `nom_bdd`; -> attach à une bdd pour travailler dessus
show tables; -> montre les tables dans la bdd
*/
DROP DATABASE IF EXISTS Helicases_Project;
CREATE DATABASE Helicases_Project; 
USE Helicases_Project; 


CREATE TABLE IF NOT EXISTS PROTEINS_COG
(
    `id_uniprot` VARCHAR(30),
    `id_cog` VARCHAR(30),
     PRIMARY KEY(`id_uniprot`, `id_cog`)
);

CREATE TABLE IF NOT EXISTS COG(
    `id_cog` VARCHAR(30) UNIQUE,
    `description` VARCHAR(100),
    `category` VARCHAR(30),
    `species_count` VARCHAR(10),
    `proteins_count` VARCHAR(10),
    PRIMARY KEY(`id_cog`)
);

CREATE TABLE IF NOT EXISTS MULTIPLE_STATUS(
    `client_id` VARCHAR(30),
    `id_uniprot`VARCHAR(30),
    `multiple`VARCHAR(30),
    `predicted_by`VARCHAR(30),
    PRIMARY KEY(`client_id`)
);


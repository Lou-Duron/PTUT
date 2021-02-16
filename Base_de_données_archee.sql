/* Commande utiles (dans le terminal):
sudo mysql -> lance mysql
show databases; -> montre les bdd exixtantes
use `nom_bdd`; -> attach à une bdd pour travailler dessus
show tables; -> montre les tables dans la bdd
*/

CREATE DATABASE IF NOT EXISTS `ptut`; --création de la bdd
USE `ptut`; -- attach à la bdd
SHOW TABLES; -- visualistation des tables  

--Création des tables
CREATE TABLE IF NOT EXISTS `table_1`
(
    `id_petra` VARCHAR(30) UNIQUE,
    `id_uniprot` VARCHAR(30),
    `id_cog` VARCHAR(30),
    `statut` VARCHAR(30),
    `multiple` VARCHAR(10)    
);

DESCRIBE `table_1`; --pour afficher le contenu de la table
--NUMBER ???
--PRIMARY KEY ???

CREATE TABLE IF NOT EXISTS `table_2`(
    `id_cog` VARCHAR(30) UNIQUE,
    `description` VARCHAR(100),
    `type` VARCHAR(30),
    `species_count` NUMBER(10),
    `proteins_count` NUMBER(10),
    PRIMARY KEY(`id_cog`)
);

CREATE TABLE IF NOT EXISTS `table_3`(
    `genome_id_gold` VARCHAR(30) UNIQUE,
    `id_petra` VARCHAR(30),
    `id_assembly`VARCHAR(30),
    PRIMARY KEY(`id_petra`)
);

/*Test insertion*/
/*À automatiser*/

/*INSERT INTO 'archee' VALUES ('fds', 'dsffsd', 45);
INSERT INTO 'archee' VALUES ('ffs', 'dsfdgfd', 76);
INSERT INTO 'archee' VALUES ('ftyj', 'dsfgdfgd', 26);
INSERT INTO 'archee' VALUES ('jytjt', 'djtyjdfgtd', 73);
INSERT INTO 'archee' VALUES ('jtyjt', 'dstyjd', 76);*/

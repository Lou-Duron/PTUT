DROP DATABASE IF EXISTS 'test_ptut';
CREATE DATABASE IF NOT EXISTS 'test_ptut';
USE 'test_ptut';


/*Création d'une table*/

CREATE TABLE IF NOT EXISTS 'archee'(
    'id' VARCHAR(30) UNIQUE,
    'truc' VARCHAR(10),
    'machin' NUMBER(10),
    PRIMARY KEY('id')
);

/*Test insertion*/
/*À automatiser*/

INSERT INTO 'archee' VALUES ('fds', 'dsffsd', 45);
INSERT INTO 'archee' VALUES ('ffs', 'dsfdgfd', 76);
INSERT INTO 'archee' VALUES ('ftyj', 'dsfgdfgd', 26);
INSERT INTO 'archee' VALUES ('jytjt', 'djtyjdfgtd', 73);
INSERT INTO 'archee' VALUES ('jtyjt', 'dstyjd', 76);

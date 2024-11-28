DROP DATABASE IF EXISTS pays;
Create DATABASE pays;
USE  pays;
CREATE TABLE voyages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    originpays VARCHAR(255),
    vacancespays VARCHAR(255),
    spentdays VARCHAR(255)
);

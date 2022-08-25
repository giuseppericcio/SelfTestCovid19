DROP TABLE IF EXISTS Farmacie;

CREATE TABLE `Farmacie` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	NomeFarmacia VARCHAR(50),
	Citta VARCHAR(50),
	CAP INT(5),
	Email VARCHAR(50),
	PWD VARCHAR(50)
);

INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Email, PWD) VALUES ('Don Bosco','Napoli','80001','donbosco@farmacia.it','prova1');

INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Email, PWD) VALUES ('Mastrelia','Napoli','80001','mastrelia@farmacia.it','prova2');
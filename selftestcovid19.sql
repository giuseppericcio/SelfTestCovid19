DROP TABLE IF EXISTS Farmacie;
DROP TABLE IF EXISTS Prenotazioni;

CREATE TABLE `Farmacie` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	NomeFarmacia VARCHAR(50),
	Citta VARCHAR(50),
	CAP INT(5),
	Email VARCHAR(50),
	PWD VARCHAR(50)
);

CREATE TABLE `Prenotazioni` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	Nome VARCHAR(50),
	Cognome VARCHAR(50),
	Email VARCHAR(50),
	PWD VARCHAR(50),
	CodiceFiscale VARCHAR(36),
	Telefono VARCHAR(10),
	Giorno DATE,
	Ora TIME,
	EsitoTampone VARCHAR(8)
);

CREATE TABLE `Tamponi` (
	ID_tamponi INTEGER PRIMARY KEY AUTOINCREMENT,
	NomeTampone VARCHAR(50),
	Tipo VARCHAR(10),
	N_pezzi INTEGER,
	Prezzo FLOAT
);

UPDATE Prenotazioni SET EsitoTampone = 'Positivo' WHERE ID = 1;


INSERT INTO Tamponi (NomeTampone, Tipo, N_pezzi, Prezzo) VALUES ('Tamporum', 'Rapido', 20,15.0);
INSERT INTO Tamponi (NomeTampone, Tipo, N_pezzi, Prezzo) VALUES ('DazTamp', 'Molecolare', 20,15.0);

INSERT INTO Prenotazioni (Nome, Cognome, Email, PWD, CodiceFiscale, Telefono, Giorno, Ora) VALUES ('Gino', 'Pino', 'gino@gmail.com','prova','GNOPNOLX12HJ', '3333233212','26-08-2022','11:00');
INSERT INTO Prenotazioni (Nome, Cognome, Email, PWD, CodiceFiscale, Telefono, Giorno, Ora) VALUES ('Ciccio', 'Verde', 'cicc@gmail.com','prova1','GMOVRELX13HJ', '3332355789','26-08-2022','11:15');
INSERT INTO Prenotazioni (Nome, Cognome, Email, PWD, CodiceFiscale, Telefono, Giorno, Ora) VALUES ('Giacomino', 'Pilopino', 'giacc@gmail.com','prova2','GNOPNOLX12HJ', '3334566654','26-08-2022','11:30');

INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Email, PWD) VALUES ('Don Bosco','Napoli','80001','donbosco@farmacia.it','prova1');

INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Email, PWD) VALUES ('Mastrelia','Napoli','80001','mastrelia@farmacia.it','prova2');

SELECT SUM(Prezzo) AS TOT FROM Tamponi WHERE Tipo = 'Rapido';
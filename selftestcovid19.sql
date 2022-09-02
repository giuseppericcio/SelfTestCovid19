DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Farmacie;
DROP TABLE IF EXISTS Prenotazioni;
DROP TABLE IF EXISTS Tamponi;
DROP TABLE IF EXISTS Orari;
DROP TABLE IF EXISTS Pazienti;

CREATE TABLE `Admin` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	Username VARCHAR(50),
	PWD VARCHAR(50)
);

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
	CodiceFiscale VARCHAR(36),
	Telefono VARCHAR(10),
	Giorno DATE,
	Ora TIME,
	EsitoTampone VARCHAR(20),
	ID_Farmacia INTEGER
);

CREATE TABLE `Tamponi` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	NomeTampone VARCHAR(50),
	Tipo VARCHAR(10),
	N_pezzi INTEGER,
	Giorno DATE,
	OraInizio TIME,
	OraFine TIME,
	Prezzo FLOAT,
	ID_Farmacia INTEGER
);

CREATE TABLE `Orari` (
	ID_Tampone INTEGER,
	Giorno DATE,
	Orario TIME,
	PRIMARY KEY ("ID_Tampone","Giorno","Orario")
);

CREATE TABLE `Pazienti` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	Nome VARCHAR(50),
	Cognome VARCHAR(50),
	Email VARCHAR(50),
	PWD VARCHAR(50),
	CodiceFiscale VARCHAR(36),
	Telefono VARCHAR(10)
);

INSERT INTO Admin (Username,PWD) VALUES ('admin','admin');

INSERT INTO Tamponi (NomeTampone, Tipo, N_pezzi, Giorno, OraInizio, OraFine, Prezzo, ID_Farmacia) VALUES ('Tamporum', 'Rapido', 20,'2022-08-26','11:00', '11:15',15.0, 1);
INSERT INTO Tamponi (NomeTampone, Tipo, N_pezzi, Giorno, OraInizio, OraFine, Prezzo, ID_Farmacia) VALUES ('DazTamp', 'Molecolare', 20,'2022-08-26','11:15', '11:30',15.0, 2);

INSERT INTO Prenotazioni (Nome, Cognome, Email, CodiceFiscale, Telefono, Giorno, Ora, EsitoTampone, ID_Farmacia) VALUES ('Gino', 'Pino', 'gino@gmail.com','GNOPNOLX12HJ', '3333233212','2022-08-26','11:00','Negativo',1);
INSERT INTO Prenotazioni (Nome, Cognome, Email, CodiceFiscale, Telefono, Giorno, Ora, EsitoTampone, ID_Farmacia) VALUES ('Ciccio', 'Verde', 'cicc@gmail.com','GMOVRELX13HJ', '3332355789','2022-08-26','11:15','Negativo',2);
INSERT INTO Prenotazioni (Nome, Cognome, Email, CodiceFiscale, Telefono, Giorno, Ora, EsitoTampone, ID_Farmacia) VALUES ('Giacomino', 'Pilopino', 'giacc@gmail.com','GNOPNOLX12HJ', '3334566654','2022-08-26','11:30','Negativo',1);

INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Email, PWD) VALUES ('Don Bosco','Napoli','80001','donbosco@farmacia.it','prova1');
INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Email, PWD) VALUES ('Mastrelia','Napoli','80001','mastrelia@farmacia.it','prova2');

INSERT INTO Pazienti (Nome, Cognome, Email, PWD, CodiceFiscale, Telefono) VALUES ('Gino', 'Pino', 'gino@gmail.com', 'prova1','GNOPNOLX12HJ', '3333233212');
INSERT INTO Pazienti (Nome, Cognome, Email, PWD, CodiceFiscale, Telefono) VALUES ('Ciccio', 'Verde', 'cicc@gmail.com', 'prova2','GMOVRELX13HJ', '3332355789');
INSERT INTO Pazienti (Nome, Cognome, Email, PWD, CodiceFiscale, Telefono) VALUES ('Giacomino', 'Pilopino', 'giacc@gmail.com', 'prova3','GNOPNOLX12HJ', '3334566654');

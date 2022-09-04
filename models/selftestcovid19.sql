DROP TABLE IF EXISTS Admin;

CREATE TABLE `Admin` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	Username VARCHAR(50),
	PWD VARCHAR(50),
	UNIQUE(Username,PWD)
);

CREATE TABLE IF NOT EXISTS `Farmacie` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	NomeFarmacia VARCHAR(50),
	Citta VARCHAR(50),
	CAP INT(5),
	Indirizzo VARCHAR(50),
	Email VARCHAR(50),
	PWD VARCHAR(50),
	UNIQUE(NomeFarmacia,Email)
);

CREATE TABLE IF NOT EXISTS `Prenotazioni` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	Nome VARCHAR(50),
	Cognome VARCHAR(50),
	Email VARCHAR(50),
	CodiceFiscale VARCHAR(36),
	Telefono VARCHAR(10),
	Giorno DATE,
	Ora TIME,
	TipoTampone VARCHAR(10),
	EsitoTampone VARCHAR(20),
	ID_Farmacia INTEGER,
	ID_Paziente INTEGER,
	ID_Tampone INTEGER
);

CREATE TABLE IF NOT EXISTS `Tamponi` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	NomeTampone VARCHAR(50),
	Tipo VARCHAR(10),
	N_pezzi INTEGER,
	Giorno DATE,
	OraInizio TIME,
	OraFine TIME,
	Prezzo FLOAT,
	ID_Farmacia INTEGER,
	UNIQUE(NomeTampone,ID_Farmacia)
);

CREATE TABLE IF NOT EXISTS `Orari` (
	ID_Tampone INTEGER,
	Giorno DATE,
	Orario TIME,
	PRIMARY KEY ("ID_Tampone","Giorno","Orario")
);

CREATE TABLE IF NOT EXISTS `Pazienti` (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	Nome VARCHAR(50),
	Cognome VARCHAR(50),
	Email VARCHAR(50),
	PWD VARCHAR(50),
	CodiceFiscale VARCHAR(36),
	Telefono VARCHAR(10),
	UNIQUE(Email,PWD)
);

INSERT INTO Admin (Username,PWD) VALUES ('admin','admin');
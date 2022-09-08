import pytest
from main import app

@pytest.fixture
def client():
    
    app.config["TESTING"] = True
    app.testing = True

    client = app.test_client()
    with app.app_context():
        yield client

#--------INSERIMENTO SINTOMI--------
def test_InserimentoSintomi_corretto(client):

    sintomi = {
        'Breathing Problem' : '0',
        'Fever' : '1',
        'Dry Cough' : '1',
        'Sore throat' : '0',
        'Running Nose' : '0',
        'Asthma' : '0',
        'Chronic Lung Disease' : '1',
        'Headache' : '0',
        'Heart Disease' : '1',
        'Diabetes' : '0',
        'Hyper Tension' : '0',
        'Fatigue ' : '0',
        'Gastrointestinal ' : '1',
        'Abroad travel' : '0',
        'Contact with COVID Patient' : '1',
        'Attended Large Gathering' : '0',
        'Visited Public Exposed Places' : '1',
        'Family working in Public Exposed Places' : '0',
        'Wearing Masks' : '1',
        'Sanitization from Market' : '0'
    }

    rv = client.post("/", data=sintomi)
    assert rv.status_code == 200

def test_InserimentoSintomi_sbagliato(client):

    #---CAMPI VUOTI---
    with pytest.raises(ValueError):
        sintomi = {
            'Breathing Problem' : '0',
            'Fever' : '0',
            'Dry Cough' : '1',
            'Sore throat' : '0',
            'Running Nose' : '1',
            'Asthma' : '0',
            'Chronic Lung Disease' : '',
            'Headache' : '0',
            'Heart Disease' : '',
            'Diabetes' : '0',
            'Hyper Tension' : '1',
            'Fatigue ' : '0',
            'Gastrointestinal ' : '0',
            'Abroad travel' : '0',
            'Contact with COVID Patient' : '1',
            'Attended Large Gathering' : '',
            'Visited Public Exposed Places' : '1',
            'Family working in Public Exposed Places' : '0',
            'Wearing Masks' : '0',
            'Sanitization from Market' : ''
        }
        client.post("/", data=sintomi)

#--------PRENOTAZIONE TAMPONE - NUOVO PAZIENTE--------
def test_prenotaNuovo_corretto(client):
    ID_farmacia = 2
    ID_tampone = 4
    Giorno = "2022-09-07"

    info_paziente = {
        "Ora": "09:00",
        "Nome": "Marco",
        "Cognome": "Ricci",
        "Email": "marco.ric@paziente.it",
        "PWD": "prova22",
        "CodiceFiscale": "mrsfff67f43l456t",
        "Telefono": "3456677891"
    }

    rv = client.post("/"+str(ID_farmacia)+"/"+str(ID_tampone)+"/"+str(Giorno)+"/confermaPrenotaNuovo", data=info_paziente)
    assert rv.status_code == 200

def test_prenotaNuovo_sbagliato(client):
    ID_farmacia = 2
    ID_tampone = 4
    Giorno = "2022-09-07"

    #---PAZIENTE GIA' REGISTRATO---
    info_paziente = {
        "Ora": "10:00",
        "Nome": "Giusepp",
        "Cognome": "Riccio",
        "Email": "peppercc99@gmail.com",
        "PWD": "prova123",
        "CodiceFiscale": "rccgpp99d22l259v",
        "Telefono": "3456677891"
    }

    rv = client.post("/"+str(ID_farmacia)+"/"+str(ID_tampone)+"/"+str(Giorno)+"/confermaPrenotaNuovo", data=info_paziente)
    assert rv.status_code == 200

#--------PRENOTAZIONE TAMPONE - PAZIENTE REGISTRATO--------
def test_prenotaRegistrato_corretto(client):
    ID_farmacia = 2
    ID_tampone = 4
    Giorno = "2022-09-07"

    info_paziente = {
        "Ora": "11:00",
        "Email": "peppercc99@gmail.com",
        "PWD": "prova123"
    }

    rv = client.post("/"+str(ID_farmacia)+"/"+str(ID_tampone)+"/"+str(Giorno)+"/confermaPrenotaRegistrato", data=info_paziente)
    assert rv.status_code == 200

def test_prenotaRegistrato_sbagliato(client):
    ID_farmacia = 2
    ID_tampone = 4
    Giorno = "2022-09-07"

    #---PAZIENTE NON REGISTRATO---
    info_paziente = {
        "Ora": "12:00",
        "Email": "fabio.par@paziente.it",
        "PWD": "prova145"
    }

    rv = client.post("/"+str(ID_farmacia)+"/"+str(ID_tampone)+"/"+str(Giorno)+"/confermaPrenotaRegistrato", data=info_paziente)
    assert rv.status_code == 200

#--------VERIFICA DISPONIBILITA' FARMACIE--------
def test_dispRapido_corretto(client):

    info_farmacia = {
        "NomeFarmacia": "Don Bosco",
        "Citta": "Napoli",
        "CAP": "80100"
    }

    rv = client.post("/disponibilitaRapido", data=info_farmacia)
    assert rv.status_code == 200

def test_dispRapido_sbagliato(client):

    #---FORMATO INFO NON VALIDE---
    info_farmacia = {
        "NomeFarmacia": "80100",
        "Citta": "Napoli",
        "CAP": "Don Bosco"
    }

    rv = client.post("/disponibilitaRapido", data=info_farmacia)
    assert rv.status_code == 200

def test_dispMolecolare_corretto(client):

    info_farmacia = {
        "NomeFarmacia": "Mastrelia",
        "Citta": "Torre del Greco",
        "CAP": "80059"
    }

    rv = client.post("/disponibilitaMolecolare", data=info_farmacia)
    assert rv.status_code == 200

def test_dispMolecolare_sbagliato(client):

    #---FORMATO INFO NON VALIDE---
    info_farmacia = {
        "NomeFarmacia": "80059",
        "Citta": "Torre del Greco",
        "CAP": "Mastrelia"
    }

    rv = client.post("/disponibilitaMolecolare", data=info_farmacia)
    assert rv.status_code == 200

#--------CREAZIONE DISPONIBILITA' TAMPONI--------
def test_CreaDisponibilitaTampone_corretto(client):

    with client.session_transaction() as session:
        session['loggedin'] = True
        session['id'] = 1
        session['username'] = 'donbosco@farmacia.it'
    
    info_tampone = {
        'NomeTampone' : 'TampCare',
        'Tipo' : 'Rapido',
        'N_pezzi' : '20',
        'Giorno' : '2022-09-07',
        'OraInizio' : '09:00',
        'OraFine' : '18:00',
        'Prezzo' : '20'
    }

    rv = client.post("/creazioneDisponibilitaTamponi", data=info_tampone)
    assert rv.status_code == 200

def test_CreaDisponibilitaTampone_sbagliato(client):

    with client.session_transaction() as session:
        session['loggedin'] = True
        session['id'] = 1
        session['username'] = 'donbosco@farmacia.it'
    
    #---TAMPONE GIA' PRESENTE---
    info_tampone = {
        'NomeTampone' : 'Tamporum',
        'Tipo' : 'Rapido',
        'N_pezzi' : '10',
        'Giorno' : '2022-09-07',
        'OraInizio' : '09:00',
        'OraFine' : '18:00',
        'Prezzo' : '20'
    }

    rv = client.post("/creazioneDisponibilitaTamponi", data=info_tampone)
    assert rv.status_code == 200

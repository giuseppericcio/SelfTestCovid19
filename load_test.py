from datetime import date,timedelta
from random import randrange, randint
from locust import HttpUser, between, task
from main import app

def generate_info():
    ID_farmacia = randint(0,999)
    ID_tampone = randint(0,999)
    start_date = date(2020, 1, 1)
    end_date = date(2022, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    Giorno = start_date + timedelta(days=random_number_of_days)

    return ID_farmacia,ID_tampone,Giorno

class SelfTestCOVID19_test(HttpUser):
    wait_time = between(5, 15)

#--------INSERIMENTO SINTOMI--------
    @task
    def load_main(self):
        self.client.get("/")

#--------VERIFICA DISPONIBILITA' FARMACIE--------
    @task
    def load_dispMolecolare(self):
        self.client.get("/disponibilitaMolecolare")

    @task
    def load_dispRapido(self):
        self.client.get("/disponibilitaRapido")

#--------PRENOTAZIONE TAMPONE--------
    @task
    def load_prenotaNuovo(self):
        ID_farmacia,ID_tampone,Giorno = generate_info()
        self.client.get("/"+str(ID_farmacia)+"/"+str(ID_tampone)+"/"+str(Giorno)+"/prenotaNuovo")

    @task
    def load_prenotaRegistrato(self):
        ID_farmacia,ID_tampone,Giorno = generate_info()
        self.client.get("/"+str(ID_farmacia)+"/"+str(ID_tampone)+"/"+str(Giorno)+"/prenotaRegistrato")

#--------RICHIESTA ESITO TAMPONE--------
    @task
    def load_EsitoTampone(self):
        with app.app_context():
            self.client.get("/dashboardPaziente")

#--------RICHIESTA LISTA PRENOTAZIONI--------
    @task
    def load_ListaPrenotazioni(self):
        with app.app_context():
            self.client.get("/dashboardFarmacia")

#--------CREAZIONE DISPONIBILITA' TAMPONI--------
    @task
    def load_creaDisponibilitaTamponi(self):
        self.client.get("/creazioneDisponibilitaTamponi")

#--------CREAZIONE FARMACIE--------
    @task
    def load_CreaFarmacie(self):
        self.client.get("/creaFarmacia")

#--------RICERCA FARMACIE--------
    @task
    def load_RicercaFarmacie(self):
        self.client.get("/ricercaFarmacia")
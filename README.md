[![Test di Unità](https://github.com/giuseppericcio/SelfTestCovid19/actions/workflows/Unit_Test.yml/badge.svg)](https://github.com/giuseppericcio/SelfTestCovid19/actions/workflows/Unit_Test.yml)
![Downloads](https://img.shields.io/github/downloads/giuseppericcio/SelfTestCovid19/total)
![GitHub](https://img.shields.io/github/license/giuseppericcio/SelfTestCovid19)

<div align="center">
<center><img src="./static/logo.png" width="188"/></center>
</div>

## :triangular_flag_on_post: La Web Application 
Si desidera realizzare il sistema **SelfTest COVID-19** che sulla base dell’esito del test attiva la relativa prenotazione di un tampone in una delle farmacie più vicine al paziente, dunque un semplice servizio gestione prenotazioni tamponi nelle farmacie. 
Il SelfTest è un modello in grado di predire una certa probabilità di infezione al SARS-CoV-2(COVID-19) in base ai sintomi e/o alle malattie che il paziente manifesta e guidarlo a come comportarsi in caso di alta probabilità di infezione.
Ad esempio, se il sistema predice che il paziente X abbia una **probabilità di infezione tra il 75\% e il 100\%** allora verrà consigliato di recarsi in un centro di tamponi (farmacia, ecc. ) e di fare un **tampone molecolare**. Se il sistema predice che il paziente Y abbia una **probabilità di infezione tra il 50\% e il 75\%** allora verrà consigliato di fare un **tampone rapido** alla farmacia più vicina ad esso.

*Il sistema cerca di diminuire il numero di persone che si recano nelle farmacie per effettuare i tamponi al fine di evitare disservizi nelle stesse e per risparmiare sul costo dei tamponi da parte dei pazienti. In che modo? Prevedendo la probabilità potenziale al COVID-19 e in base al valore ottenuto può effettuare o meno una prenotazione del tampone alla farmacia più vicina.*

## :bookmark_tabs: La Documentazione
Indice della documentazione

## :wrench: Tools utilizzati
|                       **FRONT END**                       |                    |
|:---------------------------------------------------------:|--------------------|
| _FRAMEWORK_                                               | BOOTSTRAP          |
| _LANGUAGE_                                                | HTML, CSS, JS      |
|                        **BACK END**                       |                    |
| _FRAMEWORK_                                               | FLASK              |
| _LANGUAGE_                                                | PYTHON             |
| _TESTING_                                                 | PYTEST, LOCUST, GTMETRIX  |
| _DATABASE_                                                | SQLITE             |
| **TOOLS PER IL SUPPORTO ALLA REALIZZAZIONE DEL SOFTWARE** |                    |
| _CODE_                                                    | VISUAL STUDIO CODE |
| _UML DESIGN_                                              | VISUAL PARADIGM    |
| _SCRUM SUPPORT_                                           | JIRA               |
| _WEB HOSTING_                                             | PYTHONANYWHERE     |

## :chart_with_upwards_trend: Diagramma System Context

## :video_camera: Video Demo della Web Application
Si mostrano tutte le funzionalità implementate nella web application, dallo svolgimento del test fino alla gestione delle farmacie aderenti al sistema.

https://user-images.githubusercontent.com/64225083/188891848-4e4ad96a-c5f2-485f-b708-99068c5bee3d.mp4

:warning: **ATTENZIONE** L’applicazione realizzata è solo a scopo dimostrativo, pertanto la probabilità calcolata può risultare incerta giacché, come già detto in precedenza, il dataset è datato e non aggiornato e i sintomi del virus mutano e variano ogni giorno. 

:warning: **ATTENZIONE** I sintomi, malattie e informazioni relative al COVID19 inserite nel selftest non verranno memorizzate. 

## :heavy_check_mark: La Web App è disponibile, basta un browser! 
Al seguente link si può provare la web application 
:link: https://www.selftestcovid19.it/

**Credenziali di accesso**

:sunglasses: ADMIN: *username* **admin** *password* **admin** 

:smiley: FARMACIA: *username* **donbosco@farmacia.it** *password* **prova1** (*puoi cambiare farmacia entrando dall'ADMIN*)

# Gli Autori
- Antonio Romano 
- Giuseppe Riccio

# Progetto realizzato per soli scopi dimostrativi ed educativi
La seguente trattazione è mirata alla realizzazione di un progetto software per l'esame di Software Architecture Design all'**Università degli Studi di Napoli Federico II** seguendo una documentazione adeguata.

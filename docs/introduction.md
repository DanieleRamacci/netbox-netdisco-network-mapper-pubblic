# Documentazione Introduttiva del Progetto

## Panoramica del Progetto

Questo progetto, attualmente in fase di sviluppo, mira a facilitare l'integrazione e la gestione automatizzata delle risorse di rete utilizzando due potenti strumenti: NetBox e Netdisco. Attraverso l'implementazione di script personalizzati, il progetto consente di sincronizzare e gestire efficacemente le informazioni di rete tra queste due piattaforme, sfruttando le loro API per automatizzare processi come l'inventario dei dispositivi, la mappatura delle connessioni di rete, e la documentazione delle configurazioni.


## Indice della Documentazione

- [Introduzione al Progetto](docs/introduction.md): Una panoramica generale del progetto, i suoi obiettivi e le tecnologie coinvolte.

- [API NetBox](docs/api_netbox.md): Dettagli sull'utilizzo delle API di NetBox per la gestione dell'infrastruttura di rete e la documentazione.

- [API Netdisco](docs/api_netdisco.md): Informazioni sull'uso delle API di Netdisco per la scoperta di rete e il tracciamento dei dispositivi.

- [Creazione Hosts in NetBox](docs/create_hosts.md): Guida allo script per il caricamento "sporco" degli host in NetBox, utilizzando dati predefiniti.

- [Creazione Switches in NetBox](docs/create_switches.md): Descrizione dello script per la creazione degli switch in NetBox, inclusa la preparazione e l'arricchimento dei dati.

- [Aggiornamento Switches in NetBox](docs/update_switches.md): Documentazione relativa allo script per l'aggiornamento delle informazioni degli switch in NetBox a partire dai dati di Netdisco.

Per navigare nella documentazione, clicca sui link sopra per accedere direttamente ai file markdown corrispondenti. Questi documenti forniscono una guida dettagliata su come utilizzare e sfruttare al meglio gli script e le integrazioni sviluppate in questo progetto.

## Struttura delle Cartelle

La struttura attuale delle cartelle del progetto è organizzata come segue:

progetto/
│
├── docs/ # Documentazione del progetto
│ ├── api_netbox.md
│ ├── api_netdisco.md
│ ├── create_hosts.md
│ ├── create_switches.md
│ ├── introduction.md
│ └── update_switches.md
│
├── src/ # Codice sorgente degli script
│ ├── ...
│
└── data/ # Dati e file JSON utilizzati dagli script
├── host/
├── switch/
└── tmp (json temporanei per analizzare le risposte e log di errore con timestamp )

## NetBox: Cos'è e Cosa Può Fare

[NetBox](https://demo.netbox.dev/static/docs/) è un sistema di documentazione di rete (IPAM) e di gestione dell'infrastruttura (DCIM) open source. Progettato per la pianificazione e la documentazione delle reti, NetBox aiuta a catalogare e organizzare le seguenti informazioni in modo strutturato:

- **IP Addresses**: Gestione degli indirizzi IP, compresa l'assegnazione e il tracking.
- **Subnets**: Organizzazione e documentazione delle subnet all'interno di una rete.
- **VLANs**: Catalogazione delle VLAN e delle loro proprietà.
- **Devices**: Documentazione dei dispositivi di rete, compresi i server, i switch, e i router.
- **Connections**: Mappatura delle connessioni fisiche e logiche tra dispositivi.
- **Virtual Machines**: Gestione delle macchine virtuali e delle loro relazioni con l'hardware fisico.
- **Data Centers**: Documentazione delle ubicazioni fisiche, compresi i dettagli su rack e spazi.

NetBox offre un'interfaccia utente web intuitiva e delle [API RESTful](https://netbox.apps.atlas.roma1.infn.it/api/schema/swagger-ui/) per l'interazione programmatica, consentendo agli sviluppatori di integrare facilmente NetBox con altri sistemi o di automatizzare processi di gestione della rete.

## Netdisco: Gestione e Scoperta della Rete

Netdisco è un'applicazione web SNMP open source che offre funzionalità di scoperta di rete, tracciamento di indirizzi MAC, e inventario di dispositivi. Utilizzando Netdisco, gli amministratori di rete possono:

- Scoprire automaticamente la topologia di rete.
- Tenere traccia di quali dispositivi sono connessi a quali porte switch.
- Visualizzare le configurazioni di VLAN.
- Cercare dispositivi per indirizzo IP, MAC, nome e altri attributi.
- Visualizzare la storia delle connessioni di un dispositivo o di una porta.

L'interfaccia utente web di Netdisco fornisce un accesso semplice e intuitivo a queste informazioni, mentre l'[API di Netdisco](http://t2-netdisco.roma1.infn.it:5000/swagger-ui/) permette l'integrazione con altri sistemi e la possibilità di automatizzare il monitoraggio e la gestione della rete.

## Integrazione tra NetBox e Netdisco

Il nostro progetto sfrutta le API di NetBox e Netdisco per sincronizzare dati tra le due piattaforme, automatizzando la gestione dell'infrastruttura di rete e migliorando l'efficienza operativa. Gli script sviluppati consentono di:

- Importare automaticamente i dispositivi scoperti da Netdisco in NetBox, completi di dettagli come posizione, ruolo, e configurazione.
- Mantenere aggiornate le informazioni di rete in NetBox basandosi sui dati raccolti da Netdisco.
- Automatizzare processi di documentazione e gestione delle risorse di rete per ridurre errori manuali e migliorare la precisione dei dati.

Per maggiori informazioni su NetBox e Netdisco, visita la documentazione ufficiale di [NetBox](https://demo.netbox.dev/static/docs/) e [Netdisco](http://t2-netdisco.roma1.infn.it:5000/swagger-ui/).

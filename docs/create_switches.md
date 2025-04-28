# Documentazione Script di Creazione Switch in NetBox
## note

Attualmente la funzione di ricerca  def get_switch contenuta dentro api_netdisco si occupa di chiamare la API device di netdisco per recuperare gli switch e lo fa utilizzando come parametro di ricerca location : Tier 2 , a seguito di un inserimento di un nuovo switch ci siamo resi conto che non è stata mantenuta la consistenza nella nomenclatura della location all'interno di netdisco, questo ha comportato il mancato caricamento dei device collegati allo swatlas-08 e lo swatlas-08 stesso. Quindi una azione da intraprendere è quella di avere una nomenclatura uguale per tutte le location degli switch , oppure trovare un modo alternativo per recuperare tutti gli switch.


## Introduzione

Questo script è progettato per automatizzare il processo di creazione degli switch all'interno di NetBox, sfruttando i dati provenienti da Netdisco. Si occupa di autenticarsi presso Netdisco, scaricare i dati degli switch, arricchirli con informazioni su produttore e piattaforma, e infine caricarli in NetBox.

## Configurazione e Dipendenze

Per eseguire questo script, è necessario avere installato Python e le seguenti librerie:

- `requests`
- `json`
- `urllib3`

Assicurati anche di avere accesso alle API di NetBox e Netdisco con le credenziali appropriate.

## Flusso di Lavoro dello Script

1. **Autenticazione Netdisco**: Lo script inizia autenticandosi presso Netdisco per ottenere un token di accesso.

2. **Recupero Switch da Netdisco**: Utilizzando il token, recupera la lista degli switch e le salva in un file JSON.

3. **Arricchimento dei Dati**: Aggiunge ai dati degli switch informazioni su produttore e piattaforma predefiniti, basandosi sui dati disponibili in Netdisco.

4. **Creazione di Produttori in NetBox**: Legge i dati dei produttori da un file JSON e li crea in NetBox.

5. **Recupero Piattaforme e Produttori da NetBox**: Ottiene l'elenco delle piattaforme e dei produttori già presenti in NetBox.

6. **Associazione Piattaforma e Produttore agli Switch**: Associa ad ogni switch le informazioni corrette di piattaforma e produttore basandosi sui dati di NetBox.

7. **Creazione dei Dispositivi in NetBox**: Infine, crea i dispositivi switch in NetBox utilizzando i dati arricchiti.


## Utilizzo

Per eseguire lo script:

```bash
python create_switches.py


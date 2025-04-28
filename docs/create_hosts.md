# Documentazione Script `create_hosts.py`

## Introduzione

Questo script, `create_hosts.py`, è progettato per facilitare il caricamento iniziale "sporco" degli host su NetBox. Il processo prevede l'utilizzo di valori predefiniti per tipo di dispositivo, ruolo, produttore e piattaforma. Non distingue tra IPMI e server e non gestisce le etichette per i dispositivi caricati.

## Configurazione e Dipendenze

Per eseguire correttamente questo script, assicurati di avere installato Python e le seguenti librerie:

- `requests`
- `json`
- `urllib3`

Inoltre, lo script richiede l'accesso alle API di NetBox e Netdisco. Assicurati di avere le credenziali appropriate e di configurare i seguenti percorsi per il salvataggio dei file JSON:

- `file_path_netdisco`: './../data/host/netdisco/'
- `file_path_netbox`: './../data/host/netbox/'
- `file_path_to_load`: './../data/host/to_load/'

## Flusso di Lavoro dello Script

1. **Autenticazione Netdisco**: Prima di tutto, lo script si autentica presso Netdisco per ottenere un token di accesso.

2. **Recupero Switch da Netdisco**: Utilizzando il token, recupera la lista degli switch da Netdisco.

3. **Estrazione Host**: Per ogni switch, lo script estrae gli host associati e recupera informazioni come produttore e versione del sistema operativo.

4. **Aggiunta Informazioni DNS e IP**: Successivamente, per ogni host rilevato, vengono estratti DNS e indirizzi IP e inseriti in un file JSON preparatorio.

5. **Caricamento Host su NetBox**: Infine, utilizzando valori predefiniti per tipo di dispositivo, produttore, piattaforma e ruolo del dispositivo, gli host vengono caricati su NetBox.

## Uso

Per eseguire lo script:

```bash
python create_hosts.py

## Note e Miglioramenti Futuri

### Miglioramenti Proposti

- **Gestione Etichette**: Implementazione di una logica per assegnare etichette accurate ai dispositivi durante il caricamento. Questo aiuterebbe a mantenere l'organizzazione e la categorizzazione dei dispositivi all'interno di NetBox, facilitando la gestione e la ricerca.
  
- **Distinzione IPMI/Server**: Introduzione di un meccanismo per distinguere in modo efficace tra interfacce IPMI e server veri e propri. Ciò è cruciale per assicurare che le informazioni siano corrette e che i dispositivi siano configurati con i ruoli appropriati in NetBox.
  
- **Validazione Dispositivi**: Aggiunta di controlli di validazione per verificare l'accuratezza e la completezza dei dati dei dispositivi prima del loro caricamento su NetBox. Questo passaggio è fondamentale per minimizzare gli errori e le incongruenze nei dati.
  
- **Configurazione Dinamica**: Fornire la possibilità di personalizzare i valori predefiniti (come tipo di dispositivo, produttore, piattaforma, e ruolo del dispositivo) attraverso un file di configurazione esterno o variabili di ambiente. Questo migliorerebbe la flessibilità dello script, consentendo agli utenti di adattarlo facilmente alle proprie esigenze specifiche.

### Note

- **Precisione dei Dati**: Attualmente, lo script carica gli host utilizzando valori predefiniti per diversi attributi. Questo approccio può non essere sempre accurato e potrebbe richiedere un'ulteriore revisione e pulizia dei dati in NetBox.

- **Uso Cautelativo**: Dato che lo script non distingue accuratamente tra diversi tipi di dispositivi (come IPMI rispetto ai server) e non gestisce le etichette, si consiglia di usarlo con cautela. È ideale per un primo caricamento di massa, ma gli utenti dovrebbero essere pronti a effettuare aggiustamenti manuali successivi.

Queste note e suggerimenti per miglioramenti futuri mirano a ottimizzare lo script `create_hosts.py`, rendendolo più robusto, flessibile e affidabile per gli utenti finali. Implementando queste modifiche, lo script potrebbe offrire un supporto più completo e accurato per la gestione degli host in NetBox.


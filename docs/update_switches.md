# Documentazione Script di Gestione Switch

## Panoramica

Questo script Python è progettato per facilitare la gestione degli switch di rete attraverso l'interazione con le API di NetBox e Netdisco. Permette di aggiornare automaticamente le informazioni relative alle porte degli switch, sfruttando i dati raccolti da entrambe le piattaforme.

## Dipendenze

Per eseguire correttamente lo script, è necessario installare le seguenti dipendenze:

- `requests`
- `json`
- `urllib3`
- `asyncio`
- `re`

Assicurati di avere anche accesso alle librerie personalizzate come specificato dai percorsi relativi nel codice.

## Configurazione

Prima di eseguire lo script, è necessario configurare i seguenti percorsi file per il salvataggio dei dati JSON relativi a Netdisco e NetBox:

- `file_path_netdisco`: Percorso per i dati di Netdisco.
- `file_path_netbox`: Percorso per i dati di NetBox.
- `file_path_to_load`: Percorso per i dati da caricare.
- `file_path_tmp`: Percorso temporaneo per i dati di elaborazione.

## Autenticazione

Lo script richiede l'autenticazione per accedere alle API di Netdisco e NetBox. Le credenziali o i token di accesso devono essere configurati correttamente all'interno dello script.

## Funzionalità

### Aggiornamento delle Porte degli Switch

Lo script esegue le seguenti operazioni principali:

1. **Recupero dei Dispositivi da NetBox**: Viene effettuata una richiesta all'API di NetBox per ottenere un elenco di dispositivi, che vengono filtrati in base al ruolo di "switch".

2. **Ricerca e Gestione dei Dispositivi in Netdisco**: Per ogni dispositivo identificato in NetBox, lo script cerca corrispondenze in Netdisco utilizzando il nome del dispositivo. Successivamente, recupera le informazioni relative alle porte degli switch da Netdisco.

3. **Aggiornamento delle Informazioni sulle Porte in NetBox**: Utilizzando i dati raccolti da Netdisco, lo script aggiorna NetBox con le informazioni attuali delle porte degli switch.

### Gestione Errori

Lo script include una gestione degli errori per identificare e registrare eventuali problemi incontrati durante l'aggiornamento delle informazioni delle porte.

## Esempi di Uso

```python
# Esempio di autenticazione per Netdisco
token_netdisco = NDiscoAPI.authenticate()

# Esempio di recupero dei dispositivi da NetBox
devices_netbox = NBoxAPI.get_all_devices_netbox()

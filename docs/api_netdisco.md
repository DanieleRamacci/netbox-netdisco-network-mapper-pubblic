# Documentazione Libreria Netdisco Functions

## Introduzione

La libreria `api_netdisco.py` fornisce una serie di funzioni per interagire con le API di Netdisco, consentendo operazioni come l'autenticazione, il recupero di informazioni sui dispositivi, la ricerca di dispositivi, il recupero delle porte dei dispositivi, e altro ancora. Questa documentazione dettaglia l'utilizzo di ciascuna funzione all'interno della libreria.

## Configurazione

Assicurati di configurare l'URL base di Netdisco e il token di autenticazione all'interno di ogni funzione, se necessario. Questi valori sono richiesti per autenticare le richieste alle API di Netdisco.

## Funzioni

### `authenticate()`

Esegue l'autenticazione presso Netdisco e restituisce un token di accesso.

### `get_switch(token, file_path)`

Recupera tutti i dispositivi switch da Netdisco e li salva in un file JSON specificato.

- **Parametri**:
    - `token`: Il token di autenticazione.
    - `file_path`: Il percorso in cui salvare il file JSON degli switch.

### `search_device_netdisco(token, name)`

Ricerca un dispositivo in Netdisco utilizzando un nome specificato.

- **Parametri**:
    - `token`: Il token di autenticazione.
    - `name`: Il nome del dispositivo da cercare.

### `get_ports_device_netdisco(token, ip_address)`

Recupera le informazioni sulle porte di un dispositivo specificato tramite indirizzo IP.

- **Parametri**:
    - `token`: Il token di autenticazione.
    - `ip_address`: L'indirizzo IP del dispositivo.

### `add_manufacturer_and_platform(devices, file_path_netdisco)`

Aggiunge informazioni su produttore e piattaforma ai dispositivi e salva i risultati in un file JSON.

- **Parametri**:
    - `devices`: Lista dei dispositivi.
    - `file_path_netdisco`: Il percorso in cui salvare il file JSON.

### `get_host_by_switch_ip(token, sw_devices, file_path_netdisco)`

Recupera gli host connessi a uno switch specificato tramite indirizzo IP e salva i risultati in un file JSON.

- **Parametri**:
    - `token`: Il token di autenticazione.
    - `sw_devices`: Lista dei dispositivi switch.
    - `file_path_netdisco`: Il percorso in cui salvare il file JSON degli host.

### `add_dns_ip_to_hosts_json(token, file_path_netdisco)`

Aggiunge informazioni DNS e IP agli host e salva i risultati aggiornati in un file JSON.

- **Parametri**:
    - `token`: Il token di autenticazione.
    - `file_path_netdisco`: Il percorso in cui salvare il file JSON aggiornato.

### `get_dns_ip_from_mac(mac_address, token, daterange)`

Recupera l'indirizzo IP e il nome DNS basato sull'indirizzo MAC fornito.

- **Parametri**:
    - `mac_address`: L'indirizzo MAC.
    - `token`: Il token di autenticazione.
    - `daterange`: L'intervallo di date per la ricerca.

### `save_api_response_log(data, log_file_path)`

Salva il log di una risposta API in un file JSON.

- **Parametri**:
    - `data`: I dati da loggare.
    - `log_file_path`: Il percorso del file dove salvare il log.

## Uso

Per utilizzare le funzioni di questa libreria, importa la classe `NDiscoAPI` nel tuo script Python e invoca le funzioni desiderate con i parametri appropriati.

```python
from lib.netdisco_function import NDiscoAPI

# Esempio di utilizzo
token = NDiscoAPI.authenticate()
switches = NDiscoAPI.get_switch(token, '/path/to/save/switches/')

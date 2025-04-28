# Documentazione Libreria NetBox Functions

## Introduzione

La libreria `api_netbox
.py` fornisce un insieme di funzioni per interagire con le API di NetBox, consentendo di effettuare operazioni come il recupero di informazioni sui dispositivi, la creazione di nuovi dispositivi, tipi di dispositivi, piattaforme, produttori, e interfacce. Questa documentazione dettaglia l'uso di ogni funzione all'interno della libreria.

## Configurazione

Prima di utilizzare la libreria, assicurati di configurare correttamente l'URL di base di NetBox e il token di autenticazione all'interno di ogni funzione. Questi valori sono richiesti per autenticare le richieste alle API di NetBox.

## Funzioni

### `get_platform_and_manufacturer_from_netbox(file_path_netbox)`

Questa funzione recupera l'elenco delle piattaforme disponibili in NetBox e le salva in un file JSON specificato.

- **Parametri**:
    - `file_path_netbox`: Il percorso in cui salvare il file JSON delle piattaforme.

### `create_manufacturer_and_platform_in_netbox(manufacturer_name, manufacturer_slug, manufacturer_description, platforms)`

Crea un produttore e associa a esso delle piattaforme in NetBox.

- **Parametri**:
    - `manufacturer_name`: Il nome del produttore.
    - `manufacturer_slug`: Uno slug univoco per il produttore.
    - `manufacturer_description`: Una descrizione del produttore.
    - `platforms`: Un elenco di nomi di piattaforme da associare al produttore.

### `create_model_type_in_netbox(manufacturer_id, model_data)`

Crea un tipo di modello di dispositivo in NetBox.

- **Parametri**:
    - `manufacturer_id`: L'ID del produttore associato al tipo di modello.
    - `model_data`: Un dizionario con i dati del modello di dispositivo.

### `create_model_types_roles_from_device_file_and_create_device(file_path, tag)`

Crea tipi di modelli di dispositivi e ruoli dai dati presenti in un file JSON e poi crea i dispositivi in NetBox.

- **Parametri**:
    - `file_path`: Il percorso del file JSON contenente i dati dei dispositivi.
    - `tag`: Un tag da associare ai dispositivi creati.

### `get_device_type_id_by_model(model)`

Recupera l'ID di un tipo di dispositivo basato sul modello specificato.

- **Parametri**:
    - `model`: Il modello del dispositivo.

### `create_device_in_netbox(device_type_id, device_data)`

Crea un dispositivo in NetBox.

- **Parametri**:
    - `device_type_id`: L'ID del tipo di dispositivo.
    - `device_data`: Un dizionario con i dati del dispositivo.

### `get_role_id_by_tag(tag_name)`

Recupera l'ID di un ruolo basato sul nome del tag specificato.

- **Parametri**:
    - `tag_name`: Il nome del tag associato al ruolo.

### `create_role_from_tag(tag_name)`

Crea un ruolo in NetBox basato su un nome di tag.

- **Parametri**:
    - `tag_name`: Il nome del tag da cui creare il ruolo.

### `load_hosts_to_netbox(file_path)`

Carica gli host in NetBox da un file JSON.

- **Parametri**:
    - `file_path`: Il percorso del file JSON contenente i dati degli host.

### `get_all_devices_netbox(params=None)`

Recupera tutti i dispositivi presenti in NetBox.

- **Parametri**:
    - `params`: Parametri opzionali per filtrare i dispositivi recuperati.

### `create_interface_netbox(device_id, name, type, enabled=False, label=None, mac_address=None, speed=None, duplex=None, description=None, tags=None, custom_fields=None)`

Crea una nuova interfaccia su un dispositivo in NetBox.

- **Parametri**:
    - `device_id`: L'ID del dispositivo su cui creare l'interfaccia.
    - `name`: Il nome dell'interfaccia.
    - `type`: Il tipo dell'interfaccia.
    - Altri parametri opzionali per specificare dettagli aggiuntivi dell'interfaccia.

### `match_interface_type(input_type)`

Associa un tipo di interfaccia input a uno dei tipi di interfaccia supportati da NetBox.

- **Parametri**:
    - `input_type`: Il tipo di interfaccia da associare.

## Uso

Per utilizzare le funzioni di questa libreria, è sufficiente importare la classe `NBoxAPI` nel tuo script Python e invocare le funzioni desiderate con i parametri appropriati.

```python
from lib.netbox_function import NBoxAPI

# Esempio di utilizzo
platforms = NBoxAPI.get_platform_and_manufacturer_from_netbox('/path/to/netbox/data/')

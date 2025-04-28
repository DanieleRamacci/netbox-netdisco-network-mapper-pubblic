# lib/netdisco_function.py

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sys
sys.path.append('/lavoro/netdisco-script')
import os
from datetime import datetime, timedelta
import ipaddress
from lib.utils.util_functions import Utils


class NDiscoAPI:
    def __init__(self):
        # Puoi inizializzare l'oggetto con eventuali impostazioni necessarie
        pass

    def custom_function(self):
        return "Custom function from NetBox API"
    

    def authenticate():
        
        url = "<netdisco-endpoint>/login" # endpoint netdisco
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Basic dDJ1c2VyOktudTNyVDI=",
        }
        data = {
            "username": "****",
            "password": "****"
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        #print(response)

        if response.status_code == 200:
            print(response.json()['api_key'])
            print("Autenticato")

            return response.json()['api_key']
        else:
            print(f"Authentication failed with status code {response.status_code}")
            return None

    #recupera tutti i device da netdisco
    def get_switch(token, file_path):
        r = requests.get('<netdisco-endpoint>/api/v1/search/device', 
                        headers={'Accept': 'application/json',
                                'Authorization': ''+token+''},
                        params = {"location": "Tier 2", "matchall": False, "seeallcolumns": True})
        with open(file_path+'switch.json', 'w') as json_file:
            json.dump(r.json(), json_file, indent=4)

        return r.json()
    

    #search device netdisco 
    def search_device_netdisco(token, name):
        # Endpoint per la ricerca di dispositivi in Netdisco
        netdisco_url = '<netdisco-endpoint>/api/v1/search/device'
        
    
        try:
            # Effettua la richiesta GET all'API di Netdisco
            response = requests.get(netdisco_url,  headers={'Accept': 'application/json',
                                'Authorization': ''+token+''},
                        params = {"q": name, "matchall": False, "seeallcolumns": True})
            
            # Controlla se la risposta ha avuto successo
            if response.status_code == 200:
                # Ritorna il risultato della ricerca
                return response.json()
            else:
                # Gestisce i casi di errore restituendo il codice di stato e il messaggio di errore
                return {"error": "Request failed", "status_code": response.status_code, "message": response.text}
        except requests.exceptions.RequestException as e:
            # Gestisce le eccezioni generiche delle richieste, come problemi di connessione
            return {"error": "Request exception", "message": str(e)}




        #crea e modifica il file switch_with_plat per aggiungere alla lista switch platform e manufascturer

    #get port device netdisco 
    def get_ports_device_netdisco(token , ip_address):
        # URL dell'API di Netdisco per ottenere le porte di un dispositivo
        netdisco_url = f"http://<netdisco-endpoint>/api/v1/object/device/{ip_address}/ports"

        try:
            # Esegui la richiesta GET
            response = requests.get(netdisco_url, headers={'Accept': 'application/json',
                                'Authorization': ''+token+''},)

            # Controlla se la richiesta ha avuto successo
            if response.status_code == 200:
                return response.json()  # Ritorna il JSON della risposta
            else:
                print(f"Errore nella richiesta: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            # Gestisce eventuali eccezioni durante la richiesta, come problemi di connessione
            print(f"Errore nella richiesta a Netdisco: {e}")
            return None


    def  add_manufacturer_and_platform (devices, file_path_netdisco):
        results = {}
        if os.path.exists(file_path_netdisco+'switch_with_plat.json'):
            #se esiste rimuovilo 
            print('il file da rimuovere esiste e lo rimuovo'+ file_path_netdisco+'switch_with_plat.json')
            os.remove(file_path_netdisco+'switch_with_plat.json')
        else: 
            print('il file da rimuovere non esiste')

        with open(file_path_netdisco+'switch_with_plat.json', 'a') as json_file:
            json_file.write("[\n")
        
        for index, device in enumerate(devices):
            ip = device['ip']
            platform= device['os']
            manufacturer= device['vendor']
            versione_os=device['os_ver']
            
        
            device_info = {
                "description":device['description'],
                "num_ports":device['num_ports'],
                "model":device['model'],
                "part_number": device['serial'],
                "platform": platform,
                "manufacturer": manufacturer,
                "version_os":versione_os,
                "name": device['name'],
                "ip": device['ip']
            }
            
            with open(file_path_netdisco+'switch_with_plat.json', 'a') as json_file:
                json.dump(device_info, json_file, indent=4)
                # Aggiungi virgola tra i json

                if index == len(devices)-1:
                    print("non inserisco la virgola")  
                    print(index, len(devices))
                else:
                    print(index, len(devices))
                    print("scrivo dentro la virgola")
                    json_file.write(",\n")



            results[device['name']] = device_info
            
        with open(file_path_netdisco+'switch_with_plat.json', 'a') as json_file:
            json_file.write("\n]")
        return results

    def get_host_by_switch_ip(token, sw_devices, file_path_netdisco):
        results = {}
        if os.path.exists(file_path_netdisco+'hosts.json'):
            #se esiste rimuovilo 
            print('il file da rimuovere esiste e lo rimuovo'+ file_path_netdisco+'hosts.json')
            os.remove(file_path_netdisco+'hosts.json')
        else: 
            print('il file da rimuovere non esiste')

        with open(file_path_netdisco+'hosts.json', 'a') as json_file:
            json_file.write("[\n")
        #aggiungo i manufacturer dello switch alla lista 
        for index, sw_device in enumerate(sw_devices):
            ip = sw_device['ip']
            platform= sw_device['os']
            manufacturer= sw_device['vendor']
            versione_os=sw_device['os_ver']
            

            url_netdisco = f'http://<netdisco-endpoint>/api/v1/object/device/{ip}/nodes?active_only=false'
            r = requests.get(url_netdisco,
                            headers={'Accept': 'application/json',
                                    'Authorization': ''+token+''},
                            params={"location": "Tier 2", "matchall": False, "seeallcolumns": True})
            
        #TODO dovrei aggiungere  per ogni host i manufacturer , platform, os_version ecc
            device_info = {
                "description":sw_device['description'],
                "num_ports":sw_device['num_ports'],
                "model":sw_device['model'],
                "part_number": sw_device['serial'],
                "platform": platform,
                "manufacturer": manufacturer,
                "version_os":versione_os,
                "name": sw_device['name'],
                "ip": sw_device['ip'],
                "hosts": r.json()
            }
            
            with open(file_path_netdisco+'hosts.json', 'a') as json_file:
                json.dump(device_info, json_file, indent=4)
                # Aggiungi virgola tra i json

                if index == len(sw_devices)-1:
                    print("non inserisco la virgola")  
                    print(index, len(sw_devices))
                else:
                    print(index, len(sw_devices))
                    print("scrivo dentro la virgola")
                    json_file.write(",\n")



            results[sw_device['name']] = device_info
            
        with open(file_path_netdisco+'hosts.json', 'a') as json_file:
            json_file.write("\n]")
        return results
    
    def add_dns_ip_to_hosts_json(token, file_path_netdisco):
        # Carica i dati dai file node.json e salva i dati aggiornati in node_with_dns_ip.json
        with open(file_path_netdisco + 'hosts.json', 'r') as f:
            nodes = json.load(f)
        
        # Lista per salvare i dati aggiornati
        updated_nodes = []
        # Calcola il daterange dinamico per ottenere le informazioni del momento attuale
        current_time = datetime.now()
        start_time = current_time - timedelta(minutes=5)  # Ad esempio, 5 minuti prima
        end_time = current_time + timedelta(minutes=5)  # Ad esempio, 5 minuti dopo
        daterange = f"{start_time.strftime('%Y-%m-%d %H:%M')} to {end_time.strftime('%Y-%m-%d %H:%M')}"
    
        # Cicla attraverso ogni nodo
        for node in nodes:
            print("switch:",node['name'] )

            # Per ogni nodo, cicla attraverso i dettagli per ogni indirizzo MAC
            for hosts in node['hosts']:
                mac_address = hosts['mac']

                # Fai una chiamata all'API per ottenere l'indirizzo IP e il nome DNS
                # Usando la funzione get_dns_ip_from_mac (da implementare)
                ip_dns_info, sightings_info= NDiscoAPI.get_dns_ip_from_mac_2(mac_address, token,daterange)
                
                # Aggiungi i nuovi dati ottenuti al dettaglio del nodo
                hosts['ip_dns_info'] = ip_dns_info
                hosts['sightings_info'] = sightings_info                

            # Aggiungi il nodo aggiornato alla lista dei nodi aggiornati
            updated_nodes.append(node)
        
        # Scrivi i dati aggiornati nel file node_with_dns_ip.json
        with open(file_path_netdisco + 'hosts_with_dns_ip.json', 'w') as f:
            json.dump(updated_nodes, f, indent=4)
    

    def get_dns_ip_from_mac(mac_address,token,daterange):
        # Fai una chiamata all'API precedente per ottenere l'indirizzo IP e il nome DNS
        # basandoti sull'indirizzo MAC fornito
        age ="2024-01-01to2024-02-13"
        # Esempio di URL dell'API
        api_url = f"<netdisco-endpoint>/api/v1/search/node?q={mac_address}&partial=false&deviceports=true&show_vendor=true&archived=false"
        
        print("url", api_url)

        response = requests.get(api_url, headers={'Accept': 'application/json', 'Authorization': token}, params={})
    
        # Controlla se la richiesta è andata a buon fine
        if response.status_code == 200:
            data = response.json()
            # Verifica se la lista 'sightings' esiste e contiene almeno un elemento
            if 'ips' in data and data['ips']:
                # Estrai l'indirizzo IP e il nome DNS dalla risposta
                ip = data['ips'][0]['ip']
                dns_name = data['ips'][0]['dns']
                return ip, dns_name
            else:
                print("Nessun dato trovato per l'indirizzo MAC specificato.",mac_address )
                return None, None
        else:
            print(f"Errore durante la richiesta all'API: {response.status_code}")
            return None, None


    def save_api_response_log(data, log_file_path):
        """
        Salva il log di una risposta API in un file JSON.

        Args:
        - data: I dati da loggare.
        - log_file_path: Il percorso del file dove salvare il log.
        """
        # Preparazione dei dati di log con timestamp
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": data
        }

        try:
            # Apertura del file in modalità append per aggiungere i log
            with open(log_file_path, "a") as log_file:
                # Scrittura dei dati di log nel file
                log_file.write(json.dumps(log_entry, indent=4) + ",\n")  # Aggiungi una virgola e un a capo per separare le voci
        except Exception as e:
            print(f"Errore durante il salvataggio del log: {e}")


    def get_dns_ip_from_mac_2(mac_address, token, daterange):
        api_url = f"http://<netdisco-endpoint>/api/v1/search/node?q={mac_address}&partial=false&deviceports=true&show_vendor=true&archived=false"
        print("URL:", api_url)

        response = requests.get(api_url, headers={'Accept': 'application/json', 'Authorization': token})

        ipv4_count = 0
        no_dns_count = 0
        ipmi_dns_count = 0

        if response.status_code == 200:
            data = response.json()
            NDiscoAPI.save_api_response_log(data, "api_response_logs_ok.json")

            ip_dns_info = []
            sightings_info = []

            if isinstance(data, dict):
                for ip_info in data.get('ips', []):
                    ip_type = "Unknown"
                    try:
                        ip_obj = ipaddress.ip_address(ip_info['ip'])
                        if ip_obj.version == 4:
                            ipv4_count += 1
                            dns_name = ip_info.get('dns')
                            if dns_name and not dns_name.startswith("swatlas-") and not dns_name.startswith("sw"):
                                # Questo blocco tratta gli indirizzi IPv4 che non appartengono agli switch
                                ip_type = "IPv4" 
                                pass
                            elif dns_name and (dns_name.startswith("swatlas-") or dns_name.startswith("sw")):
                                # Esclude gli switch dall'elaborazione
                                continue
                            else:
                                no_dns_count += 1
                        elif ip_obj.version == 6:
                            if ip_obj.is_link_local:
                                ip_type = "IPv6 Link-Local"
                            else:
                                ip_type = "IPv6"
                    except ValueError:
                        pass  # Se l'indirizzo IP non è valido, mantiene ip_type come "Unknown"


                    manufacturer = ip_info.get('manufacturer', {})
                    manufacturer_company = manufacturer.get('company', "Unknown") if manufacturer else "Unknown"

                    ip_dns_info.append({
                        'ip': ip_info['ip'],
                        'type': ip_type,
                        'dns': ip_info.get('dns'),
                        'time_first': ip_info.get('time_first_stamp'),
                        'time_last': ip_info.get('time_last_stamp'),
                        'manufacturer': manufacturer_company,
                        'active': ip_info.get('active', 0)
                    })

                for sighting in data.get('sightings', []):
                    device = sighting.get('device', {})
                    sightings_info.append({
                        'device_name': device.get('name'),
                        'dns': device.get('dns'),
                        'port': sighting.get('port'),
                        'vlan': sighting.get('vlan'),
                        'time_first': sighting.get('time_first_stamp'),
                        'time_last': sighting.get('time_last_stamp'),
                        'switch': sighting.get('switch'),
                        'active': sighting.get('active', 0)
                    })
            else:
                print("La risposta non è nel formato atteso (dizionario).")
                NDiscoAPI.save_api_response_log(data, "api_response_logs_error.json")
                return None, None
        else:
            print(f"Errore durante la richiesta all'API: {response.status_code}")
            return None, None

        return ip_dns_info, sightings_info
    


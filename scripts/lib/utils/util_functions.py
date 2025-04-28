# lib/utils_functions.py
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import subprocess
from pysnmp.hlapi.asyncio import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, getCmd, ObjectType, ObjectIdentity
from datetime import datetime
import os
import shutil

class Utils:
    def __init__(self):
        # Puoi inizializzare l'oggetto con eventuali impostazioni necessarie
        pass


    # prende in input device(lista di sispositivi di netdisco) e platform (lista delle platform from netbox )
    # se esiste una corrispondenza la restituisce in output.
    def confronta_netdisco_e_netbox_platform_return_id_switch(device, platforms):
        for p in platforms:
            platform_name = p['name'].lower().strip()
            device_platform_name = device['platform'].lower().strip()

            print(f"Confronto: {platform_name} con {device_platform_name}")

            if platform_name == device_platform_name:
                print("Corrispondenza trovata!")
                print("allora estrapolo anche il manufacturer")
                manufacturer_name = p['manufacturer']['name'].lower().strip()
                device_manufacturer_name = device['manufacturer'].lower().strip()
                if manufacturer_name == device_manufacturer_name:
                    print("manufacturer trovato ", manufacturer_name, device_manufacturer_name)

                # Se c'è una corrispondenza, restituisci l'ID della piattaforma
                return {
                    "description":device['description'],
                    "num_ports":device['num_ports'],
                    "model":device['model'],
                    "part_number": device['part_number'],
                    "platform_name": p['name'] ,
                    "manufacturer_name": p['manufacturer']['name'],
                    "platform_id": p['id'],
                    "manufacturer_id": p['manufacturer']['id'], # Aggiungi l'ID del produttore se necessario
                    "version_os": device['version_os'],
                    "nome": device['name'],
                }
        # Se nessuna corrispondenza è stata trovata, restituisci None per l'ID della piattaforma
        return {
                    "platform_id": None,
                    "manufacturer_id": None, # Aggiungi l'ID del produttore se necessario
                    "version_os": device['version_os'],
                    "Nome": device['tipo_dispositivo'],
        }
    


        # prende in input device(lista di sispositivi di netdisco) e platform (lista delle platform from netbox )
    # se esiste una corrispondenza la restituisce in output.
    def confronta_netdisco_e_netbox_platform_return_id_host(device, platforms):
        for p in platforms:
            platform_name = p['name'].lower().strip()
            device_platform_name = device['platform'].lower().strip()

            print(f"Confronto: {platform_name} con {device_platform_name}")

            if platform_name == device_platform_name:
                print("Corrispondenza trovata!")
                print("allora estrapolo anche il manufacturer")
                manufacturer_name = p['manufacturer']['name'].lower().strip()
                device_manufacturer_name = device['manufacturer'].lower().strip()
                if manufacturer_name == device_manufacturer_name:
                    print("manufacturer trovato ", manufacturer_name, device_manufacturer_name)

                # Se c'è una corrispondenza, restituisci l'ID della piattaforma
                return {
                    "description":device['description'],
                    "num_ports":device['num_ports'],
                    "model":device['model'],
                    "part_number": device['part_number'],
                    "platform_name": p['name'] ,
                    "manufacturer_name": p['manufacturer']['name'],
                    "platform_id": p['id'],
                    "manufacturer_id": p['manufacturer']['id'], # Aggiungi l'ID del produttore se necessario
                    "version_os": device['version_os'],
                    "nome": device['name'],
                    "hosts_collegati": device['dettagli']
                }
        # Se nessuna corrispondenza è stata trovata, restituisci None per l'ID della piattaforma
        return {
                    "platform_id": None,
                    "manufacturer_id": None, # Aggiungi l'ID del produttore se necessario
                    "version_os": device['version_os'],
                    "Nome": device['tipo_dispositivo'],
                    "dettagli": device['dettagli']
        }
    

    #prende i  devices  scaricati da netdisco e li cicla per creare un dizionario,
    # viene formato un json con una struttura dati pronta per essere carica su newtbox   
    def create_manufacturer_json_for_netbox(devices, file_path_to_load):
        manufacturers_dict = {}

        # Cicla su ogni oggetto nel JSON devices
        for device in devices:
            # Estrai i campi 'vendor' e 'os'
            vendor = device['vendor']
            platform = device['os']

            # Assicurati che il vendor non sia vuoto
            if vendor:
                # Se il vendor non è presente nel dizionario, aggiungilo
                if vendor not in manufacturers_dict:
                    manufacturers_dict[vendor] = {'name': vendor, 'platforms': set()}

                # Aggiungi la piattaforma al set delle piattaforme associate al produttore
                manufacturers_dict[vendor]['platforms'].add(platform)

        manufacturers = []

        # Costruisci la lista di manufacturer
        for vendor, data in manufacturers_dict.items():
            manufacturer = {
                'platforms': list(data['platforms']),
                'name': data['name'],
                'slug': f'manufacturer-{data["name"].lower().replace(" ", "-")}',
                'description': '',
                'tags': data['name'],
            }
            manufacturers.append(manufacturer)

        # Controllo se esiste il file, se sì, lo elimino; se no, non faccio nulla
        Utils.check_file_and_remove(file_path_to_load + 'manufacturers_to_load.json')

        # Creao il file e salvo la lista in un json
        with open(file_path_to_load + 'manufacturers_to_load.json', 'w') as json_file:
            json.dump(manufacturers, json_file, indent=2)



    def check_file_and_remove(file_path):
        if os.path.exists(file_path):
            #se esiste rimuovilo il
            print('il file da rimuovere esiste e lo rimuovo'+ file_path +'')
            os.remove(file_path)
            return True
        else: 
            print('il file da rimuovere non esiste')
            return False
        


    def fetch_ipmi(dns_name):
        file_path='./../data/ipmi/'
        username="root"
        password="superuser"
        """
        Fetch IPMI device information using ipmitool and save it to a JSON file.

        Args:
        - ip_address: IP address of the IPMI device.
        - username: Username for IPMI login.
        - password: Password for IPMI login.
        - file_path: Output JSON file to save the device information.
        """
        # Comando ipmitool per raccogliere le informazioni FRU del dispositivo
        command = f"ipmitool -I lanplus -H {dns_name} -U {username} -P {password} fru print"
        
        try:
            # Esecuzione del comando ipmitool
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            
            # Controllo se il comando è stato eseguito con successo
            if result.returncode == 0:
                data = result.stdout
                # Salvataggio dei dati in un file JSON
                with open(file_path + 'ipmi_host_info.json', "w") as file:
                    # Conversione dell'output in una struttura dati JSON (esempio semplice)
                    json.dump({"ipmi_data": data}, file, indent=4)
                print(f"IPMI data saved to {file_path}ipmi_host_info.json")
                return result.stdout
            else:
                print(f"Error executing ipmitool: {result.stderr}")
        except Exception as e:
            print(f"An error occurred: {e}")

        


    def save_to_json(data, file_path, file_name=None):
        # Se file_name è specificato, costruisci il file_path includendo il nome del file e il timestamp
        if file_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"{file_path}/{file_name}_{timestamp}.json"

        # Verifica se data è serializzabile in JSON
        try:
            # Prova a serializzare `data` per vedere se è già in formato compatibile con JSON
            json_test = json.dumps(data)
            is_json_serializable = True
        except (TypeError, ValueError):
            # Se si verifica un'eccezione, `data` non è serializzabile in JSON
            is_json_serializable = False

        # Se `data` non è serializzabile, prova a convertirlo in un dizionario
        if not is_json_serializable:
            try:
                # Supponendo che `data` possa essere convertito in un dizionario
                data = {'data': str(data)}
            except Exception as e:
                print(f"Errore nella conversione dei dati in formato JSON: {e}")
                return

        # Salva i dati in un file JSON
        try:
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Dati salvati correttamente in {file_path}")
        except Exception as e:
            print(f"Errore nel salvataggio dei dati in formato JSON: {e}")

   ## funzione che svuota una cartella e contrlla se i file che sta cancellando sono json 
            
    def empty_directory_check_json(directory_path):
        if not os.path.isdir(directory_path):
            print(f"La directory {directory_path} non esiste.")
            return

        files_deleted = 0
        directories_deleted = 0

        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path) and item_path.endswith('.json'):
                os.remove(item_path)
                print(f"Rimosso il file JSON: {item}")
                files_deleted += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Rimossa la directory: {item}")
                directories_deleted += 1

        print(f"Operazione completata. Files JSON rimossi: {files_deleted}, directories rimosse: {directories_deleted}.")

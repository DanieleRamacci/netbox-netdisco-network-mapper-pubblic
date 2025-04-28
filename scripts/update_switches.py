import requests
import json
import urllib3
import os
import sys
from lib.netbox_function.api_netbox import NBoxAPI
from lib.netdisco_function.api_netdisco import NDiscoAPI
from lib.utils.util_functions import Utils
import re  # Assicurati di importare il modulo re all'inizio del tuo script
sys.path.append('lavoro/netdisco-script/')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## dove sono salvati i json di netdicos e netbox scaricati
file_path_netdisco = './../data/switch/netdisco/'
file_path_netbox = './../data/switch/netbox/'
file_path_to_load ='./../data/switch/to_load/'
file_path_tmp ='./../data/tmp/'





##### autenticazione per netdisco
token_netdisco =  NDiscoAPI.authenticate()


## qui le routin di aggiornamento degli switch 

#####AGGIORNAMENTO DELLE PORTE DEGLI SWITCH#######

#get device from netbox 
#è possibile pqassare un parametro come tag
devices_netbox=NBoxAPI.get_all_devices_netbox()
Utils.empty_directory_check_json(file_path_tmp)

# salvo dentro un json per visualizzare i dati
Utils.save_to_json(devices_netbox,file_path_tmp,"device_from_netbox")

## processo i device ritornati da netbox filtrandoli per device_role
#in questo caso switch e prino il device 

# svuoto la cartella tmp 
for device_netbox in devices_netbox:
        # Controlla se il dispositivo ha il ruolo di "switch"
        if device_netbox.get("device_role", {}).get("slug") == "switch":
            # Stampa il nome del dispositivo
            print("Nome dispositivo (Switch):", device_netbox.get("name"))
            
            #per ogni nome dentro netbox con ruolo switch cerco dentro netdisco 
            netdisco_device=NDiscoAPI.search_device_netdisco(token_netdisco,device_netbox.get("name"))
            Utils.save_to_json(netdisco_device,file_path_tmp,str(device_netbox.get("name")))

            #per ogni dispositivo ritornato da netdisco tramite ip o mac vado vado a farmin restituire 
            #le porte 
            
          
            # Supponendo che netdisco_search_result sia la variabile che contiene la risposta della ricerca
            if netdisco_device and isinstance(netdisco_device, list):
                # Accede al primo elemento della lista e stampa l'IP, se presente
                switch = netdisco_device[0]  # Accede al primo elemento della lista
                if 'ip' in switch:
                    print(switch['ip'])
                    #GET_PORT_NETDISCO
                    device_ports_ndisco=NDiscoAPI.get_ports_device_netdisco(token_netdisco,switch['ip'])
                    if device_ports_ndisco and isinstance(device_ports_ndisco, list):
                        # La lista non è vuota, procede con l'elaborazione
                        print(f"Trovate {len(device_ports_ndisco)} porte.")
                        # Qui puoi iterare su device_ports per accedere alle informazioni di ogni porta
                        Utils.save_to_json(device_ports_ndisco,file_path_tmp,"ports_"+str(device_netbox.get("name")))
                        error_list = []
                        for port_ndisco in device_ports_ndisco:
                            # qui un eventuale caricamento di interfacce su netbox per ogni dispositivo
                            """ Crea una nuova interfaccia su un dispositivo in NetBox.
                             :param device_id: ID del dispositivo su cui creare l'interfaccia.
                             :param interface_name: Nome dell'interfaccia da creare.
                             :param interface_type: Tipo dell'interfaccia (es. 1000base-t, virtual, etc.).
                             :param mac_address: Indirizzo MAC dell'interfaccia.
                            :param description: Descrizione dell'interfaccia.
                            :param enabled: Stato dell'interfaccia (abilitata o meno).
                            :return: Risposta della richiesta di creazione.
                            """
                            device_id=device_netbox.get("id")
                            name=port_ndisco.get("port")
                            # Utilizza la funzione match_interface_type per ottenere il tipo corretto
                            type_matched = NBoxAPI.match_interface_type(port_ndisco.get("type"))  # Chiama la funzione per fare il match

                            type=port_ndisco.get("type")
                            mac = port_ndisco.get("mac")
                            if not re.match("[0-9a-fA-F]{2}([-:][0-9a-fA-F]{2}){5}$", str(mac)):
                              mac = str('')  # Ometti il campo mac_address o imposta un valore di default se necessario

                            # Converti 'enabled' in un valore booleano. 
                            # Assumi che 'up' sia una stringa che rappresenta lo stato della porta ("up" per vero, "down" per falso)
                            enabled_str = port_ndisco.get("up")
                            if enabled_str.lower() in ['true', 'up']:
                                enabled = True
                            elif enabled_str.lower() in ['false', 'down']:
                                enabled = False
                            else:
                                enabled = False  # O non includere il campo se non applicabile
                            speed_value=port_ndisco.get("speed")
                            try:
                                speed = int(speed_value)
                            except (ValueError, TypeError):
                                speed = None  # O un valore di default se necessario
                            duplex=port_ndisco.get("duplex")
                            label=""
                            description=port_ndisco.get("descr")
                            tags=None
                            custom_fields=None
                            success, error_data =NBoxAPI.create_interface_netbox(
                                device_id, name, type_matched, enabled, label, mac,speed, duplex, description, tags, custom_fields)
                            # Se la creazione dell'interfaccia fallisce, salva l'errore in un file JSON
                            if not success:
                                # Aggiunge l'errore alla lista
                                error_list.append({
                                    "interface_name": name,
                                    "error": error_data
                                })
                    else:
                        #La lista è vuota o la risposta non è una lista
                        print("Nessuna porta trovata o la risposta non è nel formato atteso")
                    

                    if error_list:
                        # Salva tutti gli errori in un unico file JSON
                        Utils.save_to_json(error_list, file_path_tmp, "errore_interfacce")

                else:
                    print("L'elemento non contiene un campo 'ip'.")
            else:
                print("Nessun risultato trovato o la risposta non è una lista.")

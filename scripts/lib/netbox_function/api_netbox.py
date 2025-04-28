# lib/netbox_function.py
import random
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
from lib.utils.util_functions import Utils
from mac_vendor_lookup import MacLookup

class NBoxAPI:
    def __init__(self):
        # Puoi inizializzare l'oggetto con eventuali impostazioni necessarie
        pass

    def custom_function(self):
        return "Custom function from NetBox API"
    
    
    #chiama api platform di netbox per salvarla dentro un file json chiamato 
    #netbox_platform.json
    def get_platform_and_manufacturer_from_netbox(file_path_netbox):
        
        token = "<token>" ## aggiungere token
        # faccio una richiesta a netbox per scaricare la lista dei platform e la scrivo dentro un json 
        """
        Scarica la lista dei platform da Netbox.
        :param token: Token di autenticazione per l'API di Netbox
        :return: Lista di piattaforme
        """
        # Configurazione della richiesta

        headers = {
            "accept": "application/json",
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
        }

        # Chiamata all'API di Netbox
        response = requests.get('<netbox-endpoint>/api/dcim/platforms/', headers=headers, verify=False)

        # Controllo dello stato della risposta
        if response.status_code == 200:
            if os.path.exists(file_path_netbox+'netbox_platform.json'):
                #se esiste rimuovilo il
                print('il file da rimuovere esiste e lo rimuovo'+ file_path_netbox +'netbox_platform.json')
                os.remove(file_path_netbox+'netbox_platform.json')
            else: 
                print('il file da rimuovere non esiste')
            platforms = response.json()['results']
            with open(file_path_netbox+'netbox_platform.json', 'a') as json_file:
                json.dump(platforms, json_file, indent=4)
                
            return platforms
        else:
            print(f"Errore nella richiesta: {response.status_code} - {response.text}")
            return None
        

    def create_manufacturer_and_platform_in_netbox(manufacturer_name, manufacturer_slug, manufacturer_description, platforms):
        manufacturer_url = "<netbox-endpoint>/api/dcim/manufacturers/"
        platforms_url = "<netbox-endpoint>/api/dcim/platforms/"

        token = "<token>"

        headers = {
            "accept": "application/json",
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
        }

        data = {
            "name": manufacturer_name,
            "slug": manufacturer_slug,
            "description": manufacturer_description
        }

        manufacturer_response = requests.post(manufacturer_url, headers=headers, json=data, verify=False)

        if manufacturer_response.status_code == 201:
            print("Manufacturer created successfully!")
            manufacturer_id = manufacturer_response.json().get('id', None)
            print("manufacturer ID:",manufacturer_id)

            if manufacturer_id is not None:
            # Cicla su ogni piattaforma nel elenco
                for platform_name in platforms:
                    # Dati per la piattaforma
                    platform_data = {
                        "name": platform_name,
                        "slug": f"platform-{platform_name.lower().replace(' ', '-')}",
                        "manufacturer": manufacturer_id,
                        "description": "",
                        "tags": [],
                        "custom_fields": {}
                    }

                    # Effettua la richiesta POST per creare la piattaforma
                    platform_response = requests.post(platforms_url, headers=headers, json=platform_data, verify=False)

                    if platform_response.status_code == 201:
                        print(f"Platform '{platform_name}' created successfully!")
                    else:
                        print(f"Error creating platform '{platform_name}': {platform_response.text}")
        else:
            print(f"Error creating manufacturer: {manufacturer_response.text}")



    def create_model_type_in_netbox(manufacturer_id ,model_data):
        netbox_url = "<netbox-endpoint>/api/dcim/device-types/"
        token = "<token>"

        headers = {
            "accept": "application/json",
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
        }


        response = requests.post(netbox_url, headers=headers, json=model_data, verify=False)

        if response.status_code == 201:
            print("Model type created successfully!")
            device_type_id = response.json()["id"]  # ID del device type appena creato
            print(response.json()["id"] , response.status_code )
            return device_type_id
        elif response.status_code == 400:
            #print(f"Device type already exists with ID: {existing_device_type}")
            existing_device_type_id = NBoxAPI.get_device_type_id_by_model(model_data["model"])
            if existing_device_type_id:
                print(f" Funz: create_model_type.. Device type already exists with ID: {existing_device_type_id}")
                return existing_device_type_id
            else:
                print(f"Funz: create_model_type..  Error: Unable to retrieve existing device type ID. response :{response}  model data: {model_data}")
                return None
        else:
            print(f"Error creating model type: {response.json()}", response.status_code)
            return None


    def create_model_types_roles_from_device_file_and_create_device(file_path, tag):
        with open(file_path+'host_with_platform_for_netbox.json', 'r') as json_file:
            devices = json.load(json_file)

            # Cicla su ogni dispositivo nel file
            for device in devices:
                # Estrai le informazioni necessarie dal dispositivo
                manufacturer_id = device['manufacturer_id'] if 'manufacturer_id' in device else None
                platform_id = device['platform_id'] if 'platform_id' in device else None

                device_role=NBoxAPI.create_role_from_tag(tag)


                model_data = {
                    #ANCHOR CAMPI PER DEVICE
                    "model": device['model'] if 'model' in device else  'error-'+str(random()),
                    "manufacturer":device['manufacturer_id'],
                    "slug": str(device['model'] + "_" + device['manufacturer_name']).replace(' ', '_'),
                    "u_height": 1,  # Aggiungi qui la logica per ottenere l'altezza U se disponibile
                    "is_full_depth": True,  # Aggiungi qui la logica per ottenere l'informazione sulla profondità
                    "description": device['description'][:200],  # Aggiungi qui la logica per ottenere una descrizione se disponibile
                    #"tags": [{"name": str(tag)}],  # Modifica se necessario
                }

                device_data = {
                    "name": device['nome'],
                    "serial": device['part_number'],
                    "platform": platform_id,  # ID della piattaforma del dispositivo
                    "description": device['description'][:200],
                  #  "status": device['ps1_status'],
                    "role":device_role,
                    "site":1 
                }


                # Chiamare la funzione create_model_type_in_netbox
                device_type_id=NBoxAPI.create_model_type_in_netbox(manufacturer_id, model_data)

                NBoxAPI.create_device_in_netbox(device_type_id, device_data)


    def get_device_type_id_by_model(model):
        netbox_url = "<netbox-endpoint>/api/dcim/device-types/"
        token = "<token>"

        headers = {
            "accept": "application/json",
            "Authorization": f"Token {token}",
        }

        params = {
            "model": model
        }

        response = requests.get(netbox_url, headers=headers, params=params, verify=False)

        if response.status_code == 200:
            device_types = response.json()["results"]
            if device_types:
                # Assumiamo che ci sia solo un tipo di dispositivo con lo stesso modello
                return device_types[0]["id"]
            else:
                return None
        else:
            print(f"Error retrieving device type by model: {response.text}")
            return None
        

    def create_device_in_netbox(device_type_id,device_data):
        netbox_url = "<netbox-endpoint>/api/dcim/devices/"
        token = "<token>"

        headers = {
            "accept": "application/json",
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
        }

        # Aggiungi l'ID del device type nella struttura dati del dispositivo
        device_data["device_type"] = device_type_id

        response = requests.post(netbox_url, headers=headers, json=device_data, verify=False)

        if response.status_code == 201:
            print("Device created successfully!")
        else:
            print(f"Error creating device: {response.text}")

    def get_role_id_by_tag(tag_name):
        netbox_url = "<netbox-endpoint>/api/dcim/device-roles/"
        token = "<token>"

        headers = {
            "accept": "application/json",
            "Authorization": f"Token {token}",
        }

        params = {
            "name": tag_name.capitalize(),
        }

        response = requests.get(netbox_url, headers=headers, params=params, verify=False)

        if response.status_code == 200:
            roles = response.json()["results"]
            if roles:
                # Assume there is only one role with the same tag name
                print("dentro get_role_by_id", roles[0]["id"])
                return roles[0]["id"]
            else:
                return None
        else:
            print(f"Error retrieving role by tag '{tag_name}': {response.text}")
            return None


    def create_role_from_tag(tag_name):
        netbox_url = "<netbox-endpoint>/api/dcim/device-roles/"
        token = "<token>"

        headers = {
            "accept": "application/json",
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
        }

        # Check if the role already exists
        existing_role_id = NBoxAPI.get_role_id_by_tag(tag_name)
        if existing_role_id:
            print(f"Role with tag '{tag_name}' already exists with ID: {existing_role_id}")
            return existing_role_id

        # Create a new role if it doesn't exist
        role_data = {
            "name": tag_name.capitalize(),
            "slug": tag_name.lower().replace(" ", "_"),
            "color": "3c608d",
            "description": f"Role created automatically from tag '{tag_name}'",
        }

        response = requests.post(netbox_url, headers=headers, json=role_data, verify=False)

        if response.status_code == 201:
            role_id = response.json()["id"]
            print(f"Role '{tag_name}' created successfully with ID: {role_id}")
            return role_id
        else:
            print(f"Error creating role '{tag_name}': {response.text}")
            return None
        
    

#funzione per la creazione dei device in questo caso gli host  con parametri di default:
        
    def load_hosts_to_netbox(file_path):

        with open(file_path+'hosts_with_dns_ip.json', 'r') as json_file:
            data = json.load(json_file)
            for switch in data:
                if "ipmi" in switch.get('nome', '').lower() or switch.get('nome') == "<switch-da-saltare>": 
                    print(f"Saltando lo switch {switch.get('nome')} per la regola specificata.")
                    continue  # Salta questo switch e procedi con il prossimo
                for host in switch['hosts']:
                    ip_dns_info = host.get('ip_dns_info', [])
                    mac=host.get('mac',[])
                    print(ip_dns_info)
                    ipv4_info = next((item for item in ip_dns_info if item.get('type') == 'IPv4' and 'ipmi' not in item.get('dns', '')), None)
                    print()
                    if not ipv4_info:
                        print("salto inserimento non esiste un indirizzo IPv4 valido")
                        # Salta l'inserimento se non esiste un indirizzo IPv4 valido o se l'array ip_dns_info è vuoto
                        continue

                    device_data = {
                        "name": ipv4_info.get('dns', 'NomeDispositivoDefault'),  # Utilizza il DNS come nome del dispositivo o un valore di default
                        "serial": host.get('part_number', 'SerialDefault'),  # Usa un valore di default se non disponibile
                        "platform": host.get('platform', 6),  # ID della piattaforma di default 
                        "description": host.get('description', 'Descrizione non disponibile generata automaticamente ')[:200],  # Usa una descrizione di default se non disponibile
                        # "status": host.get('ps1_status', 'StatusDefault'),  # Commentato, ma puoi decommentarlo e usare un valore di default
                        "role": host.get('role', 2),  # Ruolo del dispositivo (esempio) o un valore di default
                        "site": host.get('site', 1)  # ID del sito in Netbox (esempio) o un valore di default
                    }


                    device_type_id_default=13
                    # Chiamare la funzione create_device_in_netbox
                    NBoxAPI.create_device_in_netbox(device_type_id_default, device_data)




    def load_hosts_to_netbox_vm_filter(file_path, device_type_id_default):
        with open(file_path + 'hosts_with_dns_ip.json', 'r') as json_file:
            data = json.load(json_file)
            for switch in data:
                if "ipmi" in switch.get('nome', '').lower() or switch.get('nome') == "<switch-da-saltare>":
                    print(f"Saltando lo switch {switch.get('nome')} per la regola specificata.")
                    continue

                for host in switch['hosts']:
                    ip_dns_info = host.get('ip_dns_info', [])
                    mac_address = host.get('mac', '')
                    print(ip_dns_info)
                    ipv4_info = next((item for item in ip_dns_info if item.get('type') == 'IPv4' and 'ipmi' not in item.get('dns', '')), None)
                    print()
                    if not ipv4_info:
                        print("Salto inserimento: non esiste un indirizzo IPv4 valido.")
                        continue

                    # Verifica se il MAC address è di una macchina virtuale
                    print('MAC DA TESTARE :'+ mac_address)
                    is_vm, vendor = NBoxAPI.is_virtual_machine(str(mac_address))
                    if is_vm:
                        print(f"Indirizzo MAC {mac_address} identificato come macchina virtuale di {vendor}.")
                        cluster = NBoxAPI.create_cluster("host_default", "host_default")
                        if cluster:
                            device_data = {
                                "name": ipv4_info.get('dns', 'VM_Default'),
                                "serial": host.get('part_number', 'VM_Serial_Default'),
                                "platform": host.get('platform', 6),
                                "description": host.get('description', 'VM generata automaticamente')[:200],
                                "role": host.get('role', 2),
                                "site": host.get('site', 1),
                                "cluster": cluster['id'] 

                            }
                            device_id=NBoxAPI.create_device_in_netbox(device_type_id_default, device_data)
                            # Qui potresti aggiungere il codice per creare la macchina virtuale
                            NBoxAPI.create_virtual_machine(ipv4_info.get('dns', 'VM_Default'),cluster['id'],device_id)

                    else:
                        device_data = {
                            "name": ipv4_info.get('dns', 'NomeDispositivoDefault'),
                            "serial": host.get('part_number', 'SerialDefault'),
                            "platform": host.get('platform', 6),
                            "description": host.get('description', 'Descrizione non disponibile generata automaticamente')[:200],
                            "role": host.get('role', 2),
                            "site": host.get('site', 1)
                        }
                        NBoxAPI.create_device_in_netbox(device_type_id_default, device_data)
                        print(f"Creato dispositivo {device_data['name']} con successo.")


    def get_all_devices_netbox(params=None):
        base_url = "<endpoint-netbox>/api/dcim/devices/"
        token = "<token>"
        if params is None:
            params = {}
        

        headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json"
        }


        all_devices = []
        next_url = base_url

        while next_url:
            response = requests.get(next_url, headers=headers, params=params, verify=False)
            if response.status_code == 200:
                data = response.json()
                all_devices.extend(data['results'])
                next_url = data.get('next', None)
                # Dopo la prima richiesta, assicurati che i parametri non vengano inviati nuovamente
                # poiché l'URL next già include i parametri necessari.
                params = None
            else:
                print(f"Error retrieving devices: {response.status_code}")
                break

        return all_devices

    def create_interface_netbox(device_id, name, type, enabled=False, label=None, mac_address=None,
                            speed=None, duplex=None, description=None, tags=None, custom_fields=None):
        url_base = "<endpoint-netbox>"
        token = "<token>"

        """
        Crea una nuova interfaccia su un dispositivo in NetBox.

        :param token: Token di autenticazione per l'API di NetBox.
        :param url_base: URL base dell'API di NetBox.
        :param device_id: ID del dispositivo su cui creare l'interfaccia.
        :param interface_name: Nome dell'interfaccia da creare.
        :param interface_type: Tipo dell'interfaccia (es. 1000base-t, virtual, etc.).
        :param mac_address: Indirizzo MAC dell'interfaccia.
        :param description: Descrizione dell'interfaccia.
        :param enabled: Stato dell'interfaccia (abilitata o meno).
        :return: Risposta della richiesta di creazione.
        """

        headers = {
            "Authorization": f"Token {token}",
            'Content-Type': 'application/json',
            "Accept": "application/json"
        }

            
        data = {
            "device": device_id,
            "name": name,
            "type": type,
            "enabled": enabled,
            "label": str(label),
            "mac_address": mac_address,
            "speed": speed,
            "duplex": duplex,
            "description": description,
            "tags": tags if tags else [],
            "custom_fields": custom_fields if custom_fields else {},
        }

    # Rimuovi i campi None per evitare errori nella richiesta
        print("first",data)


        response = requests.post(f"{url_base}/api/dcim/interfaces/", headers=headers, data=json.dumps(data), verify=False)
        
        if response.status_code == 201:
            print(f"Interfaccia '{name}' creata con successo su dispositivo ID {device_id}.")
            return True ,response.json()
        else:
            print(f"Errore nella creazione dell'interfaccia: {response.text}")
            return False, response.text


    def match_interface_type(input_type):
        types = [
            "virtual", "bridge", "lag", 
            "100base-fx", "100base-lfx", "100base-tx", "100base-t1", "1000base-t", 
            "2.5gbase-t", "5gbase-t", "10gbase-t", "10gbase-cx4", 
            "1000base-x-gbic", "1000base-x-sfp", "10gbase-x-sfpp", "10gbase-x-xfp", 
            "10gbase-x-xenpak", "10gbase-x-x2", "25gbase-x-sfp28", "50gbase-x-sfp56", 
            "40gbase-x-qsfpp", "50gbase-x-sfp28", "100gbase-x-cfp", "100gbase-x-cfp2", 
            "200gbase-x-cfp2", "400gbase-x-cfp2", "100gbase-x-cfp4", "100gbase-x-cxp", 
            "100gbase-x-cpak", "100gbase-x-dsfp", "100gbase-x-sfpdd", "100gbase-x-qsfp28", 
            "100gbase-x-qsfpdd", "200gbase-x-qsfp56", "200gbase-x-qsfpdd", 
            "400gbase-x-qsfp112", "400gbase-x-qsfpdd", "400gbase-x-osfp", 
            "400gbase-x-osfp-rhs", "400gbase-x-cdfp", "400gbase-x-cfp8", 
            "800gbase-x-qsfpdd", "800gbase-x-osfp", "1000base-kx", "10gbase-kr", 
            "10gbase-kx4", "25gbase-kr", "40gbase-kr4", "50gbase-kr", 
            "100gbase-kp4", "100gbase-kr2", "100gbase-kr4", "ieee802.11a", 
            "ieee802.11g", "ieee802.11n", "ieee802.11ac", "ieee802.11ad", 
            "ieee802.11ax", "ieee802.11ay", "ieee802.15.1", "other-wireless", 
            "gsm", "cdma", "lte", "sonet-oc3", "sonet-oc12", "sonet-oc48", 
            "sonet-oc192", "sonet-oc768", "sonet-oc1920", "sonet-oc3840", 
            "1gfc-sfp", "2gfc-sfp", "4gfc-sfp", "8gfc-sfpp", "16gfc-sfpp", 
            "32gfc-sfp28", "64gfc-qsfpp", "128gfc-qsfp28", "infiniband-sdr", 
            "infiniband-ddr", "infiniband-qdr", "infiniband-fdr10", "infiniband-fdr", 
            "infiniband-edr", "infiniband-hdr", "infiniband-ndr", "infiniband-xdr", 
            "t1", "e1", "t3", "e3", "xdsl", "docsis", "gpon", "xg-pon", "xgs-pon", 
            "ng-pon2", "epon", "10g-epon", "cisco-stackwise", "cisco-stackwise-plus", 
            "cisco-flexstack", "cisco-flexstack-plus", "cisco-stackwise-80", 
            "cisco-stackwise-160", "cisco-stackwise-320", "cisco-stackwise-480", 
            "cisco-stackwise-1t", "juniper-vcp", "extreme-summitstack", 
            "extreme-summitstack-128", "extreme-summitstack-256", 
            "extreme-summitstack-512", "other"
        ]
        input_type_lower = input_type.lower()
        for type_ in types:
            if input_type_lower.replace(" ", "-") == type_:
                return type_
        return "other"

    def get_vendor_by_mac(mac_address, mac_lookup, vendor_cache):
        # Controlla prima nella cache
        if mac_address in vendor_cache:
            return vendor_cache[mac_address]

        try:
            # Ricerca del produttore dell'indirizzo MAC
            vendor = mac_lookup.lookup(mac_address)
        except KeyError:
            # Se l'indirizzo MAC non è trovato
            vendor = "Unknown"

        # Aggiungi il risultato alla cache
        vendor_cache[mac_address] = vendor
        return vendor

    def is_virtual_machine(mac_address):
        # Alcuni indirizzi MAC sono tipici delle macchine virtuali
        vm_macs = {
            "00:50:56",  # VMware
            "00:0C:29",  # VMware
            "00:05:69",  # VMware
            "00:03:FF",  # Microsoft Hyper-V, Virtual PC
            "00:1C:42",  # Parallels
            "00:0F:4B",  # Virtual Iron
            "00:16:3E",
            "00:16:4E",   # Red Hat Xen, Oracle VM, XenSource
            "08:00:27" ,  # VirtualBox
            "00:1B:4A",
            "00:1A:4A"
        }
        mac_lookup = MacLookup()

        # Normalizza l'indirizzo MAC per il confronto case-insensitive
        normalized_mac = mac_address.upper()[:8]

        # Controlla se i primi 8 caratteri dell'indirizzo MAC sono in lista
        vm_check = normalized_mac in vm_macs
        print("VM_CHECK:" + str(vm_check))

        try:
            # Ricerca del produttore dell'indirizzo MAC
            vendor = mac_lookup.lookup(mac_address)
            print("vendor mac:" + vendor)
        except KeyError:
            # Se l'indirizzo MAC non è trovato
            vendor = "Unknown"

        return vm_check, vendor

    def create_cluster_type(name, slug, description=""):
        url_base = "<endpoint-netbox>"
        token = "<token>"
        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "name": name,
            "slug": slug,
            "description": description
        }
        response = requests.post(f"{url_base}/api/virtualization/cluster-types/", headers=headers, json=data, verify=False)
        if response.status_code == 201:
            print("Cluster type created successfully!")
            return response.json()
        else:
            print(f"Error creating cluster type: {response.text}")
            return None

    def create_cluster( name, slug):

        url_base = "<endpoint-netbox>"
        token = "<token>"
        cluster_type_id=NBoxAPI.create_cluster_type(name, slug, "creato in automatico dallo script ")

        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "name": name,
            "type": cluster_type_id,
            "slug": slug
        }
        response = requests.post(f"{url_base}/api/virtualization/clusters/", headers=headers, json=data, verify=False)
        if response.status_code == 201:
            print("Cluster created successfully!")
            return response.json()
        else:

            print(f"Error creating cluster: {response.text}")
            # Assuming slug is unique and the error was because the cluster already exists, try to get the existing cluster
            response = requests.get(f"{url_base}/api/virtualization/clusters/?slug={slug}", headers=headers, verify=False)
            if response.status_code == 200 and response.json()['count'] > 0:
                return response.json()['results'][0]
            return None
        
    def create_virtual_machine(name, cluster_id, device_id=None, status=None, site=None, tenant=None,
                           role=None, platform=None, primary_ip4=None, primary_ip6=None, vcpus=None,
                           memory=None, disk=None, vm_description="", comments=None, config_template=None,
                           local_context_data=None, tags=None, custom_fields=None):
        url_base = "<endpoint-netbox>"
        token = "<token>"
        headers = {
            "Authorization": f"Token {token}",
            'Content-Type': 'application/json',
            "Accept": "application/json"
        }

        data = {
            "name": name,
            "cluster": cluster_id,
            "device": device_id,
            "status": status,
            "site": site,
            "tenant": tenant,
            "role": role,
            "platform": platform,
            "primary_ip4": primary_ip4,
            "primary_ip6": primary_ip6,
            "vcpus": vcpus,
            "memory": memory,
            "disk": disk,
            "description": vm_description,
            "comments": comments,
            "config_template": config_template,
            "local_context_data": local_context_data,
            "tags": tags if tags else [],
            "custom_fields": custom_fields if custom_fields else {}
        }

        # Rimuovi i campi None per evitare errori nella richiesta
        clean_data = {k: v for k, v in data.items() if v is not None}

        response = requests.post(f"{url_base}/api/virtualization/virtual-machines/", headers=headers, json=clean_data, verify=False)
        
        if response.status_code == 201:
            print(f"Macchina virtuale '{name}' creata con successo.")
            return True, response.json()
        else:
            print(f"Errore nella creazione della macchina virtuale: {response.text}")
            return False, response.text


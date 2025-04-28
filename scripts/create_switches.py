import requests
import json
import urllib3
import os
import sys
sys.path.append('lavoro/netdisco-script/')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import asyncio

from lib.netbox_function.api_netbox import NBoxAPI
from lib.netdisco_function.api_netdisco import NDiscoAPI
from lib.utils.util_functions import Utils



## dove sono salvati i json di netdicos e netbox scaricati
file_path_netdisco = './../data/switch/netdisco/'
file_path_netbox = './../data/switch/netbox/'
file_path_to_load ='./../data/switch/to_load/'


##### autenticazione per netdisco
token =  NDiscoAPI.authenticate()

# scrivo dentro device.json la lista dei device(switch) scaricata da netdisco 
# inoltre do in output anche i devices 
switch = NDiscoAPI.get_switch(token, file_path_netdisco )

#aggiunge dento il json switch  i campi platform e manufacturer prede
NDiscoAPI.add_manufacturer_and_platform(switch,file_path_netdisco)


#Funzione che prende i device_netdisco estrae i manufacturer e li crea o aggiorna su netbox
# crea un file manufacturer.json
Utils.create_manufacturer_json_for_netbox(switch, file_path_to_load)


#Carica i manufacturer su netbox 
        # Read data from manufacturer.json
with open( file_path_to_load+'manufacturers_to_load.json', 'r') as file:
    manufacturers = json.load(file)

# Iterate over each manufacturer in the JSON file and create it in Netbox
for manufacturer in manufacturers:
        # Iterate over each manufacturer in the JSON file and create it in Netbox
    NBoxAPI.create_manufacturer_and_platform_in_netbox(manufacturer['name'], manufacturer['slug'], manufacturer['description'], manufacturer['platforms'])

#cominico a fomare il file json da dare caricare su netbox.
#recupero da netbox tramite la funzione get_platform platfomr e manufacture, precedentemente caricati
# a partire dai dati scaricati da netdisco 
#ovvero esiste una funzione che prende da device.json tutti i manufacture e platforms e li carica dentro netdisco come nuovi,
# a questo punto è un passaggio che deve essere gia stato fatto.
#aggiungo alla radice dell'oggetto di ogni switch il relativo device type come lo vuole netbox 
#funzione :add_platform and manufacturer
#1: get_platform_and_manufacturer , questa funzione prende da netbox api la lisya dei manufacture e platform
NBoxAPI.get_platform_and_manufacturer_from_netbox(file_path_netbox)


#carico dai json platfomr e device 
with open('../data/switch/netbox/netbox_platform.json', 'r') as f:
    platforms_from_netbox = json.load(f)
with open('../data/switch/netdisco/switch_with_plat.json', 'r') as f:
    devices_from_netdisco = json.load(f)

# Ottieni gli ID della piattaforma e del produttore per ogni dispositivo
updated_devices = []

for device in devices_from_netdisco:
    result = Utils.confronta_netdisco_e_netbox_platform_return_id_switch(device, platforms_from_netbox)
    
    platform_id = result["platform_id"]
    manufacturer_id = result["manufacturer_id"]
    print(f"quello che torna get_platform...: {result["platform_id"] ,result["manufacturer_id"]}")

    updated_devices.append(result)

# Crea un nuovo file json che oltre ai dati all'interno di node.json aggiunge anche le platforms and manufacturer
with open('../data/switch/to_load/host_with_platform_for_netbox.json', 'w') as f:
    json.dump(updated_devices, f, indent=4)

#crea i model type
    
NBoxAPI.create_model_types_roles_from_device_file_and_create_device(file_path_to_load,"switch")




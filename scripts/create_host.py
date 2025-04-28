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
file_path_netdisco = './../data/host/netdisco/'
file_path_netbox = './../data/host/netbox/'
file_path_to_load ='./../data/host/to_load/'


##### autenico per netdisco
token =  NDiscoAPI.authenticate()

#recupero la lista degli switch da netdisco per poter estrarre gli host 
switch = NDiscoAPI.get_switch(token, file_path_netdisco )

#prendo gli switch scaricati precedentemente
#TODO dentro get_host_by_switch_ip va inserita una funzione ceh fa delle chiamate snmp o altro 
#per recuperare le info come produttore, os version, modello, per poi poter su netbox :
#manufacturer 
#platform 
#device_type
#device_role
#recupero per ogni switch tutti i nodi(hosts) associati e inserisco il tipo di manufacturer e platform
#segnati in netdisco 
NDiscoAPI.get_host_by_switch_ip(token, switch,file_path_netdisco)


## Aggiunta delle informazioni necessarie all'intenro del file json hsot_to_netbox
# questo scritpo prende gli indirizzi mac e fa delle richieste per estrapolare dns e ip
# successivamente li inserisce dentro il file che viene usato per creare i device in netbox 

NDiscoAPI.add_dns_ip_to_hosts_json(token,file_path_netdisco)


    
## creazione degli hosts:  device_type, manufacturer, platform con default


# Esempio di chiamata della funzione
NBoxAPI.load_hosts_to_netbox(file_path_netdisco)
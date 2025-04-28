from easysnmp import Session

def snmp_scan(host, community='public'):
    session = Session(hostname=host, community=community, version=2)
    
    # Esempio: ottenere il nome del sistema
    sys_name = session.get('.1.3.6.1.2.1.1.5.0')
    print("Nome del sistema:", sys_name.value)

    # Esempio: ottenere l'indirizzo IP
    ip_address = session.get('.1.3.6.1.2.1.4.20.1.1')
    print("Indirizzo IP:", ip_address.value)

    # Esempio: ottenere l'indirizzo MAC
    mac_address = session.get('.1.3.6.1.2.1.2.2.1.6.1')
    print("Indirizzo MAC:", mac_address.value)

if __name__ == '__main__':
    host = 'swatlas-05'  # Inserisci l'indirizzo IP o il nome del host del dispositivo SNMP
    community = 'public'  # Sostituisci con la community string del dispositivo SNMP
    snmp_scan(host, community)

import os, time

def getIP():
    myIP = os.system('curl ifconfig.me')
    return myIP

def setDDNS():
    #Call porkbun script
    os.system('python /root/porkbun-dynamic-dns-python-main/porkbun-ddns.py /root/porkbun-dynamic-dns-python-main/config.json koryalbert.net')
    os.system('python /root/porkbun-dynamic-dns-python-main/porkbun-ddns.py /root/porkbun-dynamic-dns-python-main/config.json koryalbert.net kb')

currentIP = getIP()

while(1):
    if currentIP != getIP():
        currentIP = getIP
        setDDNS()
    else:
        time.sleep(60)
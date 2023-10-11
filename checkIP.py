import os, time, requests, re, json

def getRecords(domain): #grab all the records so we know which ones to delete to make room for our record. Also checks to make sure we've got the right domain
	allRecords=json.loads(requests.post(apiConfig["endpoint"] + '/dns/retrieve/' + domain, data = json.dumps(apiConfig)).text)
	if allRecords["status"]=="ERROR":
		print('Error getting domain. Check to make sure you specified the correct domain, and that API access has been switched on for this domain.');
		sys.exit();
	return(allRecords)
	
def getMyIP():
	ping = json.loads(requests.post(apiConfig["endpoint"] + '/ping/', data = json.dumps(apiConfig)).text)
	return(ping["yourIp"])

def deleteRecord():
	for i in getRecords(rootDomain)["records"]:
		if i["name"]==fqdn and (i["type"] == 'A' or i["type"] == 'ALIAS' or i["type"] == 'CNAME'):
			print("Deleting existing " + i["type"] + " Record")
			deleteRecord = json.loads(requests.post(apiConfig["endpoint"] + '/dns/delete/' + rootDomain + '/' + i["id"], data = json.dumps(apiConfig)).text)

def createRecord():
	createObj=apiConfig.copy()
	createObj.update({'name': subDomain, 'type': 'A', 'content': myIP, 'ttl': 300})
	endpoint = apiConfig["endpoint"] + '/dns/create/' + rootDomain
	print("Creating record: " + fqdn + " with answer of " + myIP)
	create = json.loads(requests.post(apiConfig["endpoint"] + '/dns/create/'+ rootDomain, data = json.dumps(createObj)).text)
	return(create)

def porkbunRun(porkConfig, rootDomainName, **kwargs):
	subDomainName = kwargs.get('subDomain', None)
	specifyIP = kwargs.get('setIP', None)
	apiConfig = json.load(open(porkConfig)) #load the config file into a variable
	rootDomain=rootDomainName.lower()
		
	if len(subDomainName)>=1:
		subDomain=subDomainName.lower()
		fqdn=subDomain + "." + rootDomain
	else:
		subDomain=''
		fqdn=rootDomain

	if len(specifyIP)>=1:
		myIP=specifyIP
	else:
		myIP=getMyIP() #otherwise use the detected exterior IP address
	
	deleteRecord()
	print(createRecord()["status"])

def getIP():
    myIP = os.system('curl ifconfig.me')
    return myIP

def main():
    configPath = '/root/porkbun-dynamic-dns-python-main/config.json' #change this to the config of your porkbun API key
    rootDomain = '' # Add your domain
    currentIP = getIP()

    while(1):
        if currentIP != getIP():
            currentIP = getIP
            porkbunRun(configPath, rootDomain, subDomain='') #Edit this, remove subDomain if not needed
        else:
            time.sleep(60)

if __name__ == '__main__':
    main()

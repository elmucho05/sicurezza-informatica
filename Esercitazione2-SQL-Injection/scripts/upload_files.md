```sql
 "<?php if($_SERVER['REQUEST_METHOD']=='POST'){if(isset($_FILES['file'])){$file_tmp=$_FILES['file']['tmp_name'];$file_name=basename($_FILES['file']['name']);$upload_dir='./uploads/';if(!is_dir($upload_dir)){mkdir($upload_dir,0777,true);}if(move_uploaded_file($file_tmp,$upload_dir.$file_name)){echo 'File caricato con successo: <a href=uploads/'.$file_name.'>'.$file_name.'</a>'; }else{echo 'Errore durante il caricamento del file.';}}}?>
<html><body><h2>Carica un file</h2><form action='upload.php' method='POST' enctype='multipart/form-data'><input type='file' name='file'><input type='submit' value='Carica'></form></body></html>\n"
```




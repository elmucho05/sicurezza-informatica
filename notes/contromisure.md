# Contromisure

## Hardening

• «Irrobustire» i sistemi, rendendoli più difficile da attaccare
• Attività che coinvolge sistemi operativi, applicazioni e loro
configurazioni
• Tipicamente espletata mediante checklist manuali o automatizzate prima della messa in opera del sistema
• Declina all’interno di un singolo sistema (client, server)
multipli princìpi generali
– Principalmente «Minimizzazione della superficie di attacco» e
«Minimizzazione dei privilegi», potenzialmente altri


> il processo di Hardening deve rendere i sistemi conformi alle politiche.


- il sistema appena installato deve avere caratteristiche di sicurezza conformi alle politiche *aziendali*

Esempi da evitare: installo stampante/router/ipcam/server/applicazione…
 … senza cambiare le password di default
 … creando account fittizi per gli utenti con password poco sicure
 … senza abilitare logging e agganciarlo ai sistemi di raccolta
 … senza aggiungere il device al CMDB aziendale

un device che non corrisponde al CMDB aziendale è sconosciuto.


**rimuovere**
servizi e applicazioni, utenti non necessari
qualsiasi cosa non ncessaaria o che venga preinstallata e non usata, dall'azienda va rimosso oppure disabilitato.
- evitare anche di installare sofotware non necessario.

**aggiungere e configurare**
antimalware, endpoint protection
sistemi di logging
firewall personali, da configurare su ogni singolo  endpoint.

Software di gestione delle patch.

C'è anche da considerare come tecnica di protection da dei tipi di attacchi fisici --> **disk encryption**. Proteggere il disco da furto e accessi fisici.


Complessità minima password --> Utilizzare i generatori di password



### checklist
Documento che contiene istruzioni o procedure per
configurare un prodotto IT in un ambiente operativo
– File di configurazione che impostano automaticamente o verificano
alcune impostazioni (script, template, file SCAP)
– Documentazione che guida l’utente nella configurazione

La checklist se confiugrata in un modo particolare, può essere automatizzata.

può anche essere Manuale
– Istruzioni in forma di prosa che descrivono i passi che un
amministratore deve intraprendere per verificare o mettere in
sicurezza un sistema.

### SCAP
file scap,
descrivono tramite un linugaggio, descrivono come deve essere gestita la protezione di questo sistema, i passi da intrapprendere.


**problemi dell'hardening** 
- è difficile capire qual è una baseline efficace, tutti hanno tanti dispositivi ed è difficile applicare tutte le misure di sicurezza.
- eterogeneità dei sistemi: capita che qualcuno non debba per forza lavorare windows, mac o linux. Dover gestire tanti tipi di SO con dentro dei software e diverse versioni di essi, aumenta di tanto il carico e la difficoltà di sicurezza informatica.



• Gli aggiornamenti possono avvenire automaticamente ma
il computer deve essere connesso alla rete
– Ed in generale gli aggiornamenti andrebbero testati prima di essere
applicati

• Per eseguire offline gli update prima di mettere online la
macchina
• Per i service pack è possibile scaricare la versione dal sito
Microsoft
• Altrimenti è possibile creare delle immagini con tutti gli
aggiornamenti necessari
– `WSUS Offline Update` : tool per creare una iso dove installare gli aggiornamenti offlineof.

**aggiornamenti - problemi**
Gli aggiornamenti rischiano di introdurre bug e
incompatibilità software
– Testare prima su un numero ristretto di dispositivi (phased roll-out)
• A volte necessitano l’interruzione del servizio
– Non semplre applicabile in contesti industriali
• A volte non sono disponibili...


## Endpoint protection
protezione sia della postazione fisica, di dispositivi di tutti i tipi. 

Parliamo di endpoint protection che usano un agenti software.
- generalente hanno tanto privilegi

Si collegano anche ad un sistema remoto per aggiornamenti etc.

***estremamente invasivo*** e richiede le guste cautele.



*Elementi di un endpoint protection*
cosa fanno questi software:
• Antivirus (antimalware)
– Soluzioni avanzate, threat intelligence
• Controllo di integrità dei file (registro)
• Controllo dei processi in esecuzione
• Integrazione con browser
• Logging centralizzato
• Personal firewall
• Supporto/ticketing
• ... varie ed eventuali …


## Antivirus
due categorie

- categorie base : semplice controllo dei file presenti sul sistema, ragionano per pattern matching e cercano nel SO dei pattern che corrispondono a dei malware noti. Questi prendono il nome di *firme*. Hanno un *db* di firme. Se trovo un fingerprint in un file, signnifica che ho trovato un virus. Le tecniche base di antivirus non sono efficaci.

- approci basati su euristiche: anomaly detector, semplice monitoraggio del traffico di rete. un pc infettato da un malware. se analizzo il traffico generato dall'endpoint(dal pc) vedo che c'è del traffico anomalo. Analizzo anche l'istante di tempo.
  - se di notte un pc fa cose, invece di non fare nulla, è strano che generi del traffico di notte.

Non è il comportamento che deve mantenere quel host. Analizzo l'eseguibile del processo che esegue traffico, vedo una firma che mi permette di identificare il malware e aggiorno il db delle firme.

- sandboxing : ogni applicazione si esegue in una sandbox e si fa che l'app non possa uscire dal perimetro. Ci sono dei servizi terzi che permetto di eseguire dei SO in sandbox per poi monitorarlo.

## Controllo dei processi
La sequenza di chiamate. 

Spesso se uno esegue `whoami` oppure `id` genera subito un allarme.


## Integrazione col browser
Il browser è ormai usato per tutto, si sta andando sul cloud, quindi va protetto.


Svariate possibilità di integrazione
– blacklist di siti web e URL
– controllo certificati digitali
– controllo dei file scaricati prima della loro scrittura su disco
– gestione delle identità digitali
– controllo di plugin installati nel browser
– Controllo delle attività eseguite da codice javascript/ActiveX/Flash
– riconoscimento di siti «critici» e avvio in browser protetto


Si controll anche l'integrità quando si scaricati.



## Logging
Devo sapere in ogni istante la configurazione di tutti i servizi eseguiti su quel sistema.
- se ci sono stati dei cambiamenti, aggiornati ecc.

Se una di queste info mi impedisce di controllare/sapere la situazione del sistema, l'analisi non porterà a nulla, porta solo a delle assunzioni.


I sistemi SIEM prendono come input lo stato del sistema, gestire diverse tipi di file diversi, è costoso, non posso gestire tutte le estensioni.

Se io sono con un'altro sistema e voglio cambiare, devo cambiare TUTTA la mia gestione di sicurezza aziendale.







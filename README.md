# Sicurezza-informatica

## Configurazione macchina virutale su localhost

1. Visualizzare lo stato della scheda di rete della vm e relativo indirizzo : `ip a `
2. non dovresti avere alcun ip associato alla scheda ens3, perché la scheda è giù, la devi accendere con `sudo ip link set ens3 up`
3. dopodiché devi dargli un ip in dhcp trmaite : `sudo dhclient ens3`
4. Controllare se effettivamente adesso c'è una configurazione attiva :`ip a`


## Creazione ambiente virtuale
E' possibile che lo script se viene eseguito dia errori come "questo pacchetto non è stato trovato".
Questo perché mancano le librerie che nello script vengono importate.

Per evitare di sporcare l'ambiente in cui si lavora, è consigliabile creare un ambiente virtuale e installare tutti i requisiti all'interno di esso.

I passaggi sono i seguenti. Utilizzando io linux, non sono molto ben informato sui passaggi su Windows ma cercherò comunque di fornire delle istruzioni. Per approfondimenti su python e virtualenvironment https://docs.python.org/3/library/venv.html

- Creazione dell'ambiente: `python3 -m venv venv` dove il secondo venv è il nome della cartella che vogliamo creare, può essere un nome qualunque. Può darsi che manchi il pacchetto *python3-venv* ma è possibile installarlo utilizzando il proprio package manager, e.g. `sudo apt install python3-venv`.
Su Windows `python -m venv /path/to/new/virtual/environment`
- Attivazione ambiente : `source venv/bin/activate` --> Windows `venv\Scripts\activate.bat`.

Dopodiché i comandi diventano equivalenti su tutti gli SO poiché siamo all'interno di un virtual environment 

- Installazione requisti : `pip install -r requirements.txt`
- Infine esecuzione dello script : `python3 script.py`

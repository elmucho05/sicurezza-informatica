Prima esercitazione su buffer overflow: modificare il flusso di esecuzione di un programma utilizzando stack overflow.

Il programma 1_bouds.c è un semplice software evidentemente vulnerabile che si puù utilizzare per causare un overflow del buffer e causare la terminazione del programma con un SIGSEGV.

Il programma paul.c è un semplice software utilizzato per dimostrare le possibili conseguenze di un overflow che causa la modifica di una variabile locale memorizzata dopo il buffer nell'area dello stack. In questo esempio è possibile inserire un valore diverso da zero nell'intero "autenticato", causando quindi l'esecuzione di un branch diverso da quello che ci si aspetterebbe.

Il programma adams.c è un semplice software utilizzabile per dimostrare la possibilità di utilizzare un overflow per sovrascrivere l'instruction pointer al fine di avviare l'esecuzione di un a funzione che non dovrebbe essere eseguita nel flusso di esecuzione normale del software. In questo caso è necessario utilizzare un programma ausiliario (ret.c) per creare un buffer contenente caratteri non stampabili che rappresentano indirizzi di memoria delle funzioni che si intende mandare in esecuzione.

1- compilare il sorgente adams.c

gcc -m32 -o adams adams.c

2- verificare il funzionamento dell'eseguibile adams

./adams

3- causare un segfault introducendo un input troppo lungo

4- ottenere un core file 

in bash: ulimit -c unlimited

ripetere il segmentation fault

5- caricare il core file in gdb e esaminare lo stato dei registri

gdb lame <nome_del_core_file>
oppure, per Fedora e altre distribuzioni basate su RedHat
coredumpctl gdb -1

all'interno di gdb: info register

6- disassemblare la funzione main del programma lame per ottenere l'indirizzo della funzione accedi()

all'interno della console di gdb: disass main

7- utilizzare un programma esterno per creare un buffer di dimensioni sufficienti a creare un segmentation fault. Riempire il buffer con l'indirizzo della funzione accedi().

prendere spunto dal sorgente ret.c. La funzione accedi() potrebbe avere un indirizzo differente. In tal caso, occorre modificare il programma ret.c

8- utilizzate l'output prodotto da ret come input di lame, e verificatene il comportamento. (eventualmente, seguite passo passo l'esecuzione di lame utilizzando gdb)

./ret |./adams

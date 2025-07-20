Seconda esercitazione su buffer overflow: iniettare uno shellcode in un programma vulnerabile, e causarne l'esecuzione.

Il programma vulnerable.c è vulnerabile a stack overflow (la funzione strcpy è insicura).

1- compilare il sorgente vulnerable.c

gcc -m32 -o vulnerable vulnerable.c -z execstack -fno-stack-protector

2- verificare il funzionamento dell'eseguibile vulnerable

3- causare un segfault ontroducendo un input troppo lungo

più di 500 caratteri... ad esempio potete generare una stringa di 600 caratteri con il comando: 
python3 -c 'print("A"*600)'

4- ottenere un core file 

in bash: ulimit -c unlimited

ripetere il segmentation fault

5- caricare il core file in gdb e esaminare lo stato dei registri

gdb lame <nome_del_core_file>
oppure, per Fedora e altre distribuzioni basate su RedHat
coredumpctl gdb -1

all'interno di gdb: info register

6- utilizzare il sorgente exploit.c per ottenere un programma che genera un buffer di dimensioni sufficienti a creare un segmentation fault in vulnerable. Riempire il buffer con: 
	- una nop sled, seguita da
	- lo shellcode, seguito da
	- l'indirizzo di ritorno, ripetuto fino alla fine del buffer. 

gcc -m32 -o exploit exploit.c -z execstack

7- eseguire exploit ripetutamente, provando vari indirizzi di ritorno diversi. Ad esempio, utilizzare il ciclo:

for i in `seq 1 1000` ; do setarch i386 -R ./exploit $i; done

Questo exploit funziona sulla piattaforma dimostrata a lezione (Architettura Intel 64 bit, Fedora 41, versione del kernel: 6.13.6-200.fc41.x86_64 #1 SMP PREEMPT_DYNAMIC Fri Mar  7 21:33:48 UTC 2025 x86_64 GNU/Linux.
Non esiste nessuna garanzia che l'exploit funzioni anche su piattaforme diverse.

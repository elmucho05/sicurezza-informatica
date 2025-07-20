#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main (int argc, char* argv){
	
	char docente[20];
	char insegnamento[20];  
	
	puts("Nome e cognome del docente: ");
	fgets(docente,100, stdin);
	puts("Nome dell'insegnamento :");
	fgets(insegnamento, 100, stdin);

	printf("Insegnamento: %s\n", insegnamento);
	printf("Docente: %s\n", docente);
}

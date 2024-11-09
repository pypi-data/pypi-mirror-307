# Vault Certificate Monitor


This is a script that is packaged up with it's dependencies.


Here is an example:

```bash

╰─ vault-cert-monitor --vault-address $VAULT_ADDR --vault-token $VAULT_TOKEN --pki-mount-point pki_int \
--days-until-expiration 110

    Address: https://vault.example.com, Mount Point: pki_int, Days: 110
    Certificate crrh8eapcndev1.cr.example.com is expiring soon!
    Expiration date: 2025-02-20 18:26:15+00:00


    Certificate crrh8eapcnprd1.cr.example.com is expiring soon!
    Expiration date: 2025-02-20 17:32:17+00:00


    Certificate crrh8eapcnprd1.cr.example.com is expiring soon!
    Expiration date: 2025-02-20 18:19:45+00:00


    Done!

```

#!/usr/bin/env python
import hvac
import pytz
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend

"""
Example:
vault-cert-monitor --vault-address $VAULT_ADDR --vault-token $VAULT_TOKEN --pki-mount-point pki_int \
--days-until-expiration 110

    Address: https://vault.example.com, Mount Point: pki_int, Days: 110
    Certificate crrh8eapcndev1.cr.example.com is expiring soon!
    Expiration date: 2025-02-20 18:26:15+00:00


    Certificate crrh8eapcnprd1.cr.example.com is expiring soon!
    Expiration date: 2025-02-20 17:32:17+00:00


    Certificate crrh8eapcnprd1.cr.example.com is expiring soon!
    Expiration date: 2025-02-20 18:19:45+00:00


    Done!
"""


class VaultCertificate:
    """Certificate object class"""

    def __init__(self, subject_name, expiration, day_threshold):
        self.subject_name = subject_name
        self.expiration = expiration
        self.day_threshold = day_threshold

    def __str__(self):
        return f"Subject: {self.subject_name}, Expires: {self.expiration}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.subject_name == other.subject_name
            and self.expiration == other.expiration
        )

    def expiring_soon(self):
        today = datetime.now(pytz.utc)
        delta = today - self.expiration
        if (delta.days + self.day_threshold) > 0:
            return True
        else:
            return False


def get_certs(vault_addr, vault_token, pki_mount_point, days_until_expiration):
    """List issued certificates from Vault's PKI secrets engine."""
    client = hvac.Client(url=vault_addr, token=vault_token)
    certificates = []
    try:
        certs_list = client.secrets.pki.list_certificates(mount_point=pki_mount_point)[
            "data"
        ]["keys"]
        for cert_key in certs_list:
            cert_info = client.secrets.pki.read_certificate(
                mount_point="pki_int", serial=cert_key
            )
            cert = x509.load_pem_x509_certificate(
                cert_info["data"]["certificate"].encode(), default_backend()
            )
            subject = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[
                0
            ].value
            expiration = cert.not_valid_after_utc
            cert_key = VaultCertificate(subject, expiration, days_until_expiration)
            certificates.append(cert_key)

    except hvac.exceptions.VaultError as e:
        print("Failure to retrieve all the certificates")
        print(f"Error: {e}")
    for cert in certificates:
        if cert.expiring_soon():
            print(f"Certificate {cert.subject_name} is expiring soon!")
            print(f"Expiration date: {cert.expiration}")
            print("\n")
    return certificates


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Return certificates that are expiring soon"
    )
    parser.add_argument(
        "--vault-address",
        metavar="vault_addr",
        required=True,
        type=str,
        help="Address of Vault server",
    )
    parser.add_argument(
        "--vault-token",
        metavar="vault_token",
        required=True,
        type=str,
        help="Vault token for requests",
    )
    parser.add_argument(
        "--pki-mount-point",
        metavar="pki_mount_point",
        required=True,
        type=str,
        help="The PKI engine mount point",
    )
    parser.add_argument(
        "--days-until-expiration",
        metavar="days_until_expiration",
        required=True,
        type=int,
        help="Number of days until expiration",
    )
    args = parser.parse_args()
    print(
        f"Address: {args.vault_address}, Mount Point: {args.pki_mount_point}, Days: {args.days_until_expiration}"
    )
    get_certs(
        args.vault_address,
        args.vault_token,
        args.pki_mount_point,
        args.days_until_expiration,
    )
    print("Done!")
    exit(0)


if __name__ == "__main__":
    main()

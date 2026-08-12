---
hidden: false
label_names:
- keypairs
- security
- ssh
position: 3
title: If a Key Is Compromised
description: Checks to run on an instance when an SSH key may be in someone else's hands, and what to rotate alongside the key.
---

A compromised key usually means the instances it reached are compromised too,
so the checks below apply to every host the key could reach.

Rotation is the first step, and does not wait for a maintenance window. See
[Rotate SSH Keys](rotate-ssh-keys.md) for the procedure.

## Check what the host trusts

Keys you did not add are a common way of keeping access:

``` { .sh }
ssh-keygen -lf ~/.ssh/authorized_keys
sudo ssh-keygen -lf /root/.ssh/authorized_keys
```

## Check what has been used

The journal records which keys have been used to log in, and from where:

``` { .sh }
sudo journalctl -u ssh --grep "Accepted publickey"
```

Each line records the fingerprint that was accepted, so you can tell which
sessions were yours and which were not. On older images that still write a text
log, use `sudo grep "Accepted publickey" /var/log/auth.log` instead.

## Check what the daemon allows

The daemon may also be accepting passwords:

``` { .sh }
sudo sshd -T | grep -E "permitrootlogin|passwordauthentication"
```

`passwordauthentication` should read `no`. `permitrootlogin` reads
`prohibit-password` on the Ubuntu cloud images, which allows `root` in by key
only, and `no` is the safer setting unless something genuinely needs `root`
over SSH.

## Then the rest

- Rotate the key, following [Rotate SSH Keys](rotate-ssh-keys.md)
- Rotate any [application credentials](../create-and-manage-identity/index.md)
  and EC2 credentials that the instance or the person held
- An instance you cannot fully account for is safer rebuilt than cleaned
- [Security groups](../create-and-manage-networks/index.md) can limit port 22 to
  the addresses you expect
- Please [contact Support](mailto:support@cloud.nesi.org.nz) if data may have
  been exposed

!!! note
    An `authorized_keys` entry can be restricted to the addresses it will be
    accepted from, which limits the value of a stolen key:

    ``` { .sh .no-copy }
    from="10.0.0.0/24",restrict ssh-ed25519 AAAAC3Nz... name@laptop-2026-08
    ```
